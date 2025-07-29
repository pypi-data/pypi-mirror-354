"""Advanced usage examples for keyframe-scout"""

import keyframe_scout as ks
from pathlib import Path
import json

def example_batch_processing():
    """Batch processing multiple videos"""
    print("=== Batch Processing ===")
    
    video_configs = [
        {
            'video': 'video1.mp4',
            'output_dir': 'output/video1',
            'mode': 'adaptive',
            'resolution': '720p'
        },
        {
            'video': 'video2.mp4',
            'output_dir': 'output/video2',
            'nframes': 8,
            'resolution': '480p'
        },
        {
            'video': 'video3.mp4',
            'output_dir': 'output/video3',
            'mode': 'interval',
            'interval': 10
        }
    ]
    
    results = ks.extract_keyframes_batch(video_configs)
    
    for i, result in enumerate(results):
        if 'error' in result:
            print(f"Video {i+1}: Error - {result['error']}")
        else:
            print(f"Video {i+1}: Extracted {result['extracted_frames']} frames")


def example_custom_analysis():
    """Custom frame analysis"""
    print("\n=== Custom Analysis ===")
    
    # Analyze frames without extraction
    frame_changes, video_info = ks.analyze_video_frames(
        'sample_video.mp4',
        sample_rate=2  # Analyze every 2nd frame
    )
    
    print(f"Total frames analyzed: {len(frame_changes)}")
    print(f"Video FPS: {video_info['fps']:.2f}")
    
    # Find frames with highest change scores
    top_frames = sorted(frame_changes, key=lambda x: x['change_score'], reverse=True)[:5]
    
    print("\nTop 5 frames by change score:")
    for frame in top_frames:
        print(f"  Frame {frame['frame_idx']} at {frame['timestamp']:.2f}s: "
              f"score={frame['change_score']:.2f}")


def example_video_info():
    """Get video information"""
    print("\n=== Video Information ===")
    
    info = ks.get_video_info('sample_video.mp4')
    
    print(f"Duration: {info['duration']:.2f} seconds")
    print(f"Resolution: {info['width']}x{info['height']}")
    print(f"FPS: {info['fps']:.2f}")
    print(f"Total frames: {info['total_frames']}")


def example_save_metadata():
    """Extract frames and save metadata"""
    print("\n=== Save Metadata ===")
    
    config = {
        'video': 'sample_video.mp4',
        'output_dir': 'output/with_metadata',
        'mode': 'adaptive',
        'resolution': '720p',
        'image_quality': 90
    }
    
    result = ks.extract_video_keyframes(config)
    
    # Save metadata
    metadata_path = Path(result['output_dir']) / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    example_batch_processing()
    example_custom_analysis()
    example_video_info()
    example_save_metadata()