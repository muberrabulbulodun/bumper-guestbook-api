from django.contrib import admin
from .models import User, Entry


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_date")
    search_fields = ("name",)
    ordering = ("-created_date",)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "subject", "created_date")
    search_fields = ("user__name", "subject", "message")
    list_filter = ("created_date",)
    ordering = ("-created_date",)
