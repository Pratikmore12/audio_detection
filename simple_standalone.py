import os
import time
import whisper
from docx import Document

def test_audio():
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    print(f"Testing: {audio_file}")
    print(f"Size: {os.path.getsize(audio_file) / (1024*1024):.1f}MB")
    
    try:
        print("Loading model...")
        model = whisper.load_model('tiny')
        
        print("Transcribing...")
        start = time.time()
        result = model.transcribe(audio_file)
        end = time.time()
        
        print(f"✅ Success! Time: {end-start:.1f}s")
        print(f"Text: {result['text'][:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_audio() 