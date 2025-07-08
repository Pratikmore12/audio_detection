#!/usr/bin/env python
"""
Delete failed analyses
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_detection.settings')
django.setup()

from audio_checker.models import AudioAnalysis

def delete_failed_analyses():
    """Delete analyses that failed (accuracy = -1)"""
    failed_analyses = AudioAnalysis.objects.filter(accuracy_score=-1)
    
    print(f"Found {failed_analyses.count()} failed analyses:")
    print("="*50)
    
    for analysis in failed_analyses:
        print(f"ID: {analysis.id}")
        print(f"Title: {analysis.title}")
        try:
            file_size = analysis.audio_file.size / (1024 * 1024)
        except FileNotFoundError:
            print(f"File not found, deleting analysis {analysis.id}: {analysis.audio_file.name}")
            analysis.delete()
            continue
        if analysis.audio_file:
            print(f"File Size: {file_size:.1f} MB")
        
        # Delete the failed analysis
        analysis.delete()
        print(f"✓ Deleted failed analysis {analysis.id}")
        print("-" * 30)
    
    if failed_analyses.count() == 0:
        print("No failed analyses found!")

if __name__ == "__main__":
    delete_failed_analyses() 