#!/usr/bin/env python
"""
Audio compression utility for large files
"""
import os
import sys
from pydub import AudioSegment
import argparse

def compress_audio(input_path, output_path=None, target_size_mb=20):
    """
    Compress audio file to target size
    """
    try:
        print(f"Loading audio file: {input_path}")
        audio = AudioSegment.from_file(input_path)
        
        # Get original file info
        original_duration = len(audio) / 1000  # seconds
        original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
        
        print(f"Original: {original_duration:.1f}s, {original_size:.1f}MB")
        
        if original_size <= target_size_mb:
            print(f"File is already under {target_size_mb}MB, no compression needed.")
            return input_path
        
        # Calculate target bitrate
        target_size_bytes = target_size_mb * 1024 * 1024
        target_bitrate = int((target_size_bytes * 8) / original_duration)
        
        # Ensure minimum bitrate for quality
        target_bitrate = max(target_bitrate, 64000)  # 64 kbps minimum
        
        print(f"Compressing to {target_bitrate} bps...")
        
        # Generate output path if not provided
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_compressed{ext}"
        
        # Export compressed audio
        audio.export(
            output_path,
            format="mp3",
            bitrate=f"{target_bitrate//1000}k",
            parameters=["-q:a", "2"]  # High quality
        )
        
        # Check final size
        final_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Compressed: {final_size:.1f}MB")
        print(f"Saved to: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"Error compressing audio: {e}")
        return None

def split_audio(input_path, output_dir=None, segment_duration=600000):  # 10 minutes in ms
    """
    Split audio file into smaller segments
    """
    try:
        print(f"Loading audio file: {input_path}")
        audio = AudioSegment.from_file(input_path)
        
        total_duration = len(audio)
        num_segments = (total_duration + segment_duration - 1) // segment_duration
        
        print(f"Total duration: {total_duration/1000:.1f}s")
        print(f"Splitting into {num_segments} segments of {segment_duration/1000:.1f}s each")
        
        # Create output directory
        if output_dir is None:
            name, ext = os.path.splitext(input_path)
            output_dir = f"{name}_segments"
        
        os.makedirs(output_dir, exist_ok=True)
        
        segments = []
        for i in range(num_segments):
            start_time = i * segment_duration
            end_time = min((i + 1) * segment_duration, total_duration)
            
            segment = audio[start_time:end_time]
            segment_path = os.path.join(output_dir, f"segment_{i+1:02d}.mp3")
            
            segment.export(segment_path, format="mp3")
            segment_size = os.path.getsize(segment_path) / (1024 * 1024)
            
            print(f"Segment {i+1}: {segment_path} ({segment_size:.1f}MB)")
            segments.append(segment_path)
        
        return segments
        
    except Exception as e:
        print(f"Error splitting audio: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Audio compression and splitting utility")
    parser.add_argument("input_file", help="Input audio file path")
    parser.add_argument("--compress", action="store_true", help="Compress audio file")
    parser.add_argument("--split", action="store_true", help="Split audio into segments")
    parser.add_argument("--target-size", type=float, default=20, help="Target size in MB (default: 20)")
    parser.add_argument("--segment-duration", type=int, default=600, help="Segment duration in seconds (default: 600)")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File not found: {args.input_file}")
        return
    
    if args.compress:
        print("="*50)
        print("AUDIO COMPRESSION")
        print("="*50)
        result = compress_audio(args.input_file, args.output, args.target_size)
        if result:
            print(f"✅ Compression successful: {result}")
        else:
            print("❌ Compression failed")
    
    elif args.split:
        print("="*50)
        print("AUDIO SPLITTING")
        print("="*50)
        segments = split_audio(args.input_file, args.output, args.segment_duration * 1000)
        if segments:
            print(f"✅ Splitting successful: {len(segments)} segments created")
        else:
            print("❌ Splitting failed")
    
    else:
        print("Please specify --compress or --split")
        print("\nExamples:")
        print("  python compress_audio.py large_file.wav --compress")
        print("  python compress_audio.py large_file.wav --split")
        print("  python compress_audio.py large_file.wav --compress --target-size 15")

if __name__ == "__main__":
    main() 