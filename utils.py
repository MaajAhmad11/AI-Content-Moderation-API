from django.db import models


class ModerationLog(models.Model):
    CONTENT_TYPES = (
        ("text", "Text"),
        ("image", "Image"),
    )

    user_id = models.CharField(max_length=100)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    submitted_content = models.TextField()
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.CharField(max_length=255, blank=True, null=True)
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_type.upper()} - Flagged: {self.is_flagged} ({self.user_id})"
