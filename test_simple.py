import whisper
import time

def test():
    try:
        print("Loading model...")
        model = whisper.load_model('tiny')
        
        print("Transcribing test_audio.wav...")
        start = time.time()
        result = model.transcribe("test_audio.wav")
        end = time.time()
        
        print(f"✅ Success! Time: {end-start:.1f}s")
        print(f"Text: {result['text'][:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test() 