import logging

from datetime import timedelta
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from events.factories import CategoryFactory, EventFactory
from events.models import Category, Event

logging.disable(logging.WARNING)

logger = logging.getLogger(__name__)


def show_form_errors(response) -> None:
    """Show Form Errors from response context."""

    if isinstance(response.context, dict) and "form" in response.context:
        form = response.context["form"]

        # Check if the form has errors
        if form.errors:
            print("Form Errors:", form.errors)

            # For a more detailed output, iterate through the errors
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in field '{field}': {error}")
        else:
            print("No form errors found.")
    else:
        print("Form is not in the context.")


def create_user(username):
    user = get_user_model().objects.create_user(
        username=username,
        password="xzy",
    )
    return user


class EventTests(TestCase):
    """Testen von Event-Endpunkten."""

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user("Bob")
        cls.other_user = create_user("Alice")
        cls.event_1 = EventFactory.create(author=cls.user)
        cls.event_2 = EventFactory.create(author=cls.user)
        cls.client = Client()
        cls.category = CategoryFactory()

        cls.valid_payload = {
            "name": "Test Event",
            "sub_title": "xyz",
            "description": "syz",
            "min_group": 5,
            "category": cls.category.pk,
            "date": timezone.now() + timedelta(hours=2),
        }

    def test_event_overview_is_public(self):
        """Testen, ob die Übersicht der Events öffentlich erreichbar ist
        und die entsprechenden Daten zeigt.

        Erwartung:
        - Status Code 200
        - Template: events/event_list.html
        - Antwort enthält den Namen/Title eines Events
        """
        url = reverse("events:events")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name="events/event_list.html")
        self.assertContains(response, text=self.event_1.name)

    def test_create_event_with_authenticated_user(self):
        """Testen, ob ein authentifzierter User einen Event anlegen kann.

        Erwartung GET:
        - Status Code 200
        - Template: events/event_form.html

        Erwartung POST:
        - Status Code 302
        - Wurde der Event in die DB eingetragen?
        - stimmt die Redirect Addresse?
        """
        url = reverse("events:event-create")
        self.client.force_login(self.user)
        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name="events/event_form.html")
        # POST
        response = self.client.post(url, self.valid_payload)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        obj = Event.objects.get(name=self.valid_payload["name"])
        self.assertEqual(obj.name, self.valid_payload["name"])
        self.assertRedirects(response, obj.get_absolute_url())

    def test_create_event_with_non_authenticated_user(self):
        """Testen, ob ein nicht-authentifzierter User keinen Event anlegen kann.

        Erwartung GET:
        - Status Code 302

        Erwarung POST:
        - Status Code 302
        - kein Objekt wurde eingetragen
        """
        url = reverse("events:event-create")
        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # POST
        response = self.client.post(url, self.valid_payload)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(
            not Event.objects.filter(name=self.valid_payload["name"]).exists()
        )
        self.assertEqual(2, Event.objects.count())

    def test_update_event_with_non_owner(self):
        """Testen, ob ein Nicht-Eigentümer eines Events einen Event nicht ändern kann."""
        url = reverse("events:event-update", args=[self.event_1.pk])
        # Anderer User loggt sich ein und feuert Request ab
        self.client.force_login(self.other_user)
        response = self.client.get(url)
        # prüfen ob Status Code 403
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertNotEqual(self.other_user, self.event_1.author)
