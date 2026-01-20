"""
Event URLs
"""

from django.urls import path
from .views import categories, category_detail, EventListView, EventDetailView

app_name = "events"  # auf Basis von app_name:path_name wird die URL gebildet

urlpatterns = [
    path("", EventListView.as_view(), name="events"),
    path("<int:pk>", EventDetailView.as_view(), name="event-detail"),
    path("categories", categories, name="categories"),
    path("categories/<int:pk>", category_detail, name="category-detail"),
]


# http://127.0.0.1:8000/events/dummy
# path("dummy", dummy, name="dummy"),
# http://127.0.0.1:8000/events/all
# soll eine kommaseparierte liste der Events (Eventnamen)
# zurückgeben in der HttpResponse:
# Event A, Event B, Event C
# path("all", event_list, name="event_list"),
