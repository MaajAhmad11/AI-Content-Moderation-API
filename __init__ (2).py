from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    TextModerationRequestSerializer,
    ImageModerationRequestSerializer,
    ModerationResponseSerializer,
)
from .utils import analyze_text_content, analyze_image_content
from .models import ModerationLog


class TextModerationView(APIView):
    # Public endpoint: no auth, so browser fetch() works without CSRF tokens.
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=TextModerationRequestSerializer,
        responses={200: ModerationResponseSerializer()},
    )
    def post(self, request):
        serializer = TextModerationRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            text = serializer.validated_data["text"]

            # Evaluate text via rules engine
            ai_result = analyze_text_content(text)

            # Record audit metrics
            log = ModerationLog.objects.create(
                user_id=user_id,
                content_type="text",
                submitted_content=text,
                is_flagged=ai_result["is_flagged"],
                flag_reason=ai_result["flag_reason"],
                confidence_score=ai_result["confidence_score"],
            )

            return Response(ModerationResponseSerializer(log).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageModerationView(APIView):
    # Public endpoint: no auth, so browser fetch() works without CSRF tokens.
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=ImageModerationRequestSerializer,
        responses={200: ModerationResponseSerializer()},
    )
    def post(self, request):
        serializer = ImageModerationRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            image_url = serializer.validated_data["image_url"]

            # Evaluate graphic url structure
            ai_result = analyze_image_content(image_url)

            # Record audit metrics
            log = ModerationLog.objects.create(
                user_id=user_id,
                content_type="image",
                submitted_content=image_url,
                is_flagged=ai_result["is_flagged"],
                flag_reason=ai_result["flag_reason"],
                confidence_score=ai_result["confidence_score"],
            )

            return Response(ModerationResponseSerializer(log).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Frontend ---------------------------------------------------------------
from django.shortcuts import render


def home(request):
    """Serve the moderation console frontend."""
    return render(request, "index.html")
