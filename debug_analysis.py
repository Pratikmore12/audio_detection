#!/usr/bin/env python
"""
Debug script to test analysis process step by step
"""
import os
import sys
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_detection.settings')
django.setup()

from audio_checker.models import AudioAnalysis
from audio_checker.services import AudioAnalyzer

def test_analysis_step_by_step(analysis_id):
    """Test analysis process step by step"""
    try:
        analysis = AudioAnalysis.objects.get(id=analysis_id)
        
        print(f"Testing analysis {analysis_id}: {analysis.title}")
        print("="*60)
        
        # Check file sizes
        if analysis.script_file:
            script_size = analysis.script_file.size / (1024 * 1024)
            print(f"Script file: {script_size:.1f}MB")
        else:
            print("❌ No script file")
            return False
            
        if analysis.audio_file:
            audio_size = analysis.audio_file.size / (1024 * 1024)
            print(f"Audio file: {audio_size:.1f}MB")
        else:
            print("❌ No audio file")
            return False
        
        # Check if files exist
        script_path = analysis.script_file.path
        audio_path = analysis.audio_file.path
        
        print(f"Script path: {script_path}")
        print(f"Audio path: {audio_path}")
        
        if not os.path.exists(script_path):
            print("❌ Script file not found")
            return False
            
        if not os.path.exists(audio_path):
            print("❌ Audio file not found")
            return False
        
        print("✅ Files exist")
        
        # Test script extraction
        print("\nTesting script extraction...")
        try:
            analyzer = AudioAnalyzer(model_size='tiny')
            script_text = analyzer.extract_text_from_docx(script_path)
            script_words = analyzer.preprocess_text(script_text)
            print(f"✅ Script extracted: {len(script_words)} words")
            print(f"Sample: {script_text[:100]}...")
        except Exception as e:
            print(f"❌ Script extraction failed: {e}")
            return False
        
        # Test audio transcription
        print("\nTesting audio transcription...")
        try:
            start_time = time.time()
            transcribed_text, processing_time = analyzer.transcribe_audio(audio_path)
            audio_words = analyzer.preprocess_text(transcribed_text)
            total_time = time.time() - start_time
            
            print(f"✅ Transcription completed in {total_time:.1f}s")
            print(f"Transcribed words: {len(audio_words)}")
            print(f"Sample: {transcribed_text[:100]}...")
            
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            return False
        
        # Test text alignment
        print("\nTesting text alignment...")
        try:
            comparisons = analyzer.align_texts(script_words, audio_words)
            print(f"✅ Alignment completed: {len(comparisons)} comparisons")
            
            # Calculate statistics
            total_words = len(script_words)
            correct_words = sum(1 for comp in comparisons if comp['is_correct'])
            missing_words = sum(1 for comp in comparisons if comp['error_type'] == 'missing')
            wrong_words = sum(1 for comp in comparisons if comp['error_type'] == 'wrong')
            
            accuracy = (correct_words / total_words * 100) if total_words > 0 else 0
            
            print(f"Total words: {total_words}")
            print(f"Correct: {correct_words}")
            print(f"Missing: {missing_words}")
            print(f"Wrong: {wrong_words}")
            print(f"Accuracy: {accuracy:.1f}%")
            
        except Exception as e:
            print(f"❌ Alignment failed: {e}")
            return False
        
        print("\n✅ All tests passed!")
        return True
        
    except AudioAnalysis.DoesNotExist:
        print(f"❌ Analysis {analysis_id} not found")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_quick_test():
    """Run a quick test with a small file"""
    print("="*60)
    print("QUICK TEST - Creating a test analysis")
    print("="*60)
    
    # Create a simple test
    try:
        from audio_checker.forms import AudioAnalysisForm
        
        # This would need actual files, but let's just test the analyzer
        analyzer = AudioAnalyzer(model_size='tiny')
        print("✅ Analyzer created successfully")
        
        # Test model loading
        print("Testing model loading...")
        model = analyzer.model
        print(f"✅ Model loaded: {analyzer.model_size}")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analysis_id = int(sys.argv[1])
        test_analysis_step_by_step(analysis_id)
    else:
        print("Usage: python debug_analysis.py <analysis_id>")
        print("Or run quick test without arguments")
        run_quick_test() 