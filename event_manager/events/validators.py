from datetime import timedelta, datetime

from django.utils import timezone
from django.core.exceptions import ValidationError


def datetime_in_future(value: datetime) -> None:
    """Validierungsfunktionen haben KEINEN Rückgabewert!"""
    if value < timezone.now() + timedelta(hours=1):
        raise ValidationError(
            "Der Zeitpunkt muss mindestens 1 Stunde in der Zukunft liegen",
        )


def bad_word_filter(word_list: list[str], value: str) -> None:
    """Prüft ob verbotene Wörter in value vorhanden sind.

    word_list = ["evil", "doof"]
    wenn ein Element von word_list in value ist, soll
    ein Validationerror auftreten.
    """
    for word in word_list:
        if word in value:
            raise ValidationError(f"Das Wort {word} ist nicht erlaubt!")
