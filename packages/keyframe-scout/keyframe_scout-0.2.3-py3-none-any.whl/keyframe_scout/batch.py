"""
Batch processing functionality for keyframe-scout
"""
import logging
from pathlib import Path
from typing import Dict, List, Union, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .extractor import extract_video_keyframes

logger = logging.getLogger(__name__)


def extract_keyframes_batch(
    video_list: List[Union[str, Path]],
    output_base_dir: Union[str, Path],
    config_template: Optional[Dict] = None,
    max_workers: int = 4,
    show_progress: bool = True
) -> List[Dict]:
    """
    Extract keyframes from multiple videos in batch.
    
    Args:
        video_list: List of video file paths
        output_base_dir: Base output directory
        config_template: Template configuration for all videos
        max_workers: Maximum number of parallel workers
        show_progress: Show progress bar
    
    Returns:
        List of extraction results
    """
    output_base_dir = Path(output_base_dir)
    output_base_dir.mkdir(parents=True, exist_ok=True)
    
    # Default configuration
    if config_template is None:
        config_template = {
            'mode': 'adaptive',
            'nframes': 10,
            'resolution': '720p',
            'image_quality': 95
        }
    
    results = []
    failed = []
    
    # Create tasks
    tasks = []
    for video_path in video_list:
        video_path = Path(video_path)
        if not video_path.exists():
            logger.warning(f"Video file not found: {video_path}")
            failed.append({
                'video': str(video_path),
                'error': 'File not found',
                'status': 'failed'
            })
            continue
        
        # Create output directory for this video
        video_output_dir = output_base_dir / video_path.stem
        
        # Create config for this video
        config = config_template.copy()
        config['video'] = str(video_path)
        config['output_dir'] = str(video_output_dir)
        
        tasks.append((video_path, config))
    
    # Process videos
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_video = {
            executor.submit(extract_video_keyframes, config): video_path
            for video_path, config in tasks
        }
        
        # Progress bar
        if show_progress:
            futures = tqdm(
                as_completed(future_to_video),
                total=len(future_to_video),
                desc="Processing videos"
            )
        else:
            futures = as_completed(future_to_video)
        
        # Collect results
        for future in futures:
            video_path = future_to_video[future]
            try:
                result = future.result()
                result['status'] = 'success'
                results.append(result)
                logger.info(f"Successfully processed: {video_path}")
            except Exception as e:
                error_result = {
                    'video': str(video_path),
                    'error': str(e),
                    'status': 'failed'
                }
                failed.append(error_result)
                logger.error(f"Failed to process {video_path}: {e}")
    
    # Summary
    total = len(video_list)
    successful = len(results)
    failed_count = len(failed)
    
    summary = {
        'total_videos': total,
        'successful': successful,
        'failed': failed_count,
        'results': results,
        'failed_videos': failed
    }
    
    # Save summary
    summary_path = output_base_dir / 'batch_summary.json'
    import json
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Batch processing complete: {successful}/{total} videos processed successfully")
    
    return results


def process_video_directory(
    directory: Union[str, Path],
    output_dir: Union[str, Path],
    extensions: List[str] = None,
    recursive: bool = False,
    **kwargs
) -> List[Dict]:
    """
    Process all videos in a directory.
    
    Args:
        directory: Input directory containing videos
        output_dir: Output directory
        extensions: List of video extensions to process
        recursive: Process subdirectories recursively
        **kwargs: Additional arguments for extract_keyframes_batch
    
    Returns:
        List of extraction results
    """
    directory = Path(directory)
    
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    
    # Find all video files
    video_files = []
    if recursive:
        for ext in extensions:
            video_files.extend(directory.rglob(f'*{ext}'))
    else:
        for ext in extensions:
            video_files.extend(directory.glob(f'*{ext}'))
    
    if not video_files:
        logger.warning(f"No video files found in {directory}")
        return []
    
    logger.info(f"Found {len(video_files)} video files")
    
    return extract_keyframes_batch(
        video_list=video_files,
        output_base_dir=output_dir,
        **kwargs
    )