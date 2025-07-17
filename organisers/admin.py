from django.contrib import admin
from .models import Organiser


@admin.register(Organiser)
class OrganiserAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "get_country_display", "approved", "order")
    list_filter = ("approved", "country")
    search_fields = ("name", "role", "country")
    ordering = ("approved", "order", "name")
    list_editable = ("approved", "order")
    actions = ["approve_organisers", "unapprove_organisers"]

    def get_country_display(self, obj):
        return f"{obj.country.flag} {obj.country.name}" if obj.country else ""

    get_country_display.short_description = "Country"

    def approve_organisers(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} organiser(s) approved successfully.")

    approve_organisers.short_description = "Approve selected organisers"

    def unapprove_organisers(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f"{updated} organiser(s) unapproved successfully.")

    unapprove_organisers.short_description = "Unapprove selected organisers"
