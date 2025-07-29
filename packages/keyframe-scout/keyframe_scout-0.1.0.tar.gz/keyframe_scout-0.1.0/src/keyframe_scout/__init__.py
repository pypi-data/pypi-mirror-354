"""
KeyFrame Scout - Intelligent video keyframe extraction tool
"""

__version__ = "0.1.0"
__author__ = "Jiajun Chen"
__email__ = "cjj198909@gmail.com"

from .extractor import extract_video_keyframes, extract_keyframes_batch
from .analyzer import analyze_video_frames
from .selector import select_keyframes
from .utils import get_video_info

__all__ = [
    "extract_video_keyframes",
    "extract_keyframes_batch",
    "analyze_video_frames", 
    "select_keyframes",
    "get_video_info",
]