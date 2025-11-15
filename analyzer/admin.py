from django.contrib import admin
from .models import Conversation, Message, AnalysisReport


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at']
    list_filter = ['created_at']
    ordering = ['-created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'timestamp', 'role', 'text_preview']
    list_filter = ['role', 'timestamp']
    search_fields = ['text']
    ordering = ['timestamp']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'


@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'session_count', 'questions_asked', 'actions_identified', 'created_at']
    list_filter = ['created_at']
    ordering = ['-created_at']
    readonly_fields = ['emotion_results']
