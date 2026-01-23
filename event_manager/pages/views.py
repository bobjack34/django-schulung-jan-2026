from django.shortcuts import render
from django.views.generic import TemplateView

from events.models import Event, Category


class HomePageView(TemplateView):
    """Stellt die Homepage dar und zeigt
    5 Events und 5 Kategorien."""

    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        """Über diese Methode können wir den Kontext anreichern."""
        ctx: dict = super().get_context_data(**kwargs)
        ctx["events"] = Event.objects.all()[:5]
        ctx["categories"] = Category.objects.all()[:5]

        return ctx
