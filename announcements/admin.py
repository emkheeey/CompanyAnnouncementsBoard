from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'posted_by', 'date']
    list_filter = ['date', 'posted_by']
    search_fields = ['title', 'message']
    readonly_fields = ['id', 'date']
    ordering = ['-date']