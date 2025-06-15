from django.contrib import admin

from website.models import OpportunityGrants

@admin.register(OpportunityGrants)
class OpportunityGrantsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if OpportunityGrants.objects.exists():
            return False
        return True