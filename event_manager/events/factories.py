import factory
import random
from datetime import timedelta

from django.utils import timezone

from . import models


categories = [
    "Sports",
    "Talk",
    "Cooking",
    "Freetime",
    "Hiking",
    "Movies",
    "Travelling",
    "Science",
    "Arts",
    "Pets",
    "Music",
    "Wellness",
]


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Category
        django_get_or_create = ("name",)

    name = factory.Iterator(categories)
    sub_title = factory.Faker("sentence")
    description = factory.Faker("paragraph", nb_sentences=20)


class EventFactory(factory.django.DjangoModelFactory):
    """
    EventFactory(author=bob)
    """

    class Meta:
        model = models.Event

    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("sentence")
    sub_title = factory.Faker("sentence")
    description = factory.Faker("paragraph", nb_sentences=20)
    min_group = factory.LazyAttribute(
        lambda _: random.choice(list(models.Event.Group.values))
    )

    date = factory.Faker(
        "date_time_between",
        start_date=timezone.now() + timedelta(days=1),
        end_date=timezone.now() + timedelta(days=60),
        tzinfo=timezone.get_current_timezone(),
    )
