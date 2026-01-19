"""
Hier können die Models registriert werden,
um sie in der Administrationsoberfläche zur
Verfügung zu stellen.

http://127.0.0.1:8000/admin

Vorher einen Superuser anlegen:
python manage.py createsuperuser
"""

from django.contrib import admin
from .models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Felder in der Übersicht
    list_display = ["id", "name", "sub_title", "number_events"]
    list_display_links = ["id", "name"]

    def number_events(self, obj: Category):
        # greift auf den related_name des Event-Models zu (reverse Beziehung)
        return obj.events.count()  # SELECT count(*) from ...


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sub_title", "is_active"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "sub_title"]  # Suchbox
    actions = ["set_inactive"]  # zusätzliche Aktion
    readonly_fields = ["created_at", "updated_at"]  # nur lesen auf Detailseite
    list_filter = ["category"]  # nach Kategorien Filtern

    @admin.display(description="Setze Events inaktiv")
    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)  # update events set is_active=False where...

    # bessere Aufteilung auf der Detailseite
    fieldsets = (
        ("Standard Infos", {"fields": ("name", "category")}),
        ("Detail Infos", {"fields": ("description", "sub_title", "is_active")}),
    )
