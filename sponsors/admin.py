from django.contrib import admin

from sponsors.models import Sponsor, SponsorshipPackage, File, TaggedFile


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    pass

@admin.register(SponsorshipPackage)
class SponsorshipPackageAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

@admin.register(TaggedFile)
class TaggedFileAdmin(admin.ModelAdmin):
    pass