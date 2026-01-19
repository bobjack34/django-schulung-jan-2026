from django.db import models


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
    name = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events",
    )
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
