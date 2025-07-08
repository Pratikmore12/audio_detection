import whisper
import time
import os

def test():
    try:
        # Get absolute path
        current_dir = os.getcwd()
        audio_path = os.path.join(current_dir, "test_audio.wav")
        
        print(f"Current directory: {current_dir}")
        print(f"Audio path: {audio_path}")
        print(f"File exists: {os.path.exists(audio_path)}")
        
        print("Loading model...")
        model = whisper.load_model('tiny')
        
        print("Transcribing...")
        start = time.time()
        result = model.transcribe(audio_path)
        end = time.time()
        
        print(f"✅ Success! Time: {end-start:.1f}s")
        print(f"Text: {result['text'][:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test() 