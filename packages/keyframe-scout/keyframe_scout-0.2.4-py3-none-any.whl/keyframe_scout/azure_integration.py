"""
Azure OpenAI integration for keyframe-scout
"""
from openai import AzureOpenAI
from typing import Optional, Dict, Any
import os

class VideoAnalyzer:
    """Video analysis using Azure OpenAI GPT-4V"""
    
    def __init__(
        self,
        azure_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: str = "2024-02-15-preview",
        deployment_name: str = "gpt-4-vision-preview"
    ):
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=api_version
        )
        self.deployment_name = deployment_name
    
    def analyze_video(
        self,
        video_path: str,
        prompt: str,
        max_frames: int = 8,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        Analyze video content using GPT-4V.
        
        Args:
            video_path: Path to video file
            prompt: Analysis prompt
            max_frames: Number of frames to extract
            temperature: Response temperature
            max_tokens: Maximum response tokens
        
        Returns:
            Analysis result text
        """
        from .vlm_utils import create_video_messages
        
        messages = create_video_messages(
            video_path=video_path,
            prompt=prompt,
            max_frames=max_frames,
            system_prompt="You are a video analysis assistant. Analyze the provided video frames and answer questions about the video content."
        )
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def batch_analyze(
        self,
        video_paths: list,
        prompts: list,
        max_frames: int = 8
    ) -> list:
        """Analyze multiple videos"""
        results = []
        
        for video_path, prompt in zip(video_paths, prompts):
            try:
                result = self.analyze_video(video_path, prompt, max_frames)
                results.append({
                    'video': video_path,
                    'analysis': result,
                    'status': 'success'
                })
            except Exception as e:
                results.append({
                    'video': video_path,
                    'error': str(e),
                    'status': 'failed'
                })
        
        return results