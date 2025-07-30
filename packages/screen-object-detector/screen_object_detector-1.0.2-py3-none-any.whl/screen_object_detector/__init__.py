from .screen_detector import ScreenDetector
from .json_handler import JSONHandler
from .cli import main as cli_main

__version__ = "1.0.2"
__author__ = "Jester"
__email__ = "thettboy11@gmail.com"
__description__ = "Real-time object detection on screen with JSON output"

__all__ = [
    "ScreenDetector",
    "JSONHandler",
    "cli_main",
]