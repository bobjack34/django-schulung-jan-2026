"""
Project URLs
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("", include("pages.urls")),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("api/events/", include("events.api.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("apitoken", obtain_auth_token, name="obtain-token"),  # POST request!
    # generiert Schema:
    path(
        "schema/",
        SpectacularAPIView.as_view(api_version="v1"),
        name="schema",
    ),
    # generiert UI:
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),  # aus schema/
        name="swagger-ui",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
