# KeyFrame Scout

[[Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[[License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[[Version](https://img.shields.io/badge/version-0.2.1-orange.svg)](https://github.com/yourusername/keyframe-scout)

An intelligent video keyframe extraction tool optimized for Vision Language Models (VLMs) and video analysis. Extract meaningful frames from videos using adaptive algorithms, with direct support for Azure OpenAI GPT and other VLMs.

## ✨ Key Features

- **🎯 Intelligent Frame Selection**: Three extraction modes (adaptive, interval, fixed) to suit different use cases
- **🤖 VLM-Ready**: Direct integration with Azure OpenAI GPT and other vision language models
- **📦 Base64 Support**: Return frames as base64 strings for immediate API usage
- **⚡ Batch Processing**: Process multiple videos efficiently with parallel execution
- **🎨 Flexible Output**: Save as files, return as base64, or both
- **📊 Smart Analysis**: Automatically identifies scene changes and important moments
- **🔧 Easy Integration**: Simple Python API and command-line interface

## 🚀 What's New in v0.2.1

- **Base64 Encoding**: Direct base64 output for VLM integration
- **Azure OpenAI Support**: Built-in integration for GPT
- **VLM Utilities**: Helper functions for preparing frames for various VLMs
- **Batch Processing**: Process entire directories of videos
- **Enhanced API**: More flexible configuration options

## 📦 Installation

### Using pip

```bash
pip install keyframe-scout
```

### From source

```bash
git clone https://github.com/yourusername/keyframe-scout.git
cd keyframe-scout
pip install -e .
```

### Dependencies

- Python 3.7+
- OpenCV (cv2)
- NumPy
- Pillow
- FFmpeg (system dependency)

Install FFmpeg:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## 🎯 Quick Start

### Basic Usage

```python
import keyframe_scout as ks

# Extract keyframes from a video
result = ks.extract_video_keyframes({
    'video': 'path/to/video.mp4',
    'output_dir': 'output/frames',
    'nframes': 10
})

print(f"Extracted {result['extracted_frames']} frames")
```

### VLM Integration (New!)

```python
import keyframe_scout as ks
from openai import AzureOpenAI

# Extract frames for GPT
frames = ks.extract_frames_for_vlm(
    'video.mp4',
    max_frames=8,
    max_size=1024
)

# Prepare messages for Azure OpenAI
messages = ks.create_video_messages(
    'video.mp4',
    prompt="What's happening in this video?",
    max_frames=8
)

# Use with Azure OpenAI
client = AzureOpenAI(
    azure_endpoint="your-endpoint",
    api_key="your-key",
    api_version="2024-02-15-preview"
)

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=messages,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### Base64 Output (New!)

```python
# Get frames as base64 strings (no files saved)
result = ks.extract_video_keyframes({
    'video': 'video.mp4',
    'nframes': 5,
    'return_base64': True,
    'max_size': 1024
})

# Access base64 data
for frame in result['frames']:
    print(f"Frame at {frame['timestamp']}s")
    base64_data = frame['base64']
    # Use base64_data with your VLM API
```

## 📖 Detailed Usage

### Extraction Modes

#### 1. Adaptive Mode (Default)
Intelligently selects the most representative frames based on content analysis.

```python
result = ks.extract_video_keyframes({
    'video': 'video.mp4',
    'output_dir': 'output',
    'mode': 'adaptive',
    'nframes': 10
})
```

#### 2. Interval Mode
Extracts frames at fixed time intervals.

```python
result = ks.extract_video_keyframes({
    'video': 'video.mp4',
    'output_dir': 'output',
    'mode': 'interval',
    'interval': 5.0,  # Every 5 seconds
    'frames_per_interval': 1
})
```

#### 3. Fixed Mode
Extracts a fixed number of evenly distributed frames.

```python
result = ks.extract_video_keyframes({
    'video': 'video.mp4',
    'output_dir': 'output',
    'mode': 'fixed',
    'frames_per_interval': 20  # Total 20 frames
})
```

### VLM Integration Examples

#### Using the VideoAnalyzer Class

```python
# Initialize analyzer
analyzer = ks.VideoAnalyzer(
    azure_endpoint="your-endpoint",
    api_key="your-key"
)

# Analyze video
result = analyzer.analyze_video(
    'video.mp4',
    prompt="Describe the main events in this video",
    max_frames=10
)

print(result)
```

#### Batch Video Analysis

```python
# Analyze multiple videos
videos = ['video1.mp4', 'video2.mp4', 'video3.mp4']
prompts = ['What happens?', 'Who appears?', 'Where is this?']

results = analyzer.batch_analyze(videos, prompts, max_frames=8)
```

#### Custom VLM Integration

```python
# Get frames for any VLM
frames = ks.extract_frames_for_vlm('video.mp4', max_frames=6)

# Prepare for your VLM API
for i, frame in enumerate(frames):
    image_data = {
        'base64': frame['base64'],
        'timestamp': frame['timestamp'],
        'description': f'Frame {i+1}'
    }
    # Send to your VLM API
```

### Batch Processing

```python
# Process all videos in a directory
results = ks.process_video_directory(
    directory='videos/',
    output_dir='output/',
    extensions=['.mp4', '.avi'],
    recursive=True,
    config_template={
        'mode': 'adaptive',
        'nframes': 10,
        'return_base64': True
    }
)

# Or process a list of videos
video_list = ['video1.mp4', 'video2.mp4', 'video3.mp4']
results = ks.extract_keyframes_batch(
    video_list,
    output_base_dir='batch_output/',
    max_workers=4
)
```

### Advanced Configuration

```python
config = {
    'video': 'video.mp4',
    'output_dir': 'output',
    'mode': 'adaptive',
    'nframes': 10,
    
    # Resolution options
    'resolution': '720p',  # '360p', '480p', '720p', '1080p', 'original'
    
    # Image options
    'image_format': 'jpg',  # 'jpg' or 'png'
    'image_quality': 95,    # 1-100 for JPEG
    
    # Base64 options (new)
    'return_base64': True,
    'include_files': False,  # Don't save files when using base64
    'max_size': 1024,       # Max dimension for base64 images
    
    # Analysis parameters
    'sample_rate': 30,      # Analyze every Nth frame
    'min_frames': 5,        # Minimum frames to extract
    'max_frames': 20        # Maximum frames to extract
}

result = ks.extract_video_keyframes(config)
```

## 🔧 Command Line Interface

### Basic usage

```bash
# Extract 10 keyframes
keyframe-scout video.mp4 -o output_frames --nframes 10

# Use specific mode
keyframe-scout video.mp4 -o output_frames --mode interval --interval 5

# Set resolution and quality
keyframe-scout video.mp4 -o output_frames --resolution 720p --quality 90
```

### Batch processing

```bash
# Process directory
keyframe-scout-batch videos/ -o batch_output/ --recursive

# With custom settings
keyframe-scout-batch videos/ -o batch_output/ --nframes 8 --resolution 480p
```

## 📊 API Reference

### Core Functions

#### `extract_video_keyframes(config)`
Main extraction function with full configuration options.

#### `extract_frames_for_vlm(video_path, max_frames, max_size, mode)`
Extract frames optimized for VLM usage, returns base64 encoded frames.

#### `create_video_messages(video_path, prompt, max_frames, system_prompt)`
Create messages formatted for Azure OpenAI GPT.

#### `get_video_info(video_path)`
Get video metadata (duration, resolution, fps, etc).

### VLM Utilities

#### `prepare_for_azure_openai(video_path, max_frames, detail)`
Prepare frames in Azure OpenAI format with detail level control.

#### `estimate_token_usage(frames, detail)`
Estimate token usage for GPT API calls.

#### `save_base64_frames(frames, output_dir, prefix)`
Save base64 encoded frames to files.

## 🎨 Examples

### Video Summary for Blog

```python
import keyframe_scout as ks

# Extract key moments from a video
frames = ks.extract_frames_for_vlm('tutorial.mp4', max_frames=6)

# Generate descriptions using GPT
analyzer = ks.VideoAnalyzer()
for i, frame in enumerate(frames):
    description = analyzer.analyze_video(
        'tutorial.mp4',
        f"Describe what's shown at {frame['timestamp']} seconds",
        max_frames=1
    )
    print(f"Time {frame['timestamp']}s: {description}")
```

### Video Content Moderation

```python
# Check video content
messages = ks.create_video_messages(
    'uploaded_video.mp4',
    prompt="Does this video contain any inappropriate content? List any concerns.",
    max_frames=10,
    system_prompt="You are a content moderation assistant."
)

# Send to your moderation API
```

### Creating Video Thumbnails

```python
# Extract best frames for thumbnails
result = ks.extract_video_keyframes({
    'video': 'video.mp4',
    'output_dir': 'thumbnails',
    'mode': 'adaptive',
    'nframes': 5,
    'resolution': '720p',
    'image_quality': 95
})

# The frames are automatically selected for maximum visual interest
```

## 🐛 Troubleshooting

### FFmpeg not found
```bash
# Install FFmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

### Import errors
```bash
# Install all dependencies
pip install keyframe-scout[all]
```

### GPU acceleration
```python
# OpenCV will automatically use GPU if available
# Check GPU availability
import cv2
print(cv2.cuda.getCudaEnabledDeviceCount())
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

```bash
# Development setup
git clone https://github.com/yourusername/keyframe-scout.git
cd keyframe-scout
pip install -e ".[dev]"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenCV community for the excellent computer vision library
- FFmpeg project for video processing capabilities
- Inspired by video analysis needs in the VLM era

## 📮 Contact

- GitHub Issues: [https://github.com/yourusername/keyframe-scout/issues](https://github.com/yourusername/keyframe-scout/issues)
- Email: your.email@example.com

---

Made with ❤️ for the VLM community