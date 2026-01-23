from django.urls import path

from .views import (
    TemperatureView,
    CategoryAPIView,
    CategoryListCreateAPIView,
    EventListCreateAPIView,
)

urlpatterns = [
    # api/events/
    path("", EventListCreateAPIView.as_view(), name="events-list-create"),
    path("category", CategoryListCreateAPIView.as_view(), name="category"),
    path("categories", CategoryAPIView.as_view(), name="categories"),
    # api/events/temperature
    path("temperature", TemperatureView.as_view(), name="temperature"),
]
