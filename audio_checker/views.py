from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import os
import threading
import time
import logging

from .models import AudioAnalysis, WordComparison, AnalysisResult
from .forms import AudioAnalysisForm
from .services import AudioAnalyzer

logger = logging.getLogger(__name__)

def home(request):
    """Home page with upload form"""
    if request.method == 'POST':
        form = AudioAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            if request.user.is_authenticated:
                analysis.user = request.user
            analysis.save()
            
            # Start analysis in background with timeout
            thread = threading.Thread(target=run_analysis_with_timeout, args=(analysis.id,))
            thread.daemon = True
            thread.start()
            
            messages.success(request, 'Analysis started! You will be notified when it completes.')
            return redirect('audio_checker:analysis_detail', analysis_id=analysis.id)
    else:
        form = AudioAnalysisForm()
    
    return render(request, 'audio_checker/home.html', {'form': form})

def run_analysis_with_timeout(analysis_id):
    """Background task to run audio analysis with timeout and better error handling"""
    try:
        analysis = AudioAnalysis.objects.get(id=analysis_id)
        
        # Choose model size based on file size
        file_size = analysis.audio_file.size / (1024 * 1024)  # MB
        if file_size > 50:
            model_size = 'tiny'  # Use tiny model for large files
        elif file_size > 20:
            model_size = 'base'  # Use base model for medium files
        else:
            model_size = 'small'  # Use small model for small files
            
        logger.info(f"Starting analysis {analysis_id} with {model_size} model for {file_size:.1f}MB file")
        
        # Set a timeout for the entire analysis (30 minutes max)
        start_time = time.time()
        timeout = 1800  # 30 minutes
        
        try:
            analyzer = AudioAnalyzer(model_size=model_size)
            
            # Get file paths
            script_path = analysis.script_file.path
            audio_path = analysis.audio_file.path
            
            # EXTRA LOGGING
            logger.error(f"[DEBUG] Script path: {script_path} Exists: {os.path.exists(script_path)}")
            logger.error(f"[DEBUG] Audio path: {audio_path} Exists: {os.path.exists(audio_path)}")
            print(f"[DEBUG] Script path: {script_path} Exists: {os.path.exists(script_path)}")
            print(f"[DEBUG] Audio path: {audio_path} Exists: {os.path.exists(audio_path)}")
            
            # Check if files exist
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"Script file not found: {script_path}")
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            # Run analysis
            result = analyzer.analyze_audio_accuracy(script_path, audio_path)
            
            # Check timeout
            if time.time() - start_time > timeout:
                raise TimeoutError("Analysis timed out after 30 minutes")
            
            # Update analysis with results
            analysis.accuracy_score = result['statistics']['accuracy_score']
            analysis.total_words = result['statistics']['total_words']
            analysis.correct_words = result['statistics']['correct_words']
            analysis.missing_words = result['statistics']['missing_words']
            analysis.wrong_words = result['statistics']['wrong_words']
            analysis.save()
            
            # Create detailed result
            analysis_result, created = AnalysisResult.objects.get_or_create(
                analysis=analysis,
                defaults={
                    'transcribed_text': result['transcribed_text'],
                    'script_text': result['script_text'],
                    'processing_time': result['processing_time'],
                    'whisper_model_used': analyzer.model_size
                }
            )
            
            if not created:
                analysis_result.transcribed_text = result['transcribed_text']
                analysis_result.script_text = result['script_text']
                analysis_result.processing_time = result['processing_time']
                analysis_result.save()
            
            # Create word comparisons
            WordComparison.objects.filter(analysis=analysis).delete()
            for comp in result['comparisons']:
                WordComparison.objects.create(
                    analysis=analysis,
                    script_word=comp['script_word'],
                    audio_word=comp['audio_word'],
                    word_index=comp['word_index'],
                    is_correct=comp['is_correct'],
                    similarity_score=comp['similarity_score'],
                    error_type=comp['error_type']
                )
            
            logger.info(f"Analysis {analysis_id} completed successfully in {time.time() - start_time:.1f} seconds")
            
        except Exception as e:
            logger.error(f"Error in analysis {analysis_id}: {e}")
            # Mark analysis as failed
            analysis.accuracy_score = -1  # Use -1 to indicate failure
            analysis.save()
            raise
            
    except AudioAnalysis.DoesNotExist:
        logger.error(f"Analysis {analysis_id} not found")
    except Exception as e:
        logger.error(f"Critical error in analysis {analysis_id}: {e}")

