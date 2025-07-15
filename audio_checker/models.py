from django.db import models
from django.contrib.auth.models import User
import os

class BatchUpload(models.Model):
    """Model to handle batch uploads of multiple script-audio pairs"""
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    
    def __str__(self):
        return f"Batch: {self.title}"
    
    def get_total_analyses(self):
        return self.analyses.count()
    
    def get_completed_analyses(self):
        return self.analyses.filter(accuracy_score__isnull=False).exclude(accuracy_score=-1).count()
    
    def get_failed_analyses(self):
        return self.analyses.filter(accuracy_score=-1).count()

class AudioAnalysis(models.Model):
    title = models.CharField(max_length=200)
    script_file = models.FileField(upload_to='scripts/')
    audio_file = models.FileField(upload_to='audio/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.ForeignKey(BatchUpload, on_delete=models.CASCADE, related_name='analyses', null=True, blank=True)
    
    # Analysis results
    accuracy_score = models.FloatField(null=True, blank=True)
    total_words = models.IntegerField(default=0)
    correct_words = models.IntegerField(default=0)
    missing_words = models.IntegerField(default=0)
    wrong_words = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def get_accuracy_percentage(self):
        if self.total_words > 0:
            return (self.correct_words / self.total_words) * 100
        return 0

class WordComparison(models.Model):
    analysis = models.ForeignKey(AudioAnalysis, on_delete=models.CASCADE, related_name='word_comparisons')
    script_word = models.CharField(max_length=100)
    audio_word = models.CharField(max_length=100)
    word_index = models.IntegerField()
    is_correct = models.BooleanField(default=False)
    similarity_score = models.FloatField(default=0.0)
    error_type = models.CharField(max_length=20, choices=[
        ('correct', 'Correct'),
        ('missing', 'Missing'),
        ('wrong', 'Wrong'),
        ('extra', 'Extra'),
    ], default='correct')
    
    class Meta:
        ordering = ['word_index']

class AnalysisResult(models.Model):
    analysis = models.OneToOneField(AudioAnalysis, on_delete=models.CASCADE, related_name='detailed_result')
    transcribed_text = models.TextField()
    script_text = models.TextField()
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    whisper_model_used = models.CharField(max_length=32, null=True, blank=True)
    segments = models.JSONField(null=True, blank=True)  # Store Whisper segments
    
    def __str__(self):
        return f"Result for {self.analysis.title}"
