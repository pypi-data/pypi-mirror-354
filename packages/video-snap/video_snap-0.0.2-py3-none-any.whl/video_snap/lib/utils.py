#!/usr/bin/env python3
"""
Shared utilities for frame synchronization modules.

This module consolidates common functionality used across the frame sync system
to reduce code duplication and improve maintainability.
"""

from datetime import timedelta
from pathlib import Path
from typing import Optional

import av
import cv2
import numpy as np


def ensure_directory(path: Path) -> None:
    """
    Create directory if it doesn't exist.

    Args:
        path: Directory path to create
    """
    path.mkdir(parents=True, exist_ok=True)


def format_timestamp(seconds: float) -> str:
    """
    Format timestamp using timedelta for consistency.

    Args:
        seconds: Timestamp in seconds

    Returns:
        Formatted timestamp string (e.g. "1:23:45.67678")
    """
    return str(timedelta(seconds=seconds))


def get_video_fps_pyav(video_path: Path, default_fps: float = 29.97) -> float:
    """
    Get video frame rate using PyAV for consistent metadata extraction.

    Args:
        video_path: Path to video file
        default_fps: Default FPS to use if detection fails

    Returns:
        Frame rate in fps
    """
    try:
        with av.open(str(video_path)) as container:
            video_stream = container.streams.video[0]
            # Try multiple FPS sources in order of preference
            fps: float = (
                float(video_stream.average_rate)
                if video_stream.average_rate
                else float(video_stream.guessed_rate)
                if video_stream.guessed_rate
                else float(video_stream.base_rate)
                if video_stream.base_rate
                else default_fps
            )

            # Validate FPS is reasonable
            if 10 <= fps <= 120:
                return fps
            return default_fps

    except Exception:
        return default_fps


def create_thumbnail_cv2(img: np.ndarray, width: int) -> np.ndarray:
    """
    Create thumbnail preserving aspect ratio using OpenCV.

    Args:
        img: Input image array
        width: Target width in pixels

    Returns:
        Resized image array
    """

    h, w = img.shape[:2]
    new_height = int(h * width / w)
    return cv2.resize(img, (width, new_height), interpolation=cv2.INTER_AREA)


def create_video_capture(video_path: Path) -> "cv2.VideoCapture":
    """
    Create and validate a VideoCapture object.

    Args:
        video_path: Path to video file

    Returns:
        Opened VideoCapture object

    Raises:
        RuntimeError: If video cannot be opened
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")
    return cap


def get_video_properties(video_path: Path, cap: Optional["cv2.VideoCapture"] = None) -> dict:
    """
    Get common video properties efficiently.

    Args:
        video_path: Path to video file
        cap: Optional pre-existing VideoCapture object to use

    Returns:
        Dictionary with fps, frame_count, width, height
    """
    if cap is not None:
        # Use provided capture without creating or releasing
        return {
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }
    else:
        # Create and manage our own capture
        cap = create_video_capture(video_path)
        try:
            return {
                "fps": cap.get(cv2.CAP_PROP_FPS),
                "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            }
        finally:
            cap.release()


def read_frame_at_index(
    video_path: Path, frame_index: int, cap: Optional["cv2.VideoCapture"] = None
) -> Optional[np.ndarray]:
    """
    Read a specific frame from video efficiently.

    Args:
        video_path: Path to video file
        frame_index: Frame index to read
        cap: Optional pre-existing VideoCapture object to use

    Returns:
        Frame as numpy array or None if failed
    """
    try:
        if cap is not None:
            # Use provided capture without creating or releasing
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = cap.read()
            return frame if ret else None
        else:
            # Create and manage our own capture
            cap = create_video_capture(video_path)
            try:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                ret, frame = cap.read()
                return frame if ret else None
            finally:
                cap.release()
    except Exception:
        return None


def convert_bgr_to_gray(img: np.ndarray) -> np.ndarray:
    """
    Convert BGR image to grayscale efficiently.

    Args:
        img: BGR image array

    Returns:
        Grayscale image array
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def resize_with_aspect_ratio(img: np.ndarray, target_size: tuple, interpolation: int = cv2.INTER_AREA) -> np.ndarray:
    """
    Resize image with consistent interpolation method.

    Args:
        img: Input image array
        target_size: (width, height) tuple
        interpolation: OpenCV interpolation method

    Returns:
        Resized image array
    """
    return cv2.resize(img, target_size, interpolation=interpolation)
