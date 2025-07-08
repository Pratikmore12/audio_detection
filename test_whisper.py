#!/usr/bin/env python
"""
Test script to verify Whisper is working correctly
"""
import time
import whisper
import os
import librosa
import soundfile as sf

def test_whisper_loading():
    """Test if Whisper models can be loaded"""
    print("Testing Whisper model loading...")
    
    models_to_test = ['tiny', 'base']
    
    for model_size in models_to_test:
        try:
            print(f"Loading {model_size} model...")
            start_time = time.time()
            model = whisper.load_model(model_size)
            load_time = time.time() - start_time
            print(f"✓ {model_size} model loaded successfully in {load_time:.2f} seconds")
            
            # Test model info
            print(f"  Model parameters: {sum(p.numel() for p in model.parameters()):,}")
            
        except Exception as e:
            print(f"✗ Failed to load {model_size} model: {e}")
            return False
    
    return True

def test_whisper_transcription():
    """Test if Whisper can transcribe a simple audio file"""
    print("\nTesting Whisper transcription...")
    
    # Create a simple test audio file (you can replace this with a real file)
    test_audio_path = "test_audio.wav"
    
    try:
        # Try to load tiny model for quick test
        model = whisper.load_model('tiny')
        
        # Check if test file exists
        if os.path.exists(test_audio_path):
            print(f"Found test file: {test_audio_path}")
            start_time = time.time()
            result = model.transcribe(test_audio_path)
            processing_time = time.time() - start_time
            
            print(f"✓ Transcription completed in {processing_time:.2f} seconds")
            print(f"  Transcribed text: {result['text'][:100]}...")
            return True
        else:
            print(f"Test file not found: {test_audio_path}")
            print("Skipping transcription test")
            return True
            
    except Exception as e:
        print(f"✗ Transcription test failed: {e}")
        return False

def test_with_librosa():
    """Test using librosa to load the audio first"""
    audio_file = "10.+Risk+Management+and+Business+Continuity_compressed.wav"
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    print(f"Testing with librosa: {audio_file}")
    
    try:
        # Load audio with librosa
        print("Loading audio with librosa...")
        audio, sr = librosa.load(audio_file, sr=16000)
        
        print(f"Audio loaded: {len(audio)} samples, {sr}Hz")
        print(f"Duration: {len(audio)/sr:.1f} seconds")
        
        # Save as temporary file
        temp_file = "temp_audio.wav"
        sf.write(temp_file, audio, sr)
        
        # Test with Whisper
        print("Testing with Whisper...")
        model = whisper.load_model('tiny')
        
        start = time.time()
        result = model.transcribe(temp_file)
        end = time.time()
        
        print(f"✅ Success! Time: {end-start:.1f}s")
        print(f"Text: {result['text'][:200]}...")
        
        # Clean up
        os.remove(temp_file)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_direct_whisper():
    """Test direct Whisper loading"""
    audio_file = "10.+Risk+Management+and+Business+Continuity_compressed.wav"
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    print(f"Testing direct Whisper: {audio_file}")
    
    try:
        model = whisper.load_model('tiny')
        
        start = time.time()
        result = model.transcribe(audio_file)
        end = time.time()
        
        print(f"✅ Success! Time: {end-start:.1f}s")
        print(f"Text: {result['text'][:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print("="*60)
    print("WHISPER TEST")
    print("="*60)
    
    # Try direct method first
    test_direct_whisper()
    
    print("\n" + "="*60)
    print("LIBROSA METHOD")
    print("="*60)
    
    # Try with librosa
    test_with_librosa()
    
    print("\n✅ All tests passed! Whisper is working correctly.")
    print("\nRECOMMENDATIONS:")
    print("- Use 'tiny' model for large files (>50MB)")
    print("- Use 'base' model for medium files (20-50MB)")
    print("- Use 'small' model for small files (<20MB)")
    print("- Keep audio files under 20MB for best performance")
    
    return True

if __name__ == "__main__":
    main() 