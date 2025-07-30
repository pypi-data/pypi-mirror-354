"""Utility functions for keyframe-scout"""

from __future__ import annotations

import math
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple

import cv2
import numpy as np

from .constants import RESOLUTION_MAP, SUPPORTED_FORMATS


def round_by_factor(number: int, factor: int) -> int:
    """Returns the closest integer to 'number' that is divisible by 'factor'."""
    return round(number / factor) * factor


def ceil_by_factor(number: int, factor: int) -> int:
    """Returns the smallest integer greater than or equal to 'number' that is divisible by 'factor'."""
    return math.ceil(number / factor) * factor


def floor_by_factor(number: int, factor: int) -> int:
    """Returns the largest integer less than or equal to 'number' that is divisible by 'factor'."""
    return math.floor(number / factor) * factor


def is_video_file(path: str) -> bool:
    """Check if the file is a supported video format."""
    return Path(path).suffix.lower() in SUPPORTED_FORMATS


def get_video_info(video_path: str) -> Dict:
    """
    Get video information using OpenCV.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dictionary containing video info
        
    Raises:
        ValueError: If video cannot be opened
    """
    if not os.path.exists(video_path):
        raise ValueError(f"Video file not found: {video_path}")
    
    if not is_video_file(video_path):
        raise ValueError(f"Unsupported video format: {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")
    
    info = {
        'path': video_path,
        'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'fourcc': int(cap.get(cv2.CAP_PROP_FOURCC))
    }
    info['duration'] = info['total_frames'] / info['fps'] if info['fps'] > 0 else 0
    info['resolution'] = f"{info['width']}x{info['height']}"
    
    cap.release()
    
    return info


def calculate_output_resolution(
    resolution: str, 
    original_width: int, 
    original_height: int
) -> Tuple[Optional[str], int, int]:
    """
    Calculate output resolution based on preset.
    
    Args:
        resolution: Resolution preset or 'original'
        original_width: Original video width
        original_height: Original video height
        
    Returns:
        Tuple of (scale_filter, new_width, new_height)
    """
    if resolution == 'original':
        return None, original_width, original_height
    
    if resolution not in RESOLUTION_MAP:
        return None, original_width, original_height
    
    target_width, target_height = RESOLUTION_MAP[resolution]
    
    # Calculate scale ratio maintaining aspect ratio
    scale_ratio = min(target_width / original_width, target_height / original_height)
    
    # Don't upscale
    if scale_ratio >= 1.0:
        return None, original_width, original_height
    
    # Calculate actual output size (ensure even numbers)
    new_width = int((original_width * scale_ratio) // 2) * 2
    new_height = int((original_height * scale_ratio) // 2) * 2
    
    scale_filter = f"scale={new_width}:{new_height}"
    
    return scale_filter, new_width, new_height


def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are installed."""
    dependencies = {}
    
    # Check FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        dependencies['ffmpeg'] = True
    except:
        dependencies['ffmpeg'] = False
    
    # Check OpenCV
    try:
        import cv2
        dependencies['opencv'] = True
    except:
        dependencies['opencv'] = False
    
    # Check NumPy
    try:
        import numpy
        dependencies['numpy'] = True
    except:
        dependencies['numpy'] = False
    
    # Check Pillow
    try:
        import PIL
        dependencies['pillow'] = True
    except:
        dependencies['pillow'] = False
    
    return dependencies


def format_timestamp(seconds: float) -> str:
    """Format seconds to HH:MM:SS.ms format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def ensure_output_dir(output_dir: str) -> Path:
    """
    Ensure output directory exists, create if not.
    
    Args:
        output_dir: Output directory path
        
    Returns:
        Path object of the output directory
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path