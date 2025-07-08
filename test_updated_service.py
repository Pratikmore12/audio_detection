 #!/usr/bin/env python
"""
Test the updated audio service
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_detection.settings')
django.setup()

from audio_checker.services import AudioAnalyzer

def test_updated_service():
    """Test the updated audio service"""
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    print(f"Testing updated service with: {audio_file}")
    print(f"File size: {os.path.getsize(audio_file) / (1024*1024):.1f}MB")
    
    try:
        # Create analyzer
        analyzer = AudioAnalyzer(model_size='tiny')
        print("✅ Analyzer created")
        
        # Test transcription
        print("Transcribing audio...")
        transcribed_text, processing_time = analyzer.transcribe_audio(audio_file)
        
        print(f"✅ Transcription successful!")
        print(f"Processing time: {processing_time:.1f} seconds")
        print(f"Text length: {len(transcribed_text)} characters")
        print(f"Sample text: {transcribed_text[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_updated_service()
    if success:
        print("\n🎉 SUCCESS! The updated service works!")
        print("You can now use the web interface with your compressed file.")
    else:
        print("\n❌ The service still has issues.")