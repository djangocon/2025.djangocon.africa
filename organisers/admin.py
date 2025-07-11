from django.contrib import admin
from .models import Organiser


@admin.register(Organiser)
class OrganiserAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "get_country_display", "order")
    search_fields = ("name", "role", "country")
    ordering = ("order", "name")

    def get_country_display(self, obj):
        return f"{obj.country.flag} {obj.country.name}" if obj.country else ""

    get_country_display.short_description = "Country"
