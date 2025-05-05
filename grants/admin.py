# grants/admin.py
from django.contrib import admin
from .models import GrantApplication, VerificationCode

@admin.register(GrantApplication)
class GrantApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'status', 'grant_type', 'timestamp')
    list_filter = ('status', 'grant_type')
    search_fields = ('full_name', 'email')

@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created_at', 'expires_at')

# Register your models here.
