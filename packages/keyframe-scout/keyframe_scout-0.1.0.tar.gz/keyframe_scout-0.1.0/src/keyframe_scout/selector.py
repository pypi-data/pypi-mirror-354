"""Frame selection module for keyframe-scout"""

from __future__ import annotations

import logging
import math
from typing import Dict, List
import numpy as np

from .constants import (
    DEFAULT_INTERVAL, FRAME_FACTOR, MAX_FRAMES, MIN_FRAMES
)
from .utils import ceil_by_factor, floor_by_factor, round_by_factor

logger = logging.getLogger(__name__)


def smart_frame_count(
    duration: float, 
    mode: str = "adaptive",
    factor: int = FRAME_FACTOR,
    min_frames: int = MIN_FRAMES,
    max_frames: int = MAX_FRAMES,
    interval: float = DEFAULT_INTERVAL,
    frames_per_interval: int = 1
) -> int:
    """
    Calculate optimal number of frames to extract.
    
    Args:
        duration: Video duration in seconds
        mode: Extraction mode - "fixed", "adaptive", "interval"
        factor: Frame count factor
        min_frames: Minimum frames
        max_frames: Maximum frames
        interval: Time interval for interval mode
        frames_per_interval: Frames per interval
        
    Returns:
        Calculated frame count
    """
    if mode == "fixed":
        calculated_frames = frames_per_interval
    elif mode == "interval":
        intervals = duration / interval
        calculated_frames = int(intervals * frames_per_interval)
    elif mode == "adaptive":
        if duration <= 30:
            calculated_frames = min(5, int(duration / 5))
        elif duration <= 60:
            calculated_frames = min(8, int(duration / 7))
        elif duration <= 300:
            calculated_frames = min(15, int(duration / 15))
        else:
            calculated_frames = min(20, int(duration / 20))
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    # Ensure frame count meets constraints
    frame_count = min(max(calculated_frames, min_frames), max_frames)
    frame_count = round_by_factor(frame_count, factor)
    
    logger.info(f"Frame count calculation: duration={duration:.1f}s, mode='{mode}', frames={frame_count}")
    
    return frame_count


def select_keyframes(
    frame_changes: List[Dict], 
    n_frames: int,
    diversity_weight: float = 0.3
) -> List[Dict]:
    """
    Select most representative keyframes.
    
    Args:
        frame_changes: List of frame change information
        n_frames: Number of frames to select
        diversity_weight: Weight for temporal diversity (0-1)
        
    Returns:
        List of selected keyframes
    """
    if len(frame_changes) <= n_frames:
        return frame_changes
    
    # Sort by change score
    sorted_frames = sorted(frame_changes, key=lambda x: x['change_score'], reverse=True)
    
    selected_frames = []
    
    # Always include first frame
    selected_frames.append(frame_changes[0])
    n_frames -= 1
    
    # Calculate minimum time interval
    total_duration = frame_changes[-1]['timestamp']
    min_time_interval = max(0.5, total_duration / (n_frames * 3))
    
    # Greedy selection with diversity
    for frame in sorted_frames:
        if len(selected_frames) >= n_frames + 1:
            break
        
        # Check temporal distance
        too_close = any(
            abs(frame['timestamp'] - selected['timestamp']) < min_time_interval
            for selected in selected_frames
        )
        
        if not too_close and frame not in selected_frames:
            selected_frames.append(frame)
    
    # If not enough frames, relax constraints
    if len(selected_frames) < n_frames + 1:
        min_time_interval = max(0.2, total_duration / (n_frames * 5))
        
        for frame in sorted_frames:
            if len(selected_frames) >= n_frames + 1:
                break
            
            if frame not in selected_frames:
                too_close = any(
                    abs(frame['timestamp'] - selected['timestamp']) < min_time_interval
                    for selected in selected_frames
                )
                
                if not too_close:
                    selected_frames.append(frame)
    
    # Sort by timestamp
    selected_frames.sort(key=lambda x: x['timestamp'])
    
    # Log selected frames
    logger.info("\nSelected keyframes:")
    for i, frame in enumerate(selected_frames):
        logger.info(f"  Frame {frame['frame_idx']} "
                    f"(time: {frame['timestamp']:.2f}s, "
                    f"score: {frame['change_score']:.2f})")
    
    return selected_frames


def select_uniform_frames(frame_changes: List[Dict], n_frames: int) -> List[Dict]:
    """
    Select frames uniformly distributed across video.
    
    Args:
        frame_changes: List of frame change information
        n_frames: Number of frames to select
        
    Returns:
        List of selected frames
    """
    if len(frame_changes) <= n_frames:
        return frame_changes
    
    indices = np.linspace(0, len(frame_changes) - 1, n_frames).round().astype(int)
    return [frame_changes[i] for i in indices]


def select_threshold_frames(
    frame_changes: List[Dict], 
    threshold: float,
    min_interval: float = 1.0
) -> List[Dict]:
    """
    Select frames above a change threshold.
    
    Args:
        frame_changes: List of frame change information
        threshold: Change score threshold
        min_interval: Minimum time interval between frames
        
    Returns:
        List of selected frames
    """
    selected_frames = [frame_changes[0]]  # Always include first frame
    
    for frame in frame_changes[1:]:
        if frame['change_score'] >= threshold:
            # Check temporal distance
            too_close = any(
                abs(frame['timestamp'] - selected['timestamp']) < min_interval
                for selected in selected_frames
            )
            
            if not too_close:
                selected_frames.append(frame)
    
    return selected_frames