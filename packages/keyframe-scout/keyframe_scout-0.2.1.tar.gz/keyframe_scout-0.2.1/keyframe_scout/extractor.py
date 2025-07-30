"""
Core extraction module for keyframe-scout.
"""
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Union, Optional, Tuple
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO

from .analyzer import analyze_video_frames
from .selector import select_keyframes
from .utils import get_video_info, ensure_output_dir

logger = logging.getLogger(__name__)


def image_to_base64(image_array: np.ndarray, quality: int = 95) -> str:
    """
    Convert numpy array to base64 string.
    
    Args:
        image_array: Image as numpy array (RGB format)
        quality: JPEG quality (1-100)
    
    Returns:
        Base64 encoded string
    """
    img = Image.fromarray(image_array)
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=quality)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def resize_image_for_base64(image: np.ndarray, max_size: int) -> np.ndarray:
    """
    Resize image to fit within max_size while maintaining aspect ratio.
    
    Args:
        image: Input image array
        max_size: Maximum dimension (width or height)
    
    Returns:
        Resized image array
    """
    height, width = image.shape[:2]
    
    # Check if resizing is needed
    if height <= max_size and width <= max_size:
        return image
    
    # Calculate new dimensions
    if height > width:
        new_height = max_size
        new_width = int(width * (max_size / height))
    else:
        new_width = max_size
        new_height = int(height * (max_size / width))
    
    # Resize image
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    return resized


def extract_frames_from_video(
    video_path: Path,
    frame_indices: List[int],
    output_dir: Optional[Path] = None,
    resolution: str = "original",
    image_format: str = "jpg",
    image_quality: int = 95,
    return_base64: bool = False,
    max_size: Optional[int] = 1024
) -> List[Dict]:
    """
    Extract specific frames from video.
    
    Args:
        video_path: Path to video file
        frame_indices: List of frame indices to extract
        output_dir: Output directory for saving frames (optional if return_base64=True)
        resolution: Output resolution
        image_format: Output image format
        image_quality: Image quality (1-100)
        return_base64: If True, return base64 encoded frames
        max_size: Maximum dimension for base64 images
    
    Returns:
        List of frame information dictionaries
    """
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Resolution mapping
    resolution_map = {
        "360p": (640, 360),
        "480p": (854, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "original": None
    }
    
    target_resolution = resolution_map.get(resolution, None)
    
    extracted_frames = []
    
    for idx, frame_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        
        if not ret:
            logger.warning(f"Failed to read frame {frame_idx}")
            continue
        
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize if needed (for file output)
        if target_resolution and resolution != "original":
            frame_rgb = cv2.resize(frame_rgb, target_resolution, interpolation=cv2.INTER_LANCZOS4)
        
        # Prepare frame info
        timestamp = frame_idx / fps
        frame_info = {
            "frame_idx": frame_idx,
            "timestamp": timestamp,
            "filename": f"frame_{idx+1:04d}.{image_format}",
            "resolution": f"{frame_rgb.shape[1]}x{frame_rgb.shape[0]}"
        }
        
        # Save to file if output_dir is provided
        if output_dir:
            output_path = output_dir / frame_info["filename"]
            Image.fromarray(frame_rgb).save(
                output_path, 
                quality=image_quality if image_format == 'jpg' else None
            )
            frame_info["path"] = str(output_path)
            logger.info(f"Saved frame {idx+1} at {timestamp:.2f}s to {output_path}")
        
        # Generate base64 if requested
        if return_base64:
            # Resize for base64 if needed
            frame_for_base64 = frame_rgb
            if max_size and (frame_rgb.shape[0] > max_size or frame_rgb.shape[1] > max_size):
                frame_for_base64 = resize_image_for_base64(frame_rgb, max_size)
            
            frame_info["base64"] = image_to_base64(frame_for_base64, image_quality)
            # Update resolution for base64 version
            frame_info["base64_resolution"] = f"{frame_for_base64.shape[1]}x{frame_for_base64.shape[0]}"
        
        extracted_frames.append(frame_info)
    
    cap.release()
    return extracted_frames


def extract_frames_with_ffmpeg(
    video_path: Path,
    timestamps: List[float],
    output_dir: Path,
    resolution: str = "original",
    image_format: str = "jpg",
    image_quality: int = 95
) -> List[Dict]:
    """
    Extract frames using FFmpeg (fallback method).
    
    Args:
        video_path: Path to video file
        timestamps: List of timestamps in seconds
        output_dir: Output directory
        resolution: Output resolution
        image_format: Output image format
        image_quality: Image quality
    
    Returns:
        List of frame information
    """
    extracted_frames = []
    
    # Resolution mapping for FFmpeg
    scale_filter = ""
    if resolution == "720p":
        scale_filter = "-vf scale=1280:720"
    elif resolution == "480p":
        scale_filter = "-vf scale=854:480"
    elif resolution == "360p":
        scale_filter = "-vf scale=640:360"
    
    for idx, timestamp in enumerate(timestamps):
        output_path = output_dir / f"frame_{idx+1:04d}.{image_format}"
        
        cmd = [
            "ffmpeg", "-ss", str(timestamp), "-i", str(video_path),
            "-frames:v", "1", "-q:v", str(100 - image_quality)
        ]
        
        if scale_filter:
            cmd.extend(scale_filter.split())
        
        cmd.extend(["-y", str(output_path)])
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Extracted frame at {timestamp:.2f}s")
            
            extracted_frames.append({
                "timestamp": timestamp,
                "filename": output_path.name,
                "path": str(output_path)
            })
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr.decode()}")
    
    return extracted_frames


