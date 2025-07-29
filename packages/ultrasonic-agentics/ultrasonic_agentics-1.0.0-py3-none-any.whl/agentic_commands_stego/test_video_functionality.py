#!/usr/bin/env python3
"""
Test script to verify video processing functionality.
Tests MoviePy installation, video embedding, and decoding.
"""

import os
import sys
import tempfile
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, ColorClip, CompositeVideoClip
from moviepy.audio.AudioClip import AudioArrayClip

# Add the parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from agentic_commands_stego.embed.video_embedder import VideoEmbedder
from agentic_commands_stego.decode.video_decoder import VideoDecoder
from agentic_commands_stego.crypto.cipher import CipherService


def create_test_video(output_path: str, duration: float = 5.0):
    """Create a simple test video with audio."""
    print(f"Creating test video: {output_path}")
    
    # Create video clip (solid color)
    video = ColorClip(size=(640, 480), color=(0, 122, 255), duration=duration)
    
    # Create audio (simple sine wave)
    sample_rate = 44100
    audio_duration = duration
    t = np.linspace(0, audio_duration, int(sample_rate * audio_duration))
    audio_array = np.sin(2 * np.pi * 440 * t) * 0.3  # 440 Hz sine wave
    audio_array = np.array([audio_array, audio_array]).T  # Stereo
    
    audio = AudioArrayClip(audio_array, fps=sample_rate)
    
    # Combine video and audio
    final_video = video.set_audio(audio)
    
    # Write video file
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        fps=24,
        verbose=False,
        logger=None
    )
    
    print(f"Test video created: {output_path}")


def test_moviepy_basic():
    """Test basic MoviePy functionality."""
    print("\n=== Testing Basic MoviePy Functionality ===")
    
    try:
        # Test imports
        from moviepy.editor import VideoFileClip, AudioFileClip
        print("✓ MoviePy imports successful")
        
        # Test creating a simple video
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            temp_video = tmp.name
        
        create_test_video(temp_video, duration=2.0)
        
        # Test loading video
        video = VideoFileClip(temp_video)
        print(f"✓ Video loaded: duration={video.duration}s, fps={video.fps}, size={video.size}")
        print(f"✓ Has audio: {video.audio is not None}")
        
        video.close()
        os.unlink(temp_video)
        
        print("✓ Basic MoviePy functionality working")
        return True
        
    except Exception as e:
        print(f"✗ MoviePy basic test failed: {e}")
        return False


def test_video_embedding():
    """Test video embedding and decoding functionality."""
    print("\n=== Testing Video Embedding/Decoding ===")
    
    try:
        # Create test video
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            input_video = tmp.name
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            output_video = tmp.name
        
        create_test_video(input_video, duration=5.0)
        
        # Test command
        test_command = "echo 'Hello from video!'"
        
        # Create cipher for key generation
        cipher = CipherService()
        key = cipher.key
        
        # Test embedding
        print("\nTesting video embedding...")
        embedder = VideoEmbedder(key=key)
        
        # Check compatibility first
        compat = embedder.validate_video_compatibility(input_video)
        print(f"Video compatibility: {compat}")
        
        if not compat['compatible']:
            print(f"✗ Video not compatible: {compat.get('error', 'Unknown error')}")
            return False
        
        # Embed command
        embedder.embed_file(
            input_path=input_video,
            output_path=output_video,
            command=test_command,
            obfuscate=True
        )
        print("✓ Command embedded successfully")
        
        # Test decoding
        print("\nTesting video decoding...")
        decoder = VideoDecoder(key=key)
        
        # Detect signal
        has_signal = decoder.detect_signal(output_video)
        print(f"Signal detected: {has_signal}")
        
        # Get signal strength
        strength = decoder.get_signal_strength(output_video)
        print(f"Signal strength: {strength:.2f}")
        
        # Decode command
        decoded_command = decoder.decode_file(output_video)
        print(f"Decoded command: {decoded_command}")
        
        # Analyze video
        print("\nAnalyzing video...")
        analysis = decoder.analyze_video(output_video)
        print(f"Analysis results:")
        for key, value in analysis.items():
            if key not in ['file_path', 'frequency_spectrum']:
                print(f"  {key}: {value}")
        
        # Clean up
        os.unlink(input_video)
        os.unlink(output_video)
        
        # Check if decoding was successful
        if decoded_command == test_command:
            print("\n✓ Video embedding/decoding test PASSED")
            return True
        else:
            print(f"\n✗ Video embedding/decoding test FAILED")
            print(f"  Expected: {test_command}")
            print(f"  Got: {decoded_command}")
            return False
        
    except Exception as e:
        print(f"✗ Video embedding/decoding test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ffmpeg_availability():
    """Test if FFmpeg is available."""
    print("\n=== Testing FFmpeg Availability ===")
    
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ FFmpeg is available")
            # Print version info
            lines = result.stdout.split('\n')
            if lines:
                print(f"  {lines[0]}")
            return True
        else:
            print("✗ FFmpeg not found or error running it")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg not found in PATH")
        return False
    except Exception as e:
        print(f"✗ Error checking FFmpeg: {e}")
        return False


def main():
    """Run all video functionality tests."""
    print("Video Processing Functionality Test")
    print("==================================")
    
    # Test FFmpeg
    ffmpeg_ok = test_ffmpeg_availability()
    
    # Test MoviePy basics
    moviepy_ok = test_moviepy_basic()
    
    # Test video embedding/decoding
    if moviepy_ok and ffmpeg_ok:
        video_ok = test_video_embedding()
    else:
        print("\n✗ Skipping video embedding test due to missing dependencies")
        video_ok = False
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"FFmpeg available: {'✓' if ffmpeg_ok else '✗'}")
    print(f"MoviePy working: {'✓' if moviepy_ok else '✗'}")
    print(f"Video embedding/decoding: {'✓' if video_ok else '✗'}")
    
    if not ffmpeg_ok:
        print("\nFFmpeg is required for video processing. Install it with:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
    
    return all([ffmpeg_ok, moviepy_ok, video_ok])


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)