from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.validators import MinLengthValidator


User = get_user_model()  # eine Klasse


class DateMixin(models.Model):
    """stellt created_at und updated_at zur Verfügung, soll aber keine eigene Tabelle sein"""

    created_at = models.DateTimeField(auto_now_add=True)  # wird einmalig gesetzt
    updated_at = models.DateTimeField(auto_now=True)  # wird immer gesetzt

    class Meta:
        abstract = True


class Category(DateMixin):
    name = models.CharField(max_length=100, unique=True)  # mandatory, VARCHAR 100
    # null=True => darf nullable in der DB, blank=True => darf im Formular leer sein
    # (zb. in der Admin-Oberfläche)
    sub_title = models.CharField(max_length=200, null=True, blank=True)  # optional
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"

    def __str__(self) -> str:
        return self.name


class Event(DateMixin):
    # Aufgabe: makemigrations und migrate machen

    class Group(models.IntegerChoices):
        BIG = 20, "große Gruppe"
        SMALL = 5, "kleine Gruppe"
        UNLIMITED = 0, "keine Begrenzung"

    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ],
    )
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events",
    )  # books.events.all()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events",
    )  # bob.events.all()
    date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    min_group = models.PositiveSmallIntegerField(
        choices=Group.choices, default=Group.UNLIMITED
    )

    def get_absolute_url(self) -> str:
        """Liefert die Homepage zu einem Event. Nach Eintragen oder Update wird auf
        diese Adresse weitergeleitet."""
        return reverse_lazy("events:event-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name