def extract_video_keyframes(video_config: Dict[str, Union[str, int, float]]) -> Dict:
    """
    Extract keyframes from a video file.
    
    Args:
        video_config: Configuration dictionary with keys:
            - video: Path to video file (required)
            - output_dir: Output directory (optional if return_base64=True)
            - mode: Extraction mode ('adaptive', 'interval', 'fixed')
            - nframes: Number of frames to extract
            - interval: Time interval for interval mode
            - min_frames: Minimum frames for adaptive mode
            - max_frames: Maximum frames for adaptive mode
            - frames_per_interval: Frames per interval
            - resolution: Output resolution
            - image_format: Output format ('jpg', 'png')
            - image_quality: JPEG quality (1-100)
            - sample_rate: Frame sampling rate for analysis
            - return_base64: If True, return base64 encoded frames
            - include_files: If True, also save files when return_base64=True
            - max_size: Maximum dimension for base64 images
    
    Returns:
        Dictionary containing extraction results
    """
    # Extract configuration
    video_path = Path(video_config["video"])
    output_dir = video_config.get("output_dir")
    mode = video_config.get("mode", "adaptive")
    nframes = video_config.get("nframes")
    interval = video_config.get("interval", 5.0)
    min_frames = video_config.get("min_frames", 3)
    max_frames = video_config.get("max_frames", 30)
    frames_per_interval = video_config.get("frames_per_interval", 1)
    resolution = video_config.get("resolution", "original")
    image_format = video_config.get("image_format", "jpg")
    image_quality = video_config.get("image_quality", 95)
    sample_rate = video_config.get("sample_rate", 30)
    
    # New base64 related parameters
    return_base64 = video_config.get("return_base64", False)
    include_files = video_config.get("include_files", False)
    max_size = video_config.get("max_size", 1024)
    
    # Validate input
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Handle output directory
    if output_dir:
        output_dir = Path(output_dir)
        ensure_output_dir(output_dir)
    elif not return_base64 or include_files:
        # If not returning base64 or if we need to save files, we need an output directory
        raise ValueError("output_dir is required when not using return_base64 mode or when include_files=True")
    
    logger.info(f"Processing video: {video_path}")
    logger.info(f"Mode: {mode}, Target frames: {nframes}")
    
    # Get video information
    video_info = get_video_info(str(video_path))
    duration = video_info["duration"]
    total_frames = video_info["total_frames"]
    
    # Analyze video frames
    logger.info("Analyzing video frames...")
    frame_changes, _ = analyze_video_frames(str(video_path), sample_rate)
    
    # Select keyframes based on mode
    logger.info(f"Selecting keyframes using {mode} mode...")
    selected_frames = select_keyframes(
        frame_changes=frame_changes,
        mode=mode,
        duration=duration,
        total_frames=total_frames,
        nframes=nframes,
        interval=interval,
        min_frames=min_frames,
        max_frames=max_frames,
        frames_per_interval=frames_per_interval
    )
    
    logger.info(f"Selected {len(selected_frames)} keyframes")
    
    # Extract frames
    logger.info("Extracting frames...")
    frame_indices = [f["frame_idx"] for f in selected_frames]
    
    # Determine if we need to save files
    save_files = output_dir is not None and (not return_base64 or include_files)
    
    extracted_frames = extract_frames_from_video(
        video_path=video_path,
        frame_indices=frame_indices,
        output_dir=output_dir if save_files else None,
        resolution=resolution,
        image_format=image_format,
        image_quality=image_quality,
        return_base64=return_base64,
        max_size=max_size
    )
    
    # Prepare result
    result = {
        "video_path": str(video_path),
        "video_duration": duration,
        "total_frames": total_frames,
        "extracted_frames": len(extracted_frames),
        "output_dir": str(output_dir) if output_dir else None,
        "extraction_mode": mode,
        "resolution": resolution,
        "frames": extracted_frames
    }
    
    # Save metadata if output directory exists
    if output_dir and save_files:
        metadata_path = output_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Saved metadata to {metadata_path}")
    
    logger.info(f"Extraction complete. {len(extracted_frames)} frames extracted.")
    
    return result


def extract_single_frame(
    video_path: Union[str, Path],
    timestamp: float,
    output_path: Optional[Union[str, Path]] = None,
    return_base64: bool = False,
    max_size: Optional[int] = 1024,
    quality: int = 95
) -> Dict:
    """
    Extract a single frame at a specific timestamp.
    
    Args:
        video_path: Path to video file
        timestamp: Timestamp in seconds
        output_path: Output path for the frame (optional if return_base64=True)
        return_base64: If True, return base64 encoded frame
        max_size: Maximum dimension for base64 image
        quality: Image quality (1-100)
    
    Returns:
        Dictionary with frame information
    """
    video_path = Path(video_path)
    cap = cv2.VideoCapture(str(video_path))
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_idx = int(timestamp * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    
    if not ret:
        raise ValueError(f"Failed to extract frame at {timestamp}s")
    
    # Convert to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    result = {
        "timestamp": timestamp,
        "frame_idx": frame_idx,
        "resolution": f"{frame_rgb.shape[1]}x{frame_rgb.shape[0]}"
    }
    
    # Save to file if path provided
    if output_path:
        output_path = Path(output_path)
        Image.fromarray(frame_rgb).save(output_path, quality=quality)
        result["path"] = str(output_path)
    
    # Generate base64 if requested
    if return_base64:
        if max_size and (frame_rgb.shape[0] > max_size or frame_rgb.shape[1] > max_size):
            frame_rgb = resize_image_for_base64(frame_rgb, max_size)
        result["base64"] = image_to_base64(frame_rgb, quality)
        result["base64_resolution"] = f"{frame_rgb.shape[1]}x{frame_rgb.shape[0]}"
    
    cap.release()
    return result