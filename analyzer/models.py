from django.db import models


class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Conversation {self.id} - {self.created_at}"


class Message(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    timestamp = models.DateTimeField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    text = models.TextField()
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.role}: {self.text[:50]}"


class AnalysisReport(models.Model):
    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        related_name='report'
    )
    session_count = models.IntegerField()
    questions_asked = models.IntegerField()
    actions_identified = models.IntegerField()
    emotion_results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report for Conversation {self.conversation.id}"
    
    def to_dict(self):
        return {
            "analysis_summary": {
                "session_count": self.session_count,
                "key_moments": {
                    "questions_asked": self.questions_asked,
                    "actions_identified": self.actions_identified
                },
                "emotion_analysis_results": self.emotion_results
            }
        }
