"""
Event URLs
"""

from django.urls import path
from .views import dummy

urlpatterns = [
    # http://127.0.0.1:8000/events/dummy
    path("dummy", dummy, name="dummy"),
]
