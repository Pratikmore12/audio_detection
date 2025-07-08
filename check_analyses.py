#!/usr/bin/env python
"""
Script to check current analysis status
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_detection.settings')
django.setup()

from audio_checker.models import AudioAnalysis
from django.utils import timezone

def check_analyses():
    """Check all analyses in the database"""
    analyses = AudioAnalysis.objects.all().order_by('-created_at')
    
    print(f"Found {analyses.count()} analyses:")
    print("="*80)
    
    for analysis in analyses:
        status = "Completed" if analysis.accuracy_score is not None else "Processing"
        duration = timezone.now() - analysis.created_at
        
        print(f"ID: {analysis.id}")
        print(f"Title: {analysis.title}")
        print(f"Status: {status}")
        print(f"Created: {analysis.created_at}")
        print(f"Duration: {duration}")
        
        if analysis.accuracy_score is not None:
            print(f"Accuracy: {analysis.accuracy_score:.1f}%")
            print(f"Total Words: {analysis.total_words}")
            print(f"Correct Words: {analysis.correct_words}")
        else:
            print("Still processing...")
        
        if analysis.audio_file:
            file_size = analysis.audio_file.size / (1024 * 1024)
            print(f"Audio File Size: {file_size:.1f} MB")
        
        print("-" * 40)

if __name__ == "__main__":
    check_analyses() 