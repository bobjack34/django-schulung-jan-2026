from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from events.models import Category, Event
from .serializers import (
    EventOutputSerializer,
    EventInputSerializer,
    TemperatureSerializer,
    CategorySerializer,
)


class EventListCreateAPIView(ListCreateAPIView):
    """
    GET api/events/
    POST api/events/
    """

    # wie kann man sich authentifizieren?
    authentication_classes = [TokenAuthentication]

    # welche Rechte brauch ich? Autorisierung
    permission_classes = [IsAuthenticated]

    queryset = Event.objects.select_related("category", "author")

    def get_serializer_class(self):
        """
        bei POST nutzen wir EventInputSerializer
        bei GET nutzen wir EventOutputSerializer
        """
        if self.request.method == "POST":
            return EventInputSerializer
        return EventOutputSerializer

    def create(self, request, *args, **kwargs):
        """POST Anfrage verarbeiten."""
        # Serializer Klasse je nach http-Mthode (hier POST)
        serializer_class = self.get_serializer_class()  # Input

        # Serializer mit eingehenden Daten befüllen, prüfen und
        # via save() speichern. Als Argument von save()
        # übergeben wir den fehlenden Author.
        input_serializer = serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        event = input_serializer.save(author=self.request.user)

        # für die Rückgabe des POST requests nutzen wir einen
        # anderen Serializer (EventOutputSerializer)
        output_serializer = EventOutputSerializer(event)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class CategoryListCreateAPIView(ListCreateAPIView):
    """implementiert GET (für Liste von Kategorien) und POST
    (Anlegen einer neuen Kategorie).

    GET api/events/category
    POST api/events/category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryAPIView(APIView):
    """zeigt alle Kategorien.

    GET api/events/categories
    """

    def get(self, request):
        """Ausgehende Daten"""
        qs = Category.objects.all()
        s = CategorySerializer(qs, many=True)
        return Response(s.data, status=status.HTTP_200_OK)


class TemperatureView(APIView):
    """Soll per POST aufgerufen werden."""

    def post(self, request):
        """Eingehende Daten."""
        s = TemperatureSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        return Response(s.data, status=status.HTTP_200_OK)
