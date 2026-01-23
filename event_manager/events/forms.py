"""
Hier werden die Formulare definiert
"""

from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ("author",)

        widgets = {
            "date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }
        # Formular-Labels umbenennen
        labels = {
            "sub_title": "Slogan",
            "name": "Name des Events",
        }

    def clean_sub_title(self) -> str:
        """Wird für das Feld sub_title aufgerufen,
        wenn in der View is_valid() aufgerufen wird.
        is_valid() generiert ein cleaned_data-Dictionary,
        mit den bereinigten und konvertieren feldwerten.

        Der Rückgabewert dieser Methode ist in diesem Fall der neue sub_title
        """
        sub_title = self.cleaned_data["sub_title"]
        illegal_chars = ("*", "#")
        if isinstance(sub_title, str) and sub_title.startswith(illegal_chars):
            raise ValidationError("* und # sind nicht erlaubt am Anfang des Sub-titles")

        return sub_title

    def clean(self):
        """
        Wird aufgerufen, nachdem die cleaned_* - Funktionen aufgerufen wurden.
        Felder, die in den cleaned_* - fehlschlagen, sind NICHT mehr im cleaned_data
        dict vorhanden.
        """
        self.cleaned_data = super().clean()

        # print("cleaned data:", self.cleaned_data.keys())
        name = self.cleaned_data.get("name")
        sub_title = self.cleaned_data.get("sub_title")

        if name == sub_title:
            self.add_error("name", "Es ist ein Fehler im Name-Feld")
            self.add_error("sub_title", "Es ist ein Fehler im Slogan")
            raise ValidationError("Name und Slogan dürfen nicht gleich sein!")

        return self.cleaned_data


class CategoryForm(forms.ModelForm):
    """
    ModelForm baut auf Basis des Models ein Formular
    """

    class Meta:
        model = Category
        fields = "__all__"  # alle felder berücksichtigen
