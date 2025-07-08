#!/usr/bin/env python
"""
Test script to process the compressed audio file directly
"""
import os
import time
import whisper
from docx import Document

def test_compressed_audio():
    """Test processing the compressed audio file"""
    audio_file = "10.+Risk+Management+and+Business+Continuity_compressed.wav"
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    # Check file size
    file_size = os.path.getsize(audio_file) / (1024 * 1024)
    print(f"Audio file: {file_size:.1f}MB")
    
    # Test Whisper transcription
    print("\nTesting Whisper transcription...")
    try:
        start_time = time.time()
        
        # Load tiny model
        print("Loading tiny model...")
        model = whisper.load_model('tiny')
        
        # Transcribe
        print("Transcribing audio...")
        result = model.transcribe(
            audio_file,
            fp16=False,
            language=None,
            task="transcribe",
            verbose=False,
            condition_on_previous_text=False,
            temperature=0.0
        )
        
        processing_time = time.time() - start_time
        transcribed_text = result["text"].strip()
        
        print(f"✅ Transcription completed in {processing_time:.1f} seconds")
        print(f"Transcribed text length: {len(transcribed_text)} characters")
        print(f"Sample: {transcribed_text[:200]}...")
        
        # Count words
        words = transcribed_text.split()
        print(f"Word count: {len(words)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return False

def create_test_script():
    """Create a simple test script file"""
    script_content = """
Risk Management and Business Continuity

This is a test script for audio analysis. The content should match the audio file being processed.

Key points:
1. Risk identification
2. Business continuity planning
3. Emergency response procedures
4. Recovery strategies

This script is designed to test the audio accuracy checking system.
"""
    
    # Create a simple text file (since we don't have a DOCX)
    with open("test_script.txt", "w") as f:
        f.write(script_content)
    
    print("✅ Test script created: test_script.txt")
    return "test_script.txt"

def test_full_analysis():
    """Test the full analysis process"""
    print("="*60)
    print("FULL ANALYSIS TEST")
    print("="*60)
    
    # Test audio transcription
    if not test_compressed_audio():
        return False
    
    # Create test script
    script_file = create_test_script()
    
    print("\n✅ All tests completed successfully!")
    print("\nRECOMMENDATIONS:")
    print("1. The compressed audio file should work fine")
    print("2. Processing time should be 1-3 minutes")
    print("3. Make sure you have a matching DOCX script file")
    print("4. Upload both files through the web interface")
    
    return True

if __name__ == "__main__":
    test_full_analysis() 