from django.contrib import admin

from .models import ModerationLog


@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "content_type", "is_flagged", "confidence_score", "created_at")
    list_filter = ("content_type", "is_flagged", "created_at")
    search_fields = ("user_id", "submitted_content", "flag_reason")
    readonly_fields = ("created_at",)
