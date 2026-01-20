from django.http import HttpRequest, HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Category, Event


class EventDetailView(DetailView):
    """
    Anzeigen einer Event-Detailseite
    Template liegt events/events/event_detail.html
    events/3
    """

    model = Event


class EventListView(ListView):
    """
    Auflisten der Events
    Template muss unter events/event_list.html liegen
    /events
    """

    model = Event
    # template_name = "events/event_list.html"


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
