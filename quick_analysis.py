#!/usr/bin/env python
"""
Standalone audio analysis script
"""
import os
import sys
import time
import whisper
from docx import Document
from fuzzywuzzy import fuzz
import re

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
        print(f"Error extracting text from DOCX: {e}")
        return None

def preprocess_text(text):
    """Clean and tokenize text"""
    text = re.sub(r'\s+', ' ', text.lower().strip())
    text = re.sub(r'[^\w\s\']', '', text)
    words = text.split()
    return words

def calculate_similarity(word1, word2):
    """Calculate similarity between words"""
    return fuzz.ratio(word1.lower(), word2.lower())

def align_texts(script_words, audio_words):
    """Align script and audio words"""
    comparisons = []
    script_idx = 0
    audio_idx = 0
    
    while script_idx < len(script_words) or audio_idx < len(audio_words):
        script_word = script_words[script_idx] if script_idx < len(script_words) else ""
        audio_word = audio_words[audio_idx] if audio_idx < len(audio_words) else ""
        
        if script_idx < len(script_words) and audio_idx < len(audio_words):
            similarity = calculate_similarity(script_word, audio_word)
            
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
                if script_idx + 1 < len(script_words):
                    next_similarity = calculate_similarity(script_words[script_idx + 1], audio_word)
                    if next_similarity >= 80:
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
                            'script_word': script_word,
                            'audio_word': audio_word,
                            'word_index': script_idx,
                            'is_correct': False,
                            'similarity_score': similarity,
                            'error_type': 'wrong'
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
    print("AUDIO ACCURACY ANALYSIS")
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
    try:
        start_time = time.time()
        
        model = whisper.load_model('tiny')
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
        audio_words = preprocess_text(transcribed_text)
        
        print(f"✅ Transcription completed in {processing_time:.1f} seconds")
        print(f"Audio words: {len(audio_words)}")
        
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return None
    
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
    
    # Show sample comparisons
    print("\nSample Word Comparisons:")
    print("-" * 60)
    for i, comp in enumerate(comparisons[:20]):  # Show first 20
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
        'transcribed_text': transcribed_text
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python quick_analysis.py <script.docx> <audio.wav>")
        print("\nExample:")
        print("  python quick_analysis.py script.docx 10.+Risk+Management+and+Business+Continuity_compressed.wav")
        sys.exit(1)
    
    script_path = sys.argv[1]
    audio_path = sys.argv[2]
    
    result = analyze_audio_accuracy(script_path, audio_path)
    
    if result:
        print("\n✅ Analysis completed successfully!")
        print(f"📊 Accuracy: {result['accuracy_score']:.1f}%")
    else:
        print("\n❌ Analysis failed!") 