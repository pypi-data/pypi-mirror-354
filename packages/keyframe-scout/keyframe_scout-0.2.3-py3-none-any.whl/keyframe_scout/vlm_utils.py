"""
Utilities for Vision Language Models (VLM) integration
"""
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import base64
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)


def extract_frames_for_vlm(
    video_path: str,
    max_frames: int = 10,
    max_size: int = 1024,
    mode: str = "adaptive"
) -> List[Dict[str, Any]]:
    """
    Extract video frames optimized for VLM usage.
    
    Args:
        video_path: Path to video file
        max_frames: Maximum number of frames to extract
        max_size: Maximum dimension for images
        mode: Extraction mode ('adaptive', 'fixed', 'interval')
    
    Returns:
        List of frame dictionaries with base64 data
    """
    from .extractor import extract_video_keyframes
    
    config = {
        'video': video_path,
        'mode': mode,
        'nframes': max_frames,
        'return_base64': True,
        'max_size': max_size,
        'include_files': False  # 不保存文件，只返回 base64
    }
    
    try:
        result = extract_video_keyframes(config)
        
        # 返回简化的格式
        frames = []
        for frame in result['frames']:
            frames.append({
                'base64': frame['base64'],
                'timestamp': frame['timestamp'],
                'index': frame['frame_idx']
            })
        
        logger.info(f"Extracted {len(frames)} frames from {video_path}")
        return frames
        
    except Exception as e:
        logger.error(f"Error extracting frames: {str(e)}")
        raise


def prepare_for_azure_openai(
    video_path: str,
    max_frames: int = 8,
    detail: str = "auto"
) -> List[Dict[str, Any]]:
    """
    Prepare video frames for Azure OpenAI GPT-4V.
    
    Args:
        video_path: Path to video file
        max_frames: Maximum number of frames
        detail: Image detail level ('low', 'high', 'auto')
    
    Returns:
        List of message content items for Azure OpenAI
    """
    # 根据 detail 级别调整大小
    if detail == "low":
        max_size = 512
    elif detail == "high":
        max_size = 2048
    else:  # auto
        max_size = 1024
    
    frames = extract_frames_for_vlm(
        video_path,
        max_frames=max_frames,
        max_size=max_size
    )
    
    # 格式化为 Azure OpenAI 格式
    content_items = []
    
    for i, frame in enumerate(frames):
        # 添加图片
        content_items.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{frame['base64']}",
                "detail": detail
            }
        })
        
        # 添加时间戳描述
        content_items.append({
            "type": "text",
            "text": f"Frame {i+1} at {frame['timestamp']:.1f}s"
        })
    
    return content_items


def create_video_messages(
    video_path: str,
    prompt: str,
    max_frames: int = 8,
    system_prompt: Optional[str] = None,
    detail: str = "auto"
) -> List[Dict[str, Any]]:
    """
    Create complete messages for Azure OpenAI chat completion.
    
    Args:
        video_path: Path to video file
        prompt: User prompt/question about the video
        max_frames: Maximum number of frames
        system_prompt: Optional system prompt
        detail: Image detail level ('low', 'high', 'auto')
    
    Returns:
        Messages list ready for Azure OpenAI API
    """
    messages = []
    
    # 添加系统提示（如果有）
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    # 获取视频帧
    content_items = prepare_for_azure_openai(video_path, max_frames, detail)
    
    # 构建用户消息
    user_content = [{"type": "text", "text": prompt}]
    user_content.extend(content_items)
    
    messages.append({
        "role": "user",
        "content": user_content
    })
    
    return messages


def create_batch_messages(
    video_paths: List[str],
    prompts: Union[str, List[str]],
    max_frames_per_video: int = 5,
    system_prompt: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Create messages for analyzing multiple videos.
    
    Args:
        video_paths: List of video file paths
        prompts: Single prompt or list of prompts
        max_frames_per_video: Max frames per video
        system_prompt: Optional system prompt
    
    Returns:
        Messages list for Azure OpenAI API
    """
    messages = []
    
    # 添加系统提示
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    # 处理 prompts
    if isinstance(prompts, str):
        prompts = [prompts] * len(video_paths)
    
    # 构建用户消息
    user_content = []
    
    for i, (video_path, prompt) in enumerate(zip(video_paths, prompts)):
        # 添加视频标识
        user_content.append({
            "type": "text",
            "text": f"\n[Video {i+1}: {Path(video_path).name}]\n{prompt}"
        })
        
        # 添加视频帧
        frames_content = prepare_for_azure_openai(
            video_path, 
            max_frames=max_frames_per_video,
            detail="low"  # 多视频时使用低分辨率
        )
        user_content.extend(frames_content)
    
    messages.append({
        "role": "user",
        "content": user_content
    })
    
    return messages


def frames_to_base64_urls(
    frames: List[Dict[str, Any]],
    detail: str = "auto"
) -> List[Dict[str, Any]]:
    """
    Convert frame dictionaries to Azure OpenAI image URL format.
    
    Args:
        frames: List of frame dictionaries with base64 data
        detail: Image detail level
    
    Returns:
        List of image_url content items
    """
    content_items = []
    
    for frame in frames:
        content_items.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{frame['base64']}",
                "detail": detail
            }
        })
    
    return content_items


def save_base64_frames(
    frames: List[Dict[str, Any]],
    output_dir: str,
    prefix: str = "frame"
) -> List[str]:
    """
    Save base64 encoded frames to files.
    
    Args:
        frames: List of frame dictionaries with base64 data
        output_dir: Output directory
        prefix: File name prefix
    
    Returns:
        List of saved file paths
    """
    from pathlib import Path
    import base64
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved_paths = []
    
    for i, frame in enumerate(frames):
        # Decode base64
        image_data = base64.b64decode(frame['base64'])
        
        # Save to file
        timestamp = frame.get('timestamp', 0)
        filename = f"{prefix}_{i+1:04d}_t{timestamp:.1f}s.jpg"
        filepath = output_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        saved_paths.append(str(filepath))
        logger.info(f"Saved frame to {filepath}")
    
    return saved_paths


def estimate_token_usage(
    frames: List[Dict[str, Any]],
    detail: str = "auto"
) -> Dict[str, int]:
    """
    Estimate token usage for GPT-4V.
    
    Based on OpenAI's pricing:
    - Low detail: 85 tokens per image
    - High detail: 170 tokens base + 170 per 512x512 tile
    
    Args:
        frames: List of frame dictionaries
        detail: Image detail level
    
    Returns:
        Dictionary with token estimates
    """
    if detail == "low":
        tokens_per_image = 85
    elif detail == "high":
        # Simplified estimate
        tokens_per_image = 765  # ~4 tiles average
    else:  # auto
        tokens_per_image = 425  # Between low and high
    
    total_tokens = len(frames) * tokens_per_image
    
    return {
        "num_images": len(frames),
        "tokens_per_image": tokens_per_image,
        "total_image_tokens": total_tokens,
        "estimated_cost_usd": total_tokens * 0.00001  # Rough estimate
    }