def run_analysis(analysis_id):
    """Legacy function - now calls the timeout version"""
    run_analysis_with_timeout(analysis_id)

def analysis_detail(request, analysis_id):
    print("[DEBUG] analysis_detail called")
    analysis = get_object_or_404(AudioAnalysis, id=analysis_id)
    result = None
    try:
        result = analysis.analysisresult
        print(f"[DEBUG] AnalysisResult found: {result}")
    except Exception as e:
        print(f"[DEBUG] No AnalysisResult: {e}")
    mode = request.GET.get('mode', 'word')
    paragraph_results = None
    if mode == 'paragraph':
        analyzer = AudioAnalyzer()
        if result:
            print(f"[DEBUG] Using AnalysisResult for paragraph analysis")
            script_text = result.script_text
            audio_text = result.transcribed_text
        else:
            print(f"[DEBUG] Reconstructing script/audio text from WordComparison for paragraph analysis")
            comparisons = analysis.word_comparisons.all()
            script_text = ' '.join([c.script_word for c in comparisons if c.script_word])
            audio_text = ' '.join([c.audio_word for c in comparisons if c.audio_word])
        # Treat both as one paragraph
        paragraph_results = analyzer.compare_paragraphs(script_text, audio_text, script_path=None, force_single_paragraph=True)
    # Check if analysis failed
    if analysis.accuracy_score == -1:
        messages.error(request, 'Analysis failed. Please try again with a smaller file or different format.')
        return redirect('audio_checker:home')
    # Get word comparisons with pagination
    comparisons = analysis.word_comparisons.all()
    paginator = Paginator(comparisons, 50)  # 50 words per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'analysis': analysis,
        'page_obj': page_obj,
        'comparisons': page_obj,
        'mode': mode,
        'paragraph_results': paragraph_results,
    }
    return render(request, 'audio_checker/analysis_detail.html', context)

def analysis_list(request):
    """List all analyses"""
    analyses = AudioAnalysis.objects.all().order_by('-created_at')
    paginator = Paginator(analyses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'audio_checker/analysis_list.html', {'page_obj': page_obj})

@csrf_exempt
def check_analysis_status(request, analysis_id):
    """AJAX endpoint to check analysis status"""
    try:
        analysis = AudioAnalysis.objects.get(id=analysis_id)
        
        # Check if analysis failed
        if analysis.accuracy_score == -1:
            return JsonResponse({
                'status': 'failed',
                'error': 'Analysis failed. Please try again.'
            })
        
        return JsonResponse({
            'status': 'completed' if analysis.accuracy_score is not None else 'processing',
            'accuracy': analysis.accuracy_score,
            'total_words': analysis.total_words,
            'correct_words': analysis.correct_words,
            'missing_words': analysis.missing_words,
            'wrong_words': analysis.wrong_words,
        })
    except AudioAnalysis.DoesNotExist:
        return JsonResponse({'error': 'Analysis not found'}, status=404)

def download_results(request, analysis_id):
    """Download analysis results as CSV"""
    analysis = get_object_or_404(AudioAnalysis, id=analysis_id)
    
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="analysis_{analysis_id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Word Index', 'Script Word', 'Audio Word', 'Error Type', 'Similarity Score', 'Is Correct'])
    
    for comparison in analysis.word_comparisons.all():
        writer.writerow([
            comparison.word_index,
            comparison.script_word,
            comparison.audio_word,
            comparison.error_type,
            comparison.similarity_score,
            comparison.is_correct
        ])
    
    return response
