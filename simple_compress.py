#!/usr/bin/env python
"""
Simple audio compression using librosa
"""
import os
import librosa
import soundfile as sf
import numpy as np

def compress_audio_simple(input_path, output_path=None, target_size_mb=20):
    """Compress audio using librosa"""
    try:
        print(f"Loading audio file: {input_path}")
        
        # Load audio
        y, sr = librosa.load(input_path, sr=None)
        
        # Get original info
        original_duration = len(y) / sr
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        
        print(f"Original: {original_duration:.1f}s, {original_size:.1f}MB")
        
        if original_size <= target_size_mb:
            print(f"File is already under {target_size_mb}MB")
            return input_path
        
        # Calculate target sample rate
        target_size_bytes = target_size_mb * 1024 * 1024
        target_sr = int((target_size_bytes * sr) / (len(y) * 2))  # 16-bit audio
        
        # Ensure minimum quality
        target_sr = max(target_sr, 8000)  # Minimum 8kHz
        
        print(f"Resampling to {target_sr}Hz...")
        
        # Resample
        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
        
        # Generate output path
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_compressed{ext}"
        
        # Save compressed audio
        sf.write(output_path, y_resampled, target_sr)
        
        # Check final size
        final_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Compressed: {final_size:.1f}MB")
        print(f"Saved to: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def split_audio_simple(input_path, output_dir=None, segment_duration=600):
    """Split audio into segments"""
    try:
        print(f"Loading audio file: {input_path}")
        
        # Load audio
        y, sr = librosa.load(input_path, sr=None)
        
        total_duration = len(y) / sr
        segment_samples = int(segment_duration * sr)
        num_segments = int(np.ceil(len(y) / segment_samples))
        
        print(f"Total duration: {total_duration:.1f}s")
        print(f"Splitting into {num_segments} segments of {segment_duration}s each")
        
        # Create output directory
        if output_dir is None:
            name, ext = os.path.splitext(input_path)
            output_dir = f"{name}_segments"
        
        os.makedirs(output_dir, exist_ok=True)
        
        segments = []
        for i in range(num_segments):
            start_sample = i * segment_samples
            end_sample = min((i + 1) * segment_samples, len(y))
            
            segment = y[start_sample:end_sample]
            segment_path = os.path.join(output_dir, f"segment_{i+1:02d}.wav")
            
            sf.write(segment_path, segment, sr)
            segment_size = os.path.getsize(segment_path) / (1024 * 1024)
            
            print(f"Segment {i+1}: {segment_path} ({segment_size:.1f}MB)")
            segments.append(segment_path)
        
        return segments
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_compress.py <input_file> [--compress|--split] [--target-size 20]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)
    
    if "--compress" in sys.argv:
        target_size = 20
        if "--target-size" in sys.argv:
            idx = sys.argv.index("--target-size")
            if idx + 1 < len(sys.argv):
                target_size = float(sys.argv[idx + 1])
        
        print("="*50)
        print("AUDIO COMPRESSION")
        print("="*50)
        result = compress_audio_simple(input_file, target_size_mb=target_size)
        if result:
            print(f"✅ Compression successful: {result}")
        else:
            print("❌ Compression failed")
    
    elif "--split" in sys.argv:
        segment_duration = 600
        if "--segment-duration" in sys.argv:
            idx = sys.argv.index("--segment-duration")
            if idx + 1 < len(sys.argv):
                segment_duration = int(sys.argv[idx + 1])
        
        print("="*50)
        print("AUDIO SPLITTING")
        print("="*50)
        segments = split_audio_simple(input_file, segment_duration=segment_duration)
        if segments:
            print(f"✅ Splitting successful: {len(segments)} segments created")
        else:
            print("❌ Splitting failed")
    
    else:
        print("Please specify --compress or --split")
        print("\nExamples:")
        print("  python simple_compress.py file.wav --compress")
        print("  python simple_compress.py file.wav --split")
        print("  python simple_compress.py file.wav --compress --target-size 15") 