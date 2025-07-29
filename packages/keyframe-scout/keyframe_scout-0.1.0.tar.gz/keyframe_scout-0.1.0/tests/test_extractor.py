"""Tests for keyframe-scout extractor module"""

import pytest
import tempfile
import os
from pathlib import Path

import keyframe_scout as ks


class TestExtractor:
    """Test extractor functions"""
    
    def test_video_info(self, sample_video):
        """Test video info extraction"""
        info = ks.get_video_info(sample_video)
        
        assert 'duration' in info
        assert 'fps' in info
        assert 'width' in info
        assert 'height' in info
        assert info['duration'] > 0
        assert info['fps'] > 0
    
    def test_basic_extraction(self, sample_video, tmp_path):
        """Test basic keyframe extraction"""
        config = {
            'video': sample_video,
            'output_dir': str(tmp_path / 'output'),
            'nframes': 3
        }
        
        result = ks.extract_video_keyframes(config)
        
        assert result['extracted_frames'] == 3
        assert len(result['frames']) == 3
        
        # Check files exist
        for frame in result['frames']:
            assert Path(frame['path']).exists()
    
    def test_adaptive_mode(self, sample_video, tmp_path):
        """Test adaptive extraction mode"""
        config = {
            'video': sample_video,
            'output_dir': str(tmp_path / 'output'),
            'mode': 'adaptive',
            'min_frames': 2,
            'max_frames': 5
        }
        
        result = ks.extract_video_keyframes(config)
        
        assert 2 <= result['extracted_frames'] <= 5
    
    def test_resolution_options(self, sample_video, tmp_path):
        """Test different resolution options"""
        resolutions = ['original', '720p', '480p']
        
        for res in resolutions:
            config = {
                'video': sample_video,
                'output_dir': str(tmp_path / res),
                'nframes': 2,
                'resolution': res
            }
            
            result = ks.extract_video_keyframes(config)
            assert result['extracted_frames'] == 2


@pytest.fixture
def sample_video(tmp_path):
    """Create a sample video for testing"""
    # This would need to create or provide a test video
    # For actual tests, you'd have a small test video file
    video_path = tmp_path / "test_video.mp4"
    # ... create test video ...
    return str(video_path)