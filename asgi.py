from django.urls import path
from .views import TextModerationView, ImageModerationView

urlpatterns = [
    path('moderate/text/', TextModerationView.as_view(), name='moderate-text'),
    path('moderate/image/', ImageModerationView.as_view(), name='moderate-image'),
]