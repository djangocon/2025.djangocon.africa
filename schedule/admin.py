from django.contrib import admin
from .models import Speaker, Room, ConferenceDay, Session


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'email']
    list_filter = ['company']
    search_fields = ['name', 'company', 'email']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'bio', 'photo', 'company', 'email')
        }),
        ('Social Media', {
            'fields': ('twitter', 'github', 'linkedin', 'mastodon', 'bluesky'),
            'classes': ('collapse',)
        })
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(ConferenceDay)
class ConferenceDayAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'order', 'is_active']
    list_filter = ['is_active', 'date']
    search_fields = ['name']
    ordering = ['order', 'date']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'conference_day', 'time_range', 'room', 'session_type', 'speaker', 'slug']
    list_filter = ['conference_day', 'room', 'session_type', 'is_break']
    search_fields = ['title', 'description', 'speaker__name', 'slug']
    ordering = ['conference_day__order', 'start_time', 'room__name']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'abstract', 'speaker', 'room', 'session_type', 'conference_day')
        }),
        ('Time & Schedule', {
            'fields': ('start_time', 'end_time', 'is_break')
        })
    )
