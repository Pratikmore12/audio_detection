from django.contrib import admin
from .models import AudioAnalysis, WordComparison, AnalysisResult, BatchUpload

@admin.register(AudioAnalysis)
class AudioAnalysisAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'accuracy_score', 'total_words', 'correct_words', 'created_at']
    list_filter = ['created_at', 'accuracy_score']
    search_fields = ['title', 'user__username']
    readonly_fields = ['accuracy_score', 'total_words', 'correct_words', 'missing_words', 'wrong_words']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(WordComparison)
class WordComparisonAdmin(admin.ModelAdmin):
    list_display = ['analysis', 'script_word', 'audio_word', 'error_type', 'similarity_score', 'word_index']
    list_filter = ['error_type', 'is_correct']
    search_fields = ['script_word', 'audio_word', 'analysis__title']
    readonly_fields = ['similarity_score']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('analysis')

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['analysis', 'processing_time', 'whisper_model_used']
    readonly_fields = ['processing_time', 'whisper_model_used']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('analysis')

@admin.register(BatchUpload)
class BatchUploadAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_at', 'get_total_analyses', 'get_completed_analyses']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
