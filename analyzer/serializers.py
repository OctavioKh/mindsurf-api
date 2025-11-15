from rest_framework import serializers
from .models import Conversation, Message, AnalysisReport


class MessageSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    role = serializers.ChoiceField(choices=['user', 'assistant'])
    text = serializers.CharField()


class TranscriptRequestSerializer(serializers.Serializer):
    transcript = MessageSerializer(many=True)
    
    def validate_transcript(self, value):
        if not value:
            raise serializers.ValidationError("Transcript cannot be empty")
        return value


class AnalysisResponseSerializer(serializers.Serializer):
    analysis_summary = serializers.JSONField()
