from django.contrib import admin

from sponsors.models import Sponsor, SponsorshipPackage, SponsorshipFile


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    pass

@admin.register(SponsorshipPackage)
class SponsorshipPackageAdmin(admin.ModelAdmin):
    pass

@admin.register(SponsorshipFile)
class SponsorshipFileAdmin(admin.ModelAdmin):
    pass

