"""
python manage.py create_events --events 20
"""

import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from events.factories import CategoryFactory, EventFactory
from events.models import Category, Event


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.description = "Generate random events"
        parser.add_argument(
            "-e",
            "--events",
            type=int,
            help="Number of events to be generated",
            required=True,
        )

    def handle(self, *args, **kwargs):
        number = kwargs["events"]
        print(f"Number: {number}")

        print("Deleting Categories and Events...")
        Event.objects.all().delete()
        Category.objects.all().delete()

        print("Creating Categories...")
        categories = CategoryFactory.create_batch(10)
        users = get_user_model().objects.all()

        if not users:
            raise SystemExit("Keine User im System")

        print("Creating events...")
        for _ in range(number):
            EventFactory(
                category=random.choice(categories), author=random.choice(users)
            )
