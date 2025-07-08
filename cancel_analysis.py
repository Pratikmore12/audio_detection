#!/usr/bin/env python
"""
Script to cancel ongoing analysis and provide recommendations
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_detection.settings')
django.setup()

from audio_checker.models import AudioAnalysis

def cancel_analysis(analysis_id):
    """Cancel an ongoing analysis"""
    try:
        analysis = AudioAnalysis.objects.get(id=analysis_id)
        
        if analysis.accuracy_score is None:
            # Analysis is still processing
            print(f"Cancelling analysis {analysis_id}...")
            
            # Delete the analysis to stop processing
            analysis.delete()
            print("Analysis cancelled successfully!")
            
            return True
        else:
            print(f"Analysis {analysis_id} is already completed.")
            return False
            
    except AudioAnalysis.DoesNotExist:
        print(f"Analysis {analysis_id} not found.")
        return False

def show_recommendations():
    """Show recommendations for faster processing"""
    print("\n" + "="*50)
    print("RECOMMENDATIONS FOR FASTER PROCESSING")
    print("="*50)
    print("1. Use smaller audio files (under 20MB)")
    print("2. Convert audio to WAV format for better compatibility")
    print("3. Use shorter audio clips (under 10 minutes)")
    print("4. The system now automatically uses 'tiny' model for large files")
    print("5. Estimated processing times:")
    print("   - Tiny model: ~2 seconds per minute of audio")
    print("   - Base model: ~4 seconds per minute of audio")
    print("   - Small model: ~8 seconds per minute of audio")
    print("\nFor a 70MB file (~30-40 minutes):")
    print("   - Tiny model: ~60-80 seconds")
    print("   - Base model: ~120-160 seconds")
    print("   - Small model: ~240-320 seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analysis_id = int(sys.argv[1])
        cancel_analysis(analysis_id)
    else:
        print("Usage: python cancel_analysis.py <analysis_id>")
        print("Example: python cancel_analysis.py 2")
    
    show_recommendations() 