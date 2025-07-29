# KeyFrame Scout 🎬

[![PyPI version](https://badge.fury.io/py/keyframe-scout.svg)](https://badge.fury.io/py/keyframe-scout)
[![Python Support](https://img.shields.io/pypi/pyversions/keyframe-scout.svg)](https://pypi.org/project/keyframe-scout/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Intelligent video keyframe extraction tool that automatically identifies and extracts the most representative frames from videos using motion, scene, and content analysis.

## ✨ Features

- **Smart Frame Selection**: Automatically identifies frames with significant changes using optical flow, scene detection, and content analysis
- **Multiple Extraction Modes**:
  - `adaptive`: Automatically adjusts frame count based on video duration
  - `interval`: Extract frames at fixed time intervals
  - `fixed`: Extract a specific number of frames
- **Resolution Control**: Output frames at original or preset resolutions (1080p, 720p, 480p, etc.)
- **Batch Processing**: Process multiple videos in one command
- **Flexible Output**: Support for JPEG and PNG with quality control
- **Progress Tracking**: Real-time analysis progress updates

## 📦 Installation

```bash
pip install keyframe-scout