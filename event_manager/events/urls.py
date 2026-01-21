"""
Event URLs
"""

from django.urls import path
from .views import (
    categories,
    category_detail,
    category_create,
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
)

app_name = "events"  # auf Basis von app_name:path_name wird die URL gebildet

urlpatterns = [
    path("", EventListView.as_view(), name="events"),
    path("<int:pk>", EventDetailView.as_view(), name="event-detail"),
    path("update/<int:pk>", EventUpdateView.as_view(), name="event-update"),
    path("delete/<int:pk>", EventDeleteView.as_view(), name="event-delete"),
    path("create", EventCreateView.as_view(), name="event-create"),
    path("categories", categories, name="categories"),
    path("categories/create", category_create, name="category-create"),
    path("categories/<int:pk>", category_detail, name="category-detail"),
]


# http://127.0.0.1:8000/events/dummy
# path("dummy", dummy, name="dummy"),
# http://127.0.0.1:8000/events/all
# soll eine kommaseparierte liste der Events (Eventnamen)
# zurückgeben in der HttpResponse:
# Event A, Event B, Event C
# path("all", event_list, name="event_list"),
