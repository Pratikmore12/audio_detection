import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_detection.settings')
django.setup()

from audio_checker.models import AudioAnalysis, AnalysisResult

# Check recent analyses
recent_analyses = AudioAnalysis.objects.all().order_by('-id')[:5]

for a in recent_analyses:
    print(f"\n=== Analysis ID: {a.id} ===")
    print(f"Title: {a.title}")
    print(f"Audio file: {a.audio_file}")
    print(f"Audio exists: {os.path.exists(a.audio_file.path) if a.audio_file else False}")
    print(f"Accuracy score: {a.accuracy_score}")
    
    try:
        r = a.detailed_result
        print(f"AnalysisResult exists: {r is not None}")
        if r and r.segments:
            print(f"Segments count: {len(r.segments)}")
            print(f"First segment: {r.segments[0] if r.segments else 'None'}")
        else:
            print("No segments in AnalysisResult")
    except Exception as e:
        print(f"No AnalysisResult: {e}")
        
    print("-" * 50) 