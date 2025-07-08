import os
import time
import whisper
import numpy as np
import wave

def test_direct_whisper():
    """Test Whisper with direct audio loading"""
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    print(f"Testing: {audio_file}")
    print(f"Size: {os.path.getsize(audio_file) / (1024*1024):.1f}MB")
    
    try:
        print("Loading model...")
        model = whisper.load_model('tiny')
        
        print("Loading audio directly...")
        # Load audio using Whisper's internal method
        audio = whisper.load_audio(audio_file)
        print(f"Audio loaded: {len(audio)} samples")
        
        print("Transcribing...")
        start = time.time()
        
        # Use the loaded audio directly
        result = model.transcribe(audio)
        end = time.time()
        
        print(f"✅ Success! Time: {end-start:.1f}s")
        print(f"Text: {result['text'][:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_whisper() 