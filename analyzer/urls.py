from django.urls import path
from .views import AnalyzeTranscriptView

urlpatterns = [
    path('analyze/', AnalyzeTranscriptView.as_view(), name='analyze-transcript'),
]
