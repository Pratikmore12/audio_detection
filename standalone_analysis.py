#!/usr/bin/env python
"""
Standalone Audio Analysis - No FFmpeg Required
"""
import os
import sys
import time
import wave
import numpy as np
import whisper
from docx import Document
from fuzzywuzzy import fuzz
import re

def load_audio_without_ffmpeg(audio_path):
    """Load audio using only Python libraries"""
    try:
        # Try to load as WAV file directly
        with wave.open(audio_path, 'rb') as wav_file:
            # Get audio parameters
            frames = wav_file.getnframes()
            sample_rate = wav_file.getframerate()
            duration = frames / sample_rate
            
            # Read audio data
            audio_data = wav_file.readframes(frames)
            
            # Convert to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Normalize to float32
            audio_float = audio_array.astype(np.float32) / 32768.0
            
            print(f"✅ Loaded audio: {duration:.1f}s, {sample_rate}Hz")
            return audio_float, sample_rate
            
    except Exception as e:
        print(f"❌ Error loading WAV: {e}")
        return None, None

def transcribe_with_whisper(audio_path):
    """Transcribe audio using Whisper with custom audio loading"""
    try:
        print("Loading Whisper model...")
        model = whisper.load_model('tiny')
        
        print("Loading audio...")
        audio, sr = load_audio_without_ffmpeg(audio_path)
        
        if audio is None:
            print("❌ Could not load audio")
            return None
        
        print("Transcribing...")
        start_time = time.time()
        
        # Use Whisper's internal audio processing
        result = model.transcribe(
            audio_path,
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
        return transcribed_text, processing_time
        
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return None, 0

def extract_text_from_docx(docx_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(docx_path)
        text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text.strip())
        return ' '.join(text)
    except Exception as e:
        print(f"❌ Error extracting text from DOCX: {e}")
        return None

def preprocess_text(text):
    """Clean and tokenize text"""
    text = re.sub(r'\s+', ' ', text.lower().strip())
    text = re.sub(r'[^\w\s\']', '', text)
    words = text.split()
    return words

def align_texts(script_words, audio_words):
    """Align script and audio words"""
    comparisons = []
    script_idx = 0
    audio_idx = 0
    
    while script_idx < len(script_words) or audio_idx < len(audio_words):
        script_word = script_words[script_idx] if script_idx < len(script_words) else ""
        audio_word = audio_words[audio_idx] if audio_idx < len(audio_words) else ""
        
        if script_idx < len(script_words) and audio_idx < len(audio_words):
            similarity = fuzz.ratio(script_word.lower(), audio_word.lower())
            
            if similarity >= 80:
                comparisons.append({
                    'script_word': script_word,
                    'audio_word': audio_word,
                    'word_index': script_idx,
                    'is_correct': True,
                    'similarity_score': similarity,
                    'error_type': 'correct'
                })
                script_idx += 1
                audio_idx += 1
            else:
                comparisons.append({
                    'script_word': script_word,
                    'audio_word': audio_word,
                    'word_index': script_idx,
                    'is_correct': False,
                    'similarity_score': similarity,
                    'error_type': 'wrong'
                })
                script_idx += 1
                audio_idx += 1
        
        elif script_idx < len(script_words):
            comparisons.append({
                'script_word': script_word,
                'audio_word': '',
                'word_index': script_idx,
                'is_correct': False,
                'similarity_score': 0,
                'error_type': 'missing'
            })
            script_idx += 1
        
        else:
            comparisons.append({
                'script_word': '',
                'audio_word': audio_word,
                'word_index': audio_idx,
                'is_correct': False,
                'similarity_score': 0,
                'error_type': 'extra'
            })
            audio_idx += 1
    
    return comparisons

def analyze_audio_accuracy(script_path, audio_path):
    """Main analysis function"""
    print("="*60)
    print("STANDALONE AUDIO ACCURACY ANALYSIS")
    print("="*60)
    
    # Check files
    if not os.path.exists(script_path):
        print(f"❌ Script file not found: {script_path}")
        return None
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return None
    
    # Get file info
    script_size = os.path.getsize(script_path) / (1024 * 1024)
    audio_size = os.path.getsize(audio_path) / (1024 * 1024)
    
    print(f"Script: {script_size:.1f}MB")
    print(f"Audio: {audio_size:.1f}MB")
    
    # Extract script text
    print("\nExtracting script text...")
    script_text = extract_text_from_docx(script_path)
    if not script_text:
        return None
    
    script_words = preprocess_text(script_text)
    print(f"Script words: {len(script_words)}")
    
    # Transcribe audio
    print("\nTranscribing audio...")
    transcribed_text, processing_time = transcribe_with_whisper(audio_path)
    if not transcribed_text:
        return None
    
    audio_words = preprocess_text(transcribed_text)
    print(f"Audio words: {len(audio_words)}")
    
    # Align texts
    print("\nAligning texts...")
    comparisons = align_texts(script_words, audio_words)
    
    # Calculate statistics
    total_words = len(script_words)
    correct_words = sum(1 for comp in comparisons if comp['is_correct'])
    missing_words = sum(1 for comp in comparisons if comp['error_type'] == 'missing')
    wrong_words = sum(1 for comp in comparisons if comp['error_type'] == 'wrong')
    
    accuracy_score = (correct_words / total_words * 100) if total_words > 0 else 0
    
    # Display results
    print("\n" + "="*60)
    print("ANALYSIS RESULTS")
    print("="*60)
    print(f"Overall Accuracy: {accuracy_score:.1f}%")
    print(f"Total Words: {total_words}")
    print(f"Correct Words: {correct_words}")
    print(f"Missing Words: {missing_words}")
    print(f"Wrong Words: {wrong_words}")
    print(f"Processing Time: {processing_time:.1f} seconds")
    
    # Show sample comparisons
    print("\nSample Word Comparisons:")
    print("-" * 60)
    for i, comp in enumerate(comparisons[:20]):
        status = "✅" if comp['is_correct'] else "❌"
        print(f"{i+1:2d}. {status} Script: '{comp['script_word']}' | Audio: '{comp['audio_word']}' | Type: {comp['error_type']}")
    
    if len(comparisons) > 20:
        print(f"... and {len(comparisons) - 20} more comparisons")
    
    return {
        'accuracy_score': accuracy_score,
        'total_words': total_words,
        'correct_words': correct_words,
        'missing_words': missing_words,
        'wrong_words': wrong_words,
        'comparisons': comparisons,
        'script_text': script_text,
        'transcribed_text': transcribed_text,
        'processing_time': processing_time
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python standalone_analysis.py <script.docx> <audio.wav>")
        print("\nExample:")
        print("  python standalone_analysis.py script.docx test_audio.wav")
        sys.exit(1)
    
    script_path = sys.argv[1]
    audio_path = sys.argv[2]
    
    result = analyze_audio_accuracy(script_path, audio_path)
    
    if result:
        print("\n✅ Analysis completed successfully!")
        print(f"📊 Accuracy: {result['accuracy_score']:.1f}%")
        print(f"⏱️  Processing time: {result['processing_time']:.1f} seconds")
    else:
        print("\n❌ Analysis failed!") 