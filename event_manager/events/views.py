import logging


from django.http import HttpRequest, HttpResponse, Http404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Category, Event
from .forms import CategoryForm, EventForm


logger = logging.getLogger(__name__)


class UserIsOwner(UserPassesTestMixin):
    """prüft, ob der eingeloggte User auch der Author des Events ist."""

    def test_func(self) -> bool:
        """Wenn User der Author ist, return True, ansonsten False.
        Ausnahme: Adminuser darf auch die Aktion ausführen.
        """
        return (
            self.request.user == self.get_object().author
            or self.request.user.is_superuser
        )


class EventDeleteView(UserIsOwner, SuccessMessageMixin, DeleteView):
    """
    Löschen eines Events
    Template liegt unter events/event_confirm_delete.html
    events/delete/42
    """

    model = Event
    success_url = reverse_lazy("events:events")  # Redirect nach Löschen
    success_message = "Event wurde erfolgreich gelöscht!"


class EventUpdateView(UserIsOwner, SuccessMessageMixin, UpdateView):
    """
    Uupdate eines Events
    Template liegt unter events/event_form.html
    events/update/42
    """

    model = Event
    form_class = EventForm
    success_message = "Event wurde erfolgreich editiert!"

    def form_invalid(self, form):
        messages.error(self.request, "Da gab es einen Fehler!")
        return super().form_invalid(form)


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Eintragen eines neuen Events
    Template liegt unter events/event_form.html
    events/create
    """

    model = Event
    form_class = EventForm
    success_message = "Event wurde erfolgreich angelegt!"

    def form_valid(self, form):
        # Wir hatten den User aus dem Formular entfernt, deshalb
        # müssen wir ihn hier eintragen.
        # User muss eingeloggt sein (via admin zur Zeit)
        logger.debug("Das hat ja super geklappt %s", self.request.user)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Da gab es einen Fehler!")
        return super().form_invalid(form)


class EventDetailView(DetailView):
    """
    Anzeigen einer Event-Detailseite
    Template liegt events/events/event_detail.html
    events/3
    """

    model = Event


class EventSearchView(ListView):
    """
    /events?q=<SUCHWORD>
    """

    model = Event
    queryset = Event.objects.select_related("category", "author")

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


class EventListView(ListView):
    """
    Auflisten der Events
    Template muss unter events/event_list.html liegen
    Default Queryset: Event.objects.all()
    /events
    """

    model = Event

    # bei reverse-foreignkey oder many-to-many nimmt man:
    # queryset = Event.objects.prefetch_related("category", "author")

    # bei foreign key beziehungen:
    queryset = Event.objects.select_related("category", "author")
    # template_name = "events/event_list.html"

    def get_queryset(self):
        # http://127.0.0.1:8000/events/?category=Sports
        qs = super().get_queryset()
        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category__name__iexact=category)
        return qs


def category_create(request):
    """
    Anlegen einer neuen Kategorie

    GET & POST: /events/categories/create
    """
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            # form.save() fürht intern Category.save()
            # messages.error(request, "Diese Aktion ist nicht erlaubt!")
            category = form.save()
            # return redirect("events:categories")
            return redirect("events:category-detail", pk=category.pk)
    else:
        form = CategoryForm()

    return render(
        request,
        "events/category_form.html",
        {
            "form": form,
        },
    )


def category_detail(request, pk: int):
    """
    Detailseite einer kategorie

    /events/categories/3423
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise Http404("kategorie not found")

    return render(
        request,
        "events/category_detail.html",
        {
            "category": category,
        },
    )


def categories(request):
    """
    Liste der Kategorien
    /events/categories
    """
    qs = Category.objects.all()

    return render(
        request,
        "events/categories.html",
        {
            "categories": qs,
        },
    )


def dummy(request: HttpRequest) -> HttpResponse:
    """
    eine Beispiel-View:
    muss http-request entgegennehmen
    muss http-response zurückgeben

    http://127.0.0.1:8000/events/dummy
    """
    return HttpResponse("Hello, World!")


def event_list(request):
    """erzeuge kommaseparierte Liste der Events.

    events/all
    """
    events = Event.objects.all()
    names = [event.name for event in events]
    return HttpResponse(", ".join(names))
