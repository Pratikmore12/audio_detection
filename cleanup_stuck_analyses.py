#!/usr/bin/env python
"""
Script to clean up stuck analyses and provide recommendations
"""
import os
import sys
import django
from datetime import timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_detection.settings')
django.setup()

from audio_checker.models import AudioAnalysis
from django.utils import timezone

def cleanup_stuck_analyses():
    """Clean up analyses that have been processing for too long"""
    # Find analyses that have been processing for more than 20 minutes
    cutoff_time = timezone.now() - timedelta(minutes=20)
    stuck_analyses = AudioAnalysis.objects.filter(
        accuracy_score__isnull=True,
        created_at__lt=cutoff_time
    )
    
    print(f"Found {stuck_analyses.count()} stuck analyses:")
    print("="*60)
    
    for analysis in stuck_analyses:
        duration = timezone.now() - analysis.created_at
        file_size = analysis.audio_file.size / (1024 * 1024) if analysis.audio_file else 0
        
        print(f"ID: {analysis.id}")
        print(f"Title: {analysis.title}")
        print(f"Duration: {duration}")
        print(f"File Size: {file_size:.1f} MB")
        
        # Delete the stuck analysis
        analysis.delete()
        print(f"✓ Deleted stuck analysis {analysis.id}")
        print("-" * 40)
    
    if stuck_analyses.count() == 0:
        print("No stuck analyses found!")

def show_performance_tips():
    """Show performance optimization tips"""
    print("\n" + "="*60)
    print("PERFORMANCE OPTIMIZATION TIPS")
    print("="*60)
    print("1. FILE SIZE RECOMMENDATIONS:")
    print("   • Optimal: < 20MB (5-10 minutes of audio)")
    print("   • Acceptable: 20-50MB (10-25 minutes)")
    print("   • Avoid: > 50MB (will use tiny model, lower accuracy)")
    print()
    print("2. AUDIO FORMAT RECOMMENDATIONS:")
    print("   • Best: WAV (uncompressed, fastest processing)")
    print("   • Good: MP3 (compressed, slower but smaller)")
    print("   • Avoid: M4A, FLAC (may cause compatibility issues)")
    print()
    print("3. EXPECTED PROCESSING TIMES:")
    print("   • Tiny model: ~2 seconds per minute of audio")
    print("   • Base model: ~4 seconds per minute of audio")
    print("   • Small model: ~8 seconds per minute of audio")
    print()
    print("4. FOR LARGE FILES (>50MB):")
    print("   • Split into smaller chunks (10-15 minutes each)")
    print("   • Use audio editing software to cut files")
    print("   • Consider using online tools to compress audio")
    print()
    print("5. TROUBLESHOOTING:")
    print("   • If processing takes >30 minutes, cancel and retry")
    print("   • Check file format compatibility")
    print("   • Ensure stable internet connection (for model download)")
    print("   • Close other applications to free up memory")

def check_system_resources():
    """Check system resources"""
    import psutil
    
    print("\n" + "="*60)
    print("SYSTEM RESOURCES")
    print("="*60)
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_percent}%")
    
    # Memory
    memory = psutil.virtual_memory()
    print(f"Memory Usage: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)")
    
    # Disk
    disk = psutil.disk_usage('/')
    print(f"Disk Usage: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")
    
    # Recommendations
    if memory.percent > 80:
        print("⚠️  High memory usage - close other applications")
    if cpu_percent > 80:
        print("⚠️  High CPU usage - wait for other processes to finish")
    if disk.percent > 90:
        print("⚠️  Low disk space - free up space")

if __name__ == "__main__":
    try:
        cleanup_stuck_analyses()
        show_performance_tips()
        check_system_resources()
    except ImportError:
        print("psutil not available - skipping system resource check")
        cleanup_stuck_analyses()
        show_performance_tips() 