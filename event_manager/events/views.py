from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def dummy(request: HttpRequest) -> HttpResponse:
    """
    eine Beispiel-View:
    muss http-request entgegennehmen
    muss http-response zurückgeben

    http://127.0.0.1:8000/events/dummy
    """
    return HttpResponse("Hello, World!")
