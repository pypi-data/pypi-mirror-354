"""Constants for keyframe-scout"""

# Frame extraction constants
FRAME_FACTOR = 1
MIN_FRAMES = 3
MAX_FRAMES = 30
DEFAULT_INTERVAL = 10.0
DEFAULT_FPS = 2.0
SCALE_FACTOR = 0.25  # Analysis downscaling factor

# Resolution presets
RESOLUTION_MAP = {
    '1080p': (1920, 1080),
    '720p': (1280, 720),
    '480p': (854, 480),
    '360p': (640, 360),
    '240p': (426, 240)
}

# Optical flow parameters
FLOW_PARAMS = dict(
    pyr_scale=0.5,
    levels=3,
    winsize=15,
    iterations=3,
    poly_n=5,
    poly_sigma=1.2,
    flags=0
)

# Score weights for frame selection
SCORE_WEIGHTS = {
    'motion': 2.0,
    'scene': 1.5,
    'color': 0.5,
    'edge': 1.0
}

# Supported video formats
SUPPORTED_FORMATS = [
    '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv',
    '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'
]

# Output image format
DEFAULT_IMAGE_FORMAT = 'jpg'
DEFAULT_IMAGE_QUALITY = 95