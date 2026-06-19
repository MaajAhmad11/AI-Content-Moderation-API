from rest_framework import serializers
from .models import ModerationLog

class TextModerationRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, help_text="Unique ID of the user submitting content")
    text = serializers.CharField(min_length=1, help_text="The text message payload to look into")

class ImageModerationRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, help_text="Unique ID of the user submitting content")
    image_url = serializers.URLField(help_text="The clear public URL of the image asset")

class ModerationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationLog
        fields = ['id', 'user_id', 'content_type', 'is_flagged', 'flag_reason', 'confidence_score', 'created_at']