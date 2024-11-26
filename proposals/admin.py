from django.contrib import admin
from . import models


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProposalType)
class ProposalTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Proposal)
class ProposalAdmin(admin.ModelAdmin):
    pass
