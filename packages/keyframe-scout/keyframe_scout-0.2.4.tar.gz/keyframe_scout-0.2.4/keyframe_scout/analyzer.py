"""Frame analysis module for keyframe-scout"""

from __future__ import annotations

import logging
from typing import Dict, List, Tuple

import cv2
import numpy as np

from .constants import FLOW_PARAMS, SCALE_FACTOR, SCORE_WEIGHTS

logger = logging.getLogger(__name__)


def compute_frame_score(prev_frame: np.ndarray, curr_frame: np.ndarray) -> Dict[str, float]:
    """
    Compute change scores between two frames.
    
    Args:
        prev_frame: Previous frame (already scaled)
        curr_frame: Current frame (already scaled)
        
    Returns:
        Dictionary containing various scores
    """
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    
    # 1. Optical flow score (motion)
    try:
        flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, **FLOW_PARAMS)
        magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        motion_score = np.mean(magnitude) * 10
    except:
        motion_score = 0.0
    
    # 2. Scene change score
    pixel_diff = cv2.absdiff(prev_gray, curr_gray)
    scene_score = np.mean(pixel_diff)
    
    # 3. Color histogram difference
    prev_hsv = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2HSV)
    curr_hsv = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2HSV)
    hist_prev = cv2.calcHist([prev_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist_curr = cv2.calcHist([curr_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist_prev = cv2.normalize(hist_prev, hist_prev).flatten()
    hist_curr = cv2.normalize(hist_curr, hist_curr).flatten()
    color_score = cv2.compareHist(hist_prev, hist_curr, cv2.HISTCMP_CHISQR)
    
    # 4. Edge change score
    edges_prev = cv2.Canny(prev_gray, 50, 150)
    edges_curr = cv2.Canny(curr_gray, 50, 150)
    edge_diff = cv2.absdiff(edges_prev, edges_curr)
    edge_score = np.sum(edge_diff) / (edge_diff.shape[0] * edge_diff.shape[1]) * 100
    
    # Combined score
    total_score = (
        motion_score * SCORE_WEIGHTS['motion'] +
        scene_score * SCORE_WEIGHTS['scene'] +
        color_score * SCORE_WEIGHTS['color'] +
        edge_score * SCORE_WEIGHTS['edge']
    )
    
    return {
        'change_score': total_score,
        'motion_score': motion_score,
        'scene_score': scene_score,
        'color_score': color_score,
        'edge_score': edge_score
    }


def analyze_video_frames(
    video_path: str, 
    sample_rate: int = 1,
    progress_callback: callable = None
) -> Tuple[List[Dict], Dict]:
    """
    Analyze all frames in a video for changes.
    
    Args:
        video_path: Path to video file
        sample_rate: Frame sampling rate
        progress_callback: Optional callback for progress updates
        
    Returns:
        Tuple of (frame_changes, video_info)
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")
    
    # Get video info
    video_info = {
        'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    }
    video_info['duration'] = video_info['total_frames'] / video_info['fps'] if video_info['fps'] > 0 else 0
    
    logger.info(f"Video info: {video_info['total_frames']} frames, "
                f"{video_info['fps']:.2f} fps, {video_info['duration']:.2f}s")
    
    # Read first frame
    ret, first_frame = cap.read()
    if not ret:
        cap.release()
        raise ValueError("Cannot read first frame")
    
    # Downscale for faster processing
    first_frame_small = cv2.resize(first_frame, None, fx=SCALE_FACTOR, fy=SCALE_FACTOR)
    
    # Initialize frame changes list
    frame_changes = [{
        'frame_idx': 0,
        'timestamp': 0.0,
        'change_score': 0.0,
        'scene_score': 0.0,
        'motion_score': 0.0,
        'color_score': 0.0,
        'edge_score': 0.0
    }]
    
    prev_frame = first_frame_small
    frame_count = 0
    
    while True:
        # Sample frames
        for _ in range(sample_rate):
            ret = cap.grab()
            if not ret:
                break
            frame_count += 1
        
        if not ret:
            break
        
        ret, frame = cap.retrieve()
        if not ret:
            break
        
        # Downscale frame
        frame_small = cv2.resize(frame, None, fx=SCALE_FACTOR, fy=SCALE_FACTOR)
        
        # Compute scores
        scores = compute_frame_score(prev_frame, frame_small)
        
        frame_changes.append({
            'frame_idx': frame_count,
            'timestamp': frame_count / video_info['fps'],
            **scores
        })
        
        prev_frame = frame_small
        
        # Progress callback
        if progress_callback and frame_count % 50 == 0:
            progress = frame_count / video_info['total_frames']
            progress_callback(progress, frame_count, video_info['total_frames'])
        
        # Progress log
        if frame_count % 50 == 0:
            logger.info(f"Analyzed {frame_count}/{video_info['total_frames']} frames...")
    
    cap.release()
    
    logger.info(f"Frame analysis complete: {len(frame_changes)} frames analyzed")
    
    return frame_changes, video_info