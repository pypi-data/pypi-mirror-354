"""Basic usage examples for keyframe-scout"""

import keyframe_scout as ks
from pathlib import Path

def example_basic():
    """Basic extraction example"""
    print("=== Basic Extraction ===")
    
    config = {
        'video': 'sample_video.mp4',
        'output_dir': 'output/basic',
        'nframes': 5,
        'resolution': '720p'
    }
    
    result = ks.extract_video_keyframes(config)
    
    print(f"Extracted {result['extracted_frames']} frames")
    print(f"Output directory: {result['output_dir']}")
    

def example_adaptive():
    """Adaptive mode example"""
    print("\n=== Adaptive Mode ===")
    
    config = {
        'video': 'sample_video.mp4',
        'output_dir': 'output/adaptive',
        'mode': 'adaptive',
        'min_frames': 3,
        'max_frames': 10
    }
    
    result = ks.extract_video_keyframes(config)
    
    print(f"Video duration: {result['video_duration']:.1f}s")
    print(f"Frames extracted: {result['extracted_frames']}")
    

def example_interval():
    """Interval mode example"""
    print("\n=== Interval Mode ===")
    
    config = {
        'video': 'sample_video.mp4',
        'output_dir': 'output/interval',
        'mode': 'interval',
        'interval': 5.0,  # Every 5 seconds
        'frames_per_interval': 1
    }
    
    result = ks.extract_video_keyframes(config)
    
    for frame in result['frames']:
        print(f"  Frame at {frame['timestamp']:.1f}s: {frame['filename']}")


if __name__ == "__main__":
    example_basic()
    example_adaptive()
    example_interval()