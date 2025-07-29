"""Main extraction module for keyframe-scout"""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np
from PIL import Image

from .analyzer import analyze_video_frames
from .constants import (
    DEFAULT_IMAGE_FORMAT, DEFAULT_IMAGE_QUALITY, FRAME_FACTOR,
    MAX_FRAMES, MIN_FRAMES
)
from .selector import select_keyframes, smart_frame_count
from .utils import (
    calculate_output_resolution, format_timestamp, get_video_info,
    round_by_factor
)

logger = logging.getLogger(__name__)


def extract_frames(
    video_path: str, 
    frame_list: List[Dict], 
    output_dir: str,
    resolution: str = 'original', 
    image_format: str = DEFAULT_IMAGE_FORMAT,
    image_quality: int = DEFAULT_IMAGE_QUALITY,
    ffmpeg_path: str = 'ffmpeg'
) -> List[Dict]:
    """
    Extract specified frames from video.
    
    Args:
        video_path: Path to video file
        frame_list: List of frame information to extract
        output_dir: Output directory
        resolution: Output resolution preset
        image_format: Output image format
        image_quality: Output image quality (1-100)
        ffmpeg_path: Path to ffmpeg executable
        
    Returns:
        List of extracted frame information
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean output directory
    for file in os.listdir(output_dir):
        if file.endswith(('.jpg', '.png', '.jpeg')):
            os.unlink(os.path.join(output_dir, file))
    
    # Get video info
    video_info = get_video_info(video_path)
    
    # Calculate output resolution
    scale_filter, new_width, new_height = calculate_output_resolution(
        resolution, video_info['width'], video_info['height']
    )
    output_resolution = f"{new_width}x{new_height}"
    
    saved_frames = []
    
    for idx, frame_info in enumerate(frame_list):
        timestamp = frame_info['timestamp']
        output_filename = f'keyframe-{idx+1:03d}.{image_format}'
        output_path = os.path.join(output_dir, output_filename)
        
        # Build FFmpeg command
        cmd = [
            ffmpeg_path,
            '-ss', str(timestamp),
            '-i', video_path,
            '-frames:v', '1',
        ]
        
        # Add quality settings
        if image_format == 'jpg' or image_format == 'jpeg':
            cmd.extend(['-q:v', str(int((100 - image_quality) / 100 * 31) + 1)])
        elif image_format == 'png':
            cmd.extend(['-compression_level', str(int((100 - image_quality) / 10))])
        
        # Add scale filter if needed
        if scale_filter:
            cmd.extend(['-vf', scale_filter])
        
        cmd.extend(['-y', output_path])
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            
            if os.path.exists(output_path):
                saved_frame = {
                    'path': output_path,
                    'filename': output_filename,
                    'frame_idx': frame_info['frame_idx'],
                    'timestamp': timestamp,
                    'timestamp_str': format_timestamp(timestamp),
                    'change_score': frame_info['change_score'],
                    'resolution': output_resolution
                }
                saved_frames.append(saved_frame)
                logger.info(f"Saved: {output_filename} ({output_resolution})")
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to extract frame at {timestamp:.2f}s: {e}")
    
    return saved_frames


def extract_video_keyframes(video_config: Dict[str, Union[str, int, float]]) -> Dict:
    """
    Extract keyframes from video.
    
    Args:
        video_config: Video configuration dict containing:
            - video: Video path (required)
            - output_dir: Output directory (required)
            - nframes: Number of frames (optional)
            - mode: Extraction mode "fixed", "adaptive", "interval" (optional)
            - min_frames: Minimum frames (optional)
            - max_frames: Maximum frames (optional)
            - interval: Time interval (optional)
            - frames_per_interval: Frames per interval (optional)
            - resolution: Output resolution (optional)
            - sample_rate: Analysis sample rate (optional)
            - image_format: Output format "jpg", "png" (optional)
            - image_quality: Output quality 1-100 (optional)
            
    Returns:
        Extraction result dictionary
    """
    # Parse parameters
    video_path = video_config.get("video")
    if isinstance(video_path, str) and video_path.startswith("file://"):
        video_path = video_path[7:]
    
    output_dir = video_config.get("output_dir", "output_frames")
    mode = video_config.get("mode", "adaptive")
    resolution = video_config.get("resolution", "original")
    sample_rate = video_config.get("sample_rate", 1)
    image_format = video_config.get("image_format", DEFAULT_IMAGE_FORMAT)
    image_quality = video_config.get("image_quality", DEFAULT_IMAGE_QUALITY)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing video: {video_path}")
    logger.info(f"Output resolution: {resolution}")
    
    if not os.path.exists(video_path):
        raise ValueError(f"Video file not found: {video_path}")
    
    # 1. Analyze video frames
    logger.info("Step 1/3: Analyzing video frames...")
    frame_changes, video_info = analyze_video_frames(video_path, sample_rate)
    
    # 2. Calculate frame count
    if "nframes" in video_config:
        n_frames = round_by_factor(video_config["nframes"], FRAME_FACTOR)
        logger.info(f"Using specified frame count: {n_frames}")
    else:
        n_frames = smart_frame_count(
            duration=video_info['duration'],
            mode=mode,
            min_frames=video_config.get("min_frames", MIN_FRAMES),
            max_frames=video_config.get("max_frames", MAX_FRAMES),
            interval=video_config.get("interval", 10.0),
            frames_per_interval=video_config.get("frames_per_interval", 1)
        )
    
    logger.info(f"{'='*60}\n")
    
    # 3. Select keyframes
    logger.info(f"Step 2/3: Selecting {n_frames} keyframes from {len(frame_changes)} analyzed frames...")
    selected_frames = select_keyframes(frame_changes, n_frames)
    
    # 4. Extract frames
    logger.info(f"\nStep 3/3: Extracting keyframes...")
    saved_frames = extract_frames(
        video_path, selected_frames, output_dir, resolution,
        image_format=image_format,
        image_quality=image_quality,
        ffmpeg_path=video_config.get("ffmpeg_path", "ffmpeg")
    )
    
    # Generate result
    result = {
        'video_path': video_path,
        'video_duration': video_info['duration'],
        'total_frames_analyzed': len(frame_changes),
        'extracted_frames': len(saved_frames),
        'mode': mode,
        'resolution': resolution,
        'original_resolution': f"{video_info['width']}x{video_info['height']}",
        'output_dir': output_dir,
        'frames': saved_frames,
        'statistics': {
            'max_change_score': max(f['change_score'] for f in frame_changes),
            'avg_change_score': np.mean([f['change_score'] for f in frame_changes]),
            'selected_total_score': sum(f['change_score'] for f in saved_frames)
        }
    }
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("Extraction complete!")
    logger.info(f"Video duration: {video_info['duration']:.1f}s")
    logger.info(f"Original resolution: {result['original_resolution']}")
    logger.info(f"Output resolution: {resolution}")
    logger.info(f"Analyzed frames: {result['total_frames_analyzed']}")
    logger.info(f"Extracted frames: {result['extracted_frames']}")
    logger.info(f"Mode: {result['mode']}")
    logger.info(f"\nKeyframe summary:")
    
    for frame in saved_frames:
        logger.info(f"  - {frame['filename']}: "
                    f"time {frame['timestamp']:.1f}s, "
                    f"score {frame['change_score']:.1f}")
    
    logger.info(f"\nOutput directory: {output_dir}")
    logger.info(f"{'='*60}\n")
    
    return result


def extract_keyframes_batch(video_configs: List[Dict]) -> List[Dict]:
    """
    Extract keyframes from multiple videos.
    
    Args:
        video_configs: List of video configuration dictionaries
        
    Returns:
        List of extraction results
    """
    results = []
    
    for i, config in enumerate(video_configs):
        logger.info(f"\nProcessing video {i+1}/{len(video_configs)}")
        try:
            result = extract_video_keyframes(config)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process video: {e}")
            results.append({'error': str(e), 'video_config': config})
    
    return results