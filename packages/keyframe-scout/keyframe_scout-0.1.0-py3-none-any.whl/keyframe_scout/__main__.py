"""Command line interface for keyframe-scout"""

import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .extractor import extract_video_keyframes
from .utils import check_dependencies

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='KeyFrame Scout - Intelligent video keyframe extraction',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract 5 frames with 720p resolution
  keyframe-scout video.mp4 -o output_frames --nframes 5 --resolution 720p
  
  # Adaptive mode with 480p resolution
  keyframe-scout video.mp4 -o output_frames --mode adaptive --resolution 480p
  
  # Extract 1 frame every 10 seconds
  keyframe-scout video.mp4 -o output_frames --mode interval --interval 10
  
  # Batch process multiple videos
  keyframe-scout video1.mp4 video2.mp4 -o output_dir --mode adaptive
        """
    )
    
    parser.add_argument('videos', nargs='+', help='Video file path(s)')
    parser.add_argument('-o', '--output', default='keyframes', help='Output directory')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    
    # Frame selection options
    frame_group = parser.add_argument_group('frame selection')
    frame_group.add_argument('--nframes', type=int, help='Number of frames to extract')
    frame_group.add_argument('--mode', choices=['fixed', 'adaptive', 'interval'], 
                            default='adaptive', help='Extraction mode')
    frame_group.add_argument('--interval', type=float, default=10.0,
                            help='Time interval (seconds) for interval mode')
    frame_group.add_argument('--frames-per-interval', type=int, default=1,
                            help='Frames per interval')
    frame_group.add_argument('--min-frames', type=int, default=3, help='Minimum frames')
    frame_group.add_argument('--max-frames', type=int, default=30, help='Maximum frames')
    
    # Output options
    output_group = parser.add_argument_group('output options')
    output_group.add_argument('--resolution', 
                             choices=['original', '1080p', '720p', '480p', '360p', '240p'],
                             default='original', help='Output resolution')
    output_group.add_argument('--format', choices=['jpg', 'png'], default='jpg',
                             help='Output image format')
    output_group.add_argument('--quality', type=int, default=95,
                             help='Output image quality (1-100)')
    
    # Advanced options
    advanced_group = parser.add_argument_group('advanced options')
    advanced_group.add_argument('--sample-rate', type=int, default=1,
                               help='Frame sampling rate for analysis')
    advanced_group.add_argument('--ffmpeg-path', default='ffmpeg',
                               help='Path to ffmpeg executable')
    advanced_group.add_argument('--check-deps', action='store_true',
                               help='Check dependencies and exit')
    
    args = parser.parse_args()
    
    # Check dependencies
    if args.check_deps:
        deps = check_dependencies()
        print("\nDependency Status:")
        for dep, status in deps.items():
            status_str = "✓ Installed" if status else "✗ Not found"
            print(f"  {dep}: {status_str}")
        sys.exit(0 if all(deps.values()) else 1)
    
    # Process videos
    for i, video_path in enumerate(args.videos):
        if len(args.videos) > 1:
            # Create subdirectory for each video
            video_name = Path(video_path).stem
            output_dir = Path(args.output) / video_name
        else:
            output_dir = args.output
        
        # Build configuration
        video_config = {
            'video': video_path,
            'output_dir': str(output_dir),
            'mode': args.mode,
            'interval': args.interval,
            'frames_per_interval': args.frames_per_interval,
            'min_frames': args.min_frames,
            'max_frames': args.max_frames,
            'resolution': args.resolution,
            'sample_rate': args.sample_rate,
            'image_format': args.format,
            'image_quality': args.quality,
            'ffmpeg_path': args.ffmpeg_path
        }
        
        if args.nframes:
            video_config['nframes'] = args.nframes
        
        try:
            if len(args.videos) > 1:
                logger.info(f"\nProcessing video {i+1}/{len(args.videos)}: {video_path}")
            
            result = extract_video_keyframes(video_config)
            
        except Exception as e:
            logger.error(f"Error processing {video_path}: {e}")
            if len(args.videos) == 1:
                sys.exit(1)


if __name__ == "__main__":
    main()