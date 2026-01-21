"""
Hier werden die Formulare definiert
"""

from django import forms

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


class CategoryForm(forms.ModelForm):
    """
    ModelForm baut auf Basis des Models ein Formular
    """

    class Meta:
        model = Category
        fields = "__all__"  # alle felder berücksichtigen
