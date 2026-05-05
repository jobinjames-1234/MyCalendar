from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "created_at", "last_edited_at")
    list_filter = ("date",)
    search_fields = ("user__username", "user__email", "content")
