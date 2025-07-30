"""
KeyFrame Scout - Intelligent video keyframe extraction tool
"""

__version__ = "0.2.4"
__author__ = "Jiajun Chen"
__email__ = "cjj198909@gmail.com"

# Core functionality imports
from .extractor import extract_video_keyframes, extract_single_frame
from .analyzer import analyze_video_frames
from .selector import select_keyframes
from .utils import get_video_info, check_dependencies, ensure_output_dir

# Batch processing
try:
    from .batch import extract_keyframes_batch
except ImportError:
    # If batch module doesn't exist, set to None
    extract_keyframes_batch = None

# VLM utilities
from .vlm_utils import (
    extract_frames_for_vlm,
    prepare_for_azure_openai,
    create_video_messages,
    create_batch_messages,
    frames_to_base64_urls,
    save_base64_frames,
    estimate_token_usage
)

# Azure integration (optional)
try:
    from .azure_integration import VideoAnalyzer
except ImportError:
    VideoAnalyzer = None

# Define what should be imported with "from keyframe_scout import *"
__all__ = [
    # Version info
    "__version__",
    
    # Core functions
    "extract_video_keyframes",
    "extract_single_frame",
    "analyze_video_frames",
    "select_keyframes",
    "get_video_info",
    "check_dependencies",
    "ensure_output_dir",
    
    # Batch processing
    "extract_keyframes_batch",
    
    # VLM utilities
    "extract_frames_for_vlm",
    "prepare_for_azure_openai",
    "create_video_messages",
    "create_batch_messages",
    "frames_to_base64_urls",
    "save_base64_frames",
    "estimate_token_usage",
    
    # Azure integration
    "VideoAnalyzer"
]

# Remove None values from __all__
__all__ = [item for item in __all__ if item not in ["extract_keyframes_batch", "VideoAnalyzer"] or eval(item) is not None]


def get_version():
    """Get the current version of keyframe-scout"""
    return __version__


def print_info():
    """Print information about keyframe-scout"""
    print(f"KeyFrame Scout v{__version__}")
    print("Intelligent video keyframe extraction tool")
    print(f"Author: {__author__}")
    
    # Check dependencies
    deps = check_dependencies()
    print("\nDependencies:")
    for dep, available in deps.items():
        status = "✓" if available else "✗"
        print(f"  {status} {dep}")
    
    # Check optional features
    print("\nOptional features:")
    print(f"  {'✓' if extract_keyframes_batch else '✗'} Batch processing")
    print(f"  {'✓' if VideoAnalyzer else '✗'} Azure OpenAI integration")