#!/usr/bin/env python
"""
Test the complete analysis process
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_detection.settings')
django.setup()

from audio_checker.services import AudioAnalyzer

def test_complete_analysis():
    """Test the complete analysis process"""
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    print(f"Testing complete analysis with: {audio_file}")
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
        
        # Test text processing
        print("\nTesting text processing...")
        audio_words = analyzer.preprocess_text(transcribed_text)
        print(f"✅ Processed {len(audio_words)} words")
        
        # Create a test script
        test_script = """
        Lesson 10. Risk management and business continuity. 
        Unexpected disruptions can shut down operations in minutes, 
        but recovering from them can take weeks or months. 
        This lesson will teach you how to identify and manage risks.
        """
        
        script_words = analyzer.preprocess_text(test_script)
        print(f"✅ Script processed: {len(script_words)} words")
        
        # Test alignment
        print("\nTesting text alignment...")
        comparisons = analyzer.align_texts(script_words, audio_words)
        
        # Calculate accuracy
        total_words = len(script_words)
        correct_words = sum(1 for comp in comparisons if comp['is_correct'])
        accuracy = (correct_words / total_words * 100) if total_words > 0 else 0
        
        print(f"✅ Alignment completed!")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"Total words: {total_words}")
        print(f"Correct words: {correct_words}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_analysis()
    if success:
        print("\n🎉 SUCCESS! The complete analysis system is working!")
        print("You can now use the web interface at http://127.0.0.1:8000/")
        print("Upload your compressed file and a matching DOCX script for analysis.")
    else:
        print("\n❌ The analysis system still has issues.") 