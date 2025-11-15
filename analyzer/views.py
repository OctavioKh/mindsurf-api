from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Conversation, Message, AnalysisReport
from .serializers import TranscriptRequestSerializer
from .analysis import TranscriptAnalyzer


class AnalyzeTranscriptView(APIView):
    """
    POST /api/analyze/
    Receives a transcript, stores it, analyzes it, and returns a report
    """
    
    def post(self, request):
        serializer = TranscriptRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transcript_data = serializer.validated_data['transcript']
        
        try:
            with transaction.atomic():
                # Create conversation
                conversation = Conversation.objects.create()
                
                # Create messages
                for msg_data in transcript_data:
                    Message.objects.create(
                        conversation=conversation,
                        timestamp=msg_data['timestamp'],
                        role=msg_data['role'],
                        text=msg_data['text']
                    )
                
                # Analyze transcript
                analyzer = TranscriptAnalyzer(transcript_data)
                analysis_results = analyzer.analyze()
                
                # Save report
                report = AnalysisReport.objects.create(
                    conversation=conversation,
                    session_count=analysis_results['session_count'],
                    questions_asked=analysis_results['key_moments']['questions_asked'],
                    actions_identified=analysis_results['key_moments']['actions_identified'],
                    emotion_results=analysis_results['emotion_analysis_results']
                )
                
                return Response(
                    report.to_dict(),
                    status=status.HTTP_201_CREATED
                )
        
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
