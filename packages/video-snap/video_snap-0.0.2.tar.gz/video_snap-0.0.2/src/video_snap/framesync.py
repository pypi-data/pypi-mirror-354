#!/usr/bin/env python3
"""
Hybrid Frame Synchronization Engine

An intelligent video synchronization orchestrator that combines packet-based analysis
with FAISS-accelerated visual matching to identify temporal alignment between video clips.

WHAT IT DOES
============
This module finds the exact temporal position where a distorted/trimmed video clip
originates within a longer reference video. It uses a hybrid strategy that prioritizes
ultra-fast packet analysis and falls back to visual similarity search when needed.

The system identifies synchronization points with sub-second accuracy while optimizing
for both speed and reliability across different video encoding scenarios.

HOW IT WORKS
============
The hybrid approach employs a three-phase strategy:

**Phase 1: Packet Analysis (Primary)**
• Extracts packet size patterns from both videos (metadata only, no decoding)
• Performs Z-normalized cross-correlation to identify temporal alignment patterns
• Generates ranked candidates based on packet pattern similarity
• Typically completes in 50-200ms with high accuracy for similar encodings

**Phase 2: Precise Window Verification**
• Creates focused search windows (±5s default) around top packet candidates
• Performs frame-by-frame visual similarity analysis using SSIM or MSE
• Uses optimized video seeking and batch processing for efficiency
• Accepts matches with confidence ≥0.6 to avoid unnecessary FAISS fallback

**Phase 3: FAISS Visual Fallback (When Needed)**
• Activates only when packet analysis confidence is low (<0.6)
• Builds perceptual hash index of reference video frames
• Performs sub-millisecond visual similarity search using FAISS binary indices
• Provides content-based matching robust to encoding differences

Author: Gareth Edwards (Medtronic)
"""

import argparse
from dataclasses import dataclass
from typing import Optional, List, Tuple
from pathlib import Path
import sys
import time
import tempfile
import cv2
import numpy as np

from .lib.video_frame_faiss_analyser import FAISSConfig, VideoFrameFAISSAnalyser
from .lib.video_frame_packet_analyser import VideoFramePacketAnalyser
from .lib.video_frame_ssim_analyser import SSIMConfig, VideoFrameSSIMAnalyser

from .lib.utils import (
    create_video_capture,
    format_timestamp,
    get_video_properties,
    read_frame_at_index,
)


# =====================================================================================
# CONSTANTS AND CONFIGURATION
# =====================================================================================

# Confidence thresholds
CONFIDENCE_THRESHOLD_ACCEPT = 0.6  # Accept reasonable precise matches
CONFIDENCE_EXCELLENT = 0.9  # Excellent match threshold
CONFIDENCE_GOOD = 0.8  # Good match threshold
CONFIDENCE_FAIR = 0.7  # Fair match threshold
CONFIDENCE_MODERATE = 0.6  # Moderate match threshold

# Processing limits
TOP_PACKET_CANDIDATES = 10  # Top packet matches to verify
MAX_CANDIDATES_PACKET = 100  # Maximum packet candidates to generate

# Window merging and seeking
WINDOW_MERGE_BUFFER_FRAMES = 10  # Buffer frames for window overlap detection

# Image processing
MSE_NORMALIZATION_FACTOR = 1000.0  # MSE normalization for confidence conversion
CONFIDENCE_MIN = 0.0  # Minimum confidence value
CONFIDENCE_MAX = 1.0  # Maximum confidence value

# Timing and display
SEPARATOR_LENGTH = 60  # Length of separator lines

# Default configuration values
DEFAULT_CONFIDENCE_THRESHOLD = 0.6
DEFAULT_MAX_CANDIDATES = 50
DEFAULT_TEMPLATE_LENGTH = 5000
DEFAULT_SEARCH_WINDOW = 2.5  # seconds (±1.25s)
DEFAULT_REFINE_SCALE = 640

# FAISS default settings
DEFAULT_FRAME_STEP = 5
DEFAULT_THUMB_WIDTH = 300
DEFAULT_FAISS_K = 10

# Optimization default settings
DEFAULT_ENABLE_GPU = True
DEFAULT_MIN_SEEK_DISTANCE = 30


@dataclass
class SynchronizationConfig:
    """Configuration parameters for hybrid frame synchronization."""

    method: str = "auto"
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD
    max_candidates: int = DEFAULT_MAX_CANDIDATES
    template_length: int = DEFAULT_TEMPLATE_LENGTH
    search_window: float = DEFAULT_SEARCH_WINDOW
    refine_scale: int = DEFAULT_REFINE_SCALE

    # FAISS settings
    frame_step: int = DEFAULT_FRAME_STEP
    thumb_width: int = DEFAULT_THUMB_WIDTH
    faiss_k: int = DEFAULT_FAISS_K

    # Optimization settings
    enable_gpu: bool = DEFAULT_ENABLE_GPU
    min_seek_distance: int = DEFAULT_MIN_SEEK_DISTANCE

    # Temp directory setting
    temp_dir: Optional[str] = None


@dataclass
class CandidateWindow:
    """Represents a search window around a candidate timestamp."""

    start_frame: int
    end_frame: int
    candidate_time: float
    score: float


@dataclass
class SynchronizationResult:
    """Final synchronization result with detailed metrics."""

    timestamp: float
    frame_number: int
    confidence: float
    candidates_checked: int
    execution_time: float
    method_used: str
    frames_processed: int = 0


class OptimizedVideoReader:
    """Optimized video reader with intelligent seeking capabilities."""

    def __init__(self, video_path: Path, config: SynchronizationConfig):
        self.video_path = video_path
        self.config = config
        self.cap: Optional[cv2.VideoCapture] = create_video_capture(video_path)

        # Get video properties using utility function
        props = get_video_properties(video_path, self.cap)
        self.fps = props["fps"]
        self.frame_count = props["frame_count"]
        self.current_frame = -1
        self.frames_read = 0

    def read_frame(self, frame_idx: int) -> Optional[np.ndarray]:
        """Read a specific frame using the utility function."""
        if self.cap is None:
            return None

        # Use the utility function to read the frame
        frame = read_frame_at_index(self.video_path, frame_idx, self.cap)

        # Update tracking for compatibility with existing code
        if frame is not None:
            self.current_frame = frame_idx
            self.frames_read += 1

        return frame

    def close(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None


class HybridFrameSynchronizer:
    """
    Main class for hybrid frame synchronization combining packet analysis with FAISS fallback.

    This class orchestrates the complete synchronization workflow:
    1. Packet pattern analysis for rapid candidate generation
    2. Precise window verification using visual similarity
    3. FAISS-based fallback for challenging cases

    Example usage:
        config = SynchronizationConfig(confidence_threshold=0.8)
        synchronizer = HybridFrameSynchronizer(config, verbose=True)
        result = synchronizer.synchronize(ref_path, dist_path)
        print(f"Match at {result.timestamp:.3f}s with confidence {result.confidence:.3f}")
    """

    def __init__(self, config: SynchronizationConfig, verbose: bool = False):
        """
        Initialize the hybrid frame synchronizer.

        Args:
            config: Configuration parameters for synchronization
            verbose: Enable detailed logging during processing
        """
        self.config = config
        self.verbose = verbose

    def synchronize(
        self, reference_path: Path, distorted_path: Path
    ) -> SynchronizationResult:
        """
        Execute the synchronization workflow based on the selected method.

        Args:
            reference_path: Path to reference video
            distorted_path: Path to distorted/trimmed video

        Returns:
            SynchronizationResult with timestamp, confidence, and metrics
        """
        start_time = time.time()

        if self.verbose:
            print("=" * SEPARATOR_LENGTH)
            print("HYBRID FRAME SYNCHRONIZATION")
            print("=" * SEPARATOR_LENGTH)
            print(f"Reference: {reference_path.name}")
            print(f"Distorted: {distorted_path.name}")
            print(f"Method:      {self.config.method}")

        method_map = {
            "auto": self._synchronize_auto,
            "packet": self._synchronize_packet,
            "faiss": self._synchronize_faiss,
            "ssim": self._synchronize_ssim,
        }

        sync_function = method_map.get(self.config.method)
        if not sync_function:
            raise ValueError(f"Unknown synchronization method: '{self.config.method}'")

        result = sync_function(reference_path, distorted_path)

        # Finalize result
        result.execution_time = time.time() - start_time

        # Generate final report
        self._generate_final_report(result)

        return result

    def _synchronize_auto(
        self, reference_path: Path, distorted_path: Path
    ) -> SynchronizationResult:
        """
        Execute the complete hybrid synchronization workflow (auto method).
        This is the original synchronization logic.

        Args:
            reference_path: Path to reference video
            distorted_path: Path to distorted/trimmed video

        Returns:
            SynchronizationResult with timestamp, confidence, and metrics
        """
        # Phase 1: Packet pattern analysis
        candidates, fps, method = self._analyze_packet_patterns(
            reference_path, distorted_path
        )

        # Check if packet analysis already provided verified result
        if method == "PacketAnalysis-PreciseVerified":
            if candidates:
                score, frame_num, timestamp = candidates[0]
                return SynchronizationResult(
                    timestamp=timestamp,
                    frame_number=int(frame_num),
                    confidence=score,
                    candidates_checked=1,
                    execution_time=0,  # Calculated in main synchronize method
                    method_used=method,
                    frames_processed=0,
                )

        # Phase 2: Rank candidates if needed
        if len(candidates) > 5:
            ranked_candidates = self._rank_and_filter_candidates(candidates)
        else:
            ranked_candidates = candidates

        # Phase 3: Precise verification
        result = self._verify_precise_windows(
            reference_path, distorted_path, ranked_candidates, fps
        )

        # Finalize result
        result.method_used = method

        return result

    def _synchronize_packet(
        self, ref_path: Path, dist_path: Path
    ) -> SynchronizationResult:
        """Synchronize using only packet analysis."""
        if self.verbose:
            print("\n" + "=" * SEPARATOR_LENGTH)
            print("METHOD: PACKET PATTERN ANALYSIS")
            print("=" * SEPARATOR_LENGTH)

        analyzer = VideoFramePacketAnalyser(verbose=self.verbose)
        correlation_candidates = analyzer.analyze(
            ref_path,
            dist_path,
            template_length=self.config.template_length,
            max_candidates=1,
        )

        if not correlation_candidates:
            return SynchronizationResult(0, 0, 0.0, 0, 0, "PacketAnalysis", 0)

        top = correlation_candidates[0]
        return SynchronizationResult(
            timestamp=top.timestamp,
            frame_number=int(top.frame_number),
            confidence=top.score,
            candidates_checked=len(correlation_candidates),
            execution_time=0,
            method_used="PacketAnalysis",
            frames_processed=0,
        )

    def _synchronize_faiss(
        self, ref_path: Path, dist_path: Path
    ) -> SynchronizationResult:
        """Synchronize using only FAISS."""
        candidates, _, method = self._perform_faiss_fallback(ref_path, dist_path)

        if not candidates:
            return SynchronizationResult(0, 0, 0.0, 0, 0, "FAISS-Fallback", 0)

        score, frame_num, timestamp = candidates[0]
        return SynchronizationResult(
            timestamp=timestamp,
            frame_number=int(frame_num),
            confidence=score,
            candidates_checked=1,
            execution_time=0,
            method_used=method,
            frames_processed=len(candidates),
        )

    def _synchronize_ssim(
        self, ref_path: Path, dist_path: Path
    ) -> SynchronizationResult:
        """Synchronize using a full SSIM scan."""
        return self._perform_ssim_scan(ref_path, dist_path)

    def _analyze_packet_patterns(
        self, ref_path: Path, dist_path: Path
    ) -> tuple[list[tuple[float, float, float]], float, str]:
        """
        Phase 1: Ultra-fast packet analysis with precise verification.

        Extracts packet patterns, performs correlation analysis, and verifies
        top candidates with precise window analysis. Falls back to FAISS only
        if no high-confidence match is found.

        Returns:
            Tuple of (candidates, fps, method_used)
        """
        if self.verbose:
            print("\n" + "=" * SEPARATOR_LENGTH)
            print("PHASE 1: PACKET PATTERN ANALYSIS")
            print("=" * SEPARATOR_LENGTH)

        # Create packet analyzer
        analyzer = VideoFramePacketAnalyser(verbose=self.verbose)

        # Analyze packet patterns
        correlation_candidates = analyzer.analyze(
            ref_path,
            dist_path,
            template_length=self.config.template_length,
            max_candidates=MAX_CANDIDATES_PACKET,
        )

        # Get FPS for later use
        fps = analyzer.get_video_fps(ref_path)

        # Convert CorrelationCandidate objects to tuple format for compatibility
        all_candidates = []
        for candidate in correlation_candidates:
            all_candidates.append(
                (candidate.score, float(candidate.frame_number), candidate.timestamp)
            )

        # Take top candidates for frame verification
        top_k = min(TOP_PACKET_CANDIDATES, len(all_candidates))
        top_candidates = all_candidates[:top_k]

        if self.verbose:
            print(f"\nTop {top_k} packet correlation candidates:")
            print("| Rank | Score  | Time           | Frame")
            print("|------|--------|----------------|--------")
            for i, (score, frame_num, timestamp) in enumerate(top_candidates):
                time_formatted = format_timestamp(timestamp)
                print(
                    f"| {i + 1:02d}   | {score:.4f} | {time_formatted} | {int(frame_num)}"
                )

        # Phase 2: Precise window verification
        if self.verbose:
            print("\n" + "-" * SEPARATOR_LENGTH)
            print("PHASE 2: PRECISE WINDOW VERIFICATION")
            print("-" * SEPARATOR_LENGTH)
            print(
                f"Analyzing top {len(top_candidates)} candidates with ±{self.config.search_window / 2:.1f}s windows..."
            )

        try:
            precise_result = self._verify_precise_windows(
                ref_path, dist_path, top_candidates, fps
            )

            if self.verbose:
                print(
                    f"\n- Best window match found: confidence {precise_result.confidence:.3f}"
                )

            if precise_result.confidence >= CONFIDENCE_THRESHOLD_ACCEPT:
                if self.verbose:
                    print("- Good match found - skipping FAISS indexing")
                winning_candidate = [
                    (
                        precise_result.confidence,
                        float(precise_result.frame_number),
                        float(precise_result.timestamp),
                    )
                ]
                return winning_candidate, fps, "PacketAnalysis-PreciseVerified"
            else:
                if self.verbose:
                    print(
                        f"⚠ Confidence {precise_result.confidence:.3f} below threshold {CONFIDENCE_THRESHOLD_ACCEPT}"
                    )

        except Exception as e:
            if self.verbose:
                print(f"✗ Precise verification failed: {type(e).__name__}: {str(e)}")

        # Phase 3: FAISS fallback
        return self._perform_faiss_fallback(ref_path, dist_path)

    def _perform_faiss_fallback(
        self, ref_path: Path, dist_path: Path
    ) -> tuple[list[tuple[float, float, float]], float, str]:
        """
        Phase 3: FAISS-based visual similarity fallback.

        Args:
            ref_path: Reference video path
            dist_path: Distorted video path

        Returns:
            Tuple of (faiss_candidates, fps, method_name)
        """
        if self.verbose:
            print("\n" + "-" * SEPARATOR_LENGTH)
            print("PHASE 3: FAISS VISUAL FALLBACK")
            print("-" * SEPARATOR_LENGTH)
            print("Using FAISS perceptual hashing for visual similarity search...")

        # Get temp directory from app config
        temp_dir = self.config.temp_dir
        if not temp_dir:
            temp_dir = tempfile.gettempdir()

        # Create FAISS config from main config
        faiss_config = FAISSConfig(
            frame_step=self.config.frame_step,
            thumb_width=self.config.thumb_width,
            faiss_k=self.config.faiss_k,
            enable_gpu=self.config.enable_gpu,
            cache_enabled=True,
            verbose=self.verbose,
            temp_dir=temp_dir,
        )

        # Build or load FAISS index
        indexer = VideoFrameFAISSAnalyser(ref_path, faiss_config)
        indexer.build_index()

        # Get query frame
        cap_dist = create_video_capture(dist_path)
        try:
            ret, query_frame = cap_dist.read()
            if not ret:
                raise RuntimeError("Cannot read distorted video")
        finally:
            cap_dist.release()

        # Find candidates using FAISS
        faiss_candidates = indexer.find_candidates_tuple_format(query_frame)

        # Get FPS using packet analyzer for consistency
        analyzer = VideoFramePacketAnalyser(verbose=False)
        fps = analyzer.get_video_fps(ref_path)

        if self.verbose:
            print(f"- Generated {len(faiss_candidates)} FAISS candidates")

        return faiss_candidates, fps, "FAISS-Fallback"

    def _rank_and_filter_candidates(
        self, candidates: list[tuple[float, float, float]]
    ) -> list[tuple[float, float, float]]:
        """
        Rank and filter candidates to remove duplicates and limit count.

        Args:
            candidates: List of (score, frame_num, timestamp) tuples

        Returns:
            Filtered and ranked candidate list
        """
        if self.verbose:
            print("- Ranking and filtering candidates...")

        # Sort by score, remove near-duplicates
        sorted_candidates = sorted(candidates, key=lambda x: x[0], reverse=True)
        unique_candidates: List[Tuple[float, float, float]] = []
        seen = set()

        for score, frame_num, timestamp in sorted_candidates:
            key = round(timestamp, 1)
            if key not in seen and len(unique_candidates) < self.config.max_candidates:
                unique_candidates.append((score, frame_num, timestamp))
                seen.add(key)

        if self.verbose:
            print(f"- Selected {len(unique_candidates)} unique candidates")

        return unique_candidates

    def _precompute_candidate_windows(
        self, candidates: list[tuple[float, float, float]], fps: float
    ) -> list[CandidateWindow]:
        """
        Precompute and optimize search windows for all candidates.

        Args:
            candidates: List of candidate tuples
            fps: Video frame rate

        Returns:
            List of optimized CandidateWindow objects
        """
        half_window = self.config.search_window / 2.0
        windows = []

        for score, frame_num, timestamp in candidates:
            if frame_num >= 0:
                center_frame = int(frame_num)
                half_window_frames = int(half_window * fps)
                start_frame = max(0, center_frame - half_window_frames)
                end_frame = center_frame + half_window_frames
            else:
                start_frame = max(0, int((timestamp - half_window) * fps))
                end_frame = int((timestamp + half_window) * fps)

            windows.append(
                CandidateWindow(
                    start_frame=start_frame,
                    end_frame=end_frame,
                    candidate_time=timestamp,
                    score=score,
                )
            )

        # Merge overlapping windows to minimize seeking
        return self._merge_overlapping_windows(windows)

    def _merge_overlapping_windows(
        self, windows: list[CandidateWindow]
    ) -> list[CandidateWindow]:
        """
        Merge overlapping search windows while preserving score-based order.

        Args:
            windows: List of candidate windows

        Returns:
            List of merged windows
        """
        if not windows:
            return []

        processed = []
        used_indices = set()

        for i, window in enumerate(windows):
            if i in used_indices:
                continue

            merged_window = window
            used_indices.add(i)

            # Look for overlapping windows in remaining candidates
            for j, other in enumerate(windows[i + 1 :], i + 1):
                if j in used_indices:
                    continue

                # Check for overlap (with small buffer)
                if (
                    merged_window.start_frame
                    <= other.end_frame + WINDOW_MERGE_BUFFER_FRAMES
                    and other.start_frame
                    <= merged_window.end_frame + WINDOW_MERGE_BUFFER_FRAMES
                ):
                    # Merge windows, keeping the better score
                    merged_window = CandidateWindow(
                        start_frame=min(merged_window.start_frame, other.start_frame),
                        end_frame=max(merged_window.end_frame, other.end_frame),
                        candidate_time=merged_window.candidate_time
                        if merged_window.score > other.score
                        else other.candidate_time,
                        score=max(merged_window.score, other.score),
                    )
                    used_indices.add(j)

            processed.append(merged_window)

        return processed

    def _verify_precise_windows(
        self,
        ref_path: Path,
        dist_path: Path,
        candidates: list[tuple[float, float, float]],
        fps: float,
    ) -> SynchronizationResult:
        """
        Perform precise frame verification using the SSIM analyzer.

        Args:
            ref_path: Reference video path
            dist_path: Distorted video path
            candidates: List of candidate tuples
            fps: Video frame rate

        Returns:
            SynchronizationResult with best match details
        """
        # Read query frame from distorted video
        cap_dist = create_video_capture(dist_path)
        try:
            ret, query_frame = cap_dist.read()
            if not ret:
                raise RuntimeError("Cannot read distorted video")
        finally:
            cap_dist.release()

        # Create SSIM analyzer with configuration
        ssim_config = SSIMConfig(
            refine_scale=self.config.refine_scale,
            batch_size=100,  # Process frames in batches
            min_score_threshold=0.0,  # Don't filter, we'll handle thresholds
            verbose=False,  # We'll handle verbose output ourselves
        )
        ssim_analyzer = VideoFrameSSIMAnalyser(ssim_config)

        # Precompute optimized search windows
        windows = self._precompute_candidate_windows(candidates, fps)

        best_confidence = CONFIDENCE_MIN
        best_timestamp = candidates[0][2]
        best_frame_number = 0
        total_frames_processed = 0
        candidates_checked = 0

        # Process each window
        for window_idx, window in enumerate(windows):
            window_time_formatted = format_timestamp(window.candidate_time)

            # Calculate time range for this window
            start_time_seconds = window.start_frame / fps
            end_time_seconds = window.end_frame / fps

            # Format timestamps for SSIM analyzer
            start_time_str = format_timestamp(start_time_seconds)
            end_time_str = format_timestamp(end_time_seconds)

            if self.verbose:
                print(
                    f"Window {window_idx + 1}: frames {window.start_frame}-{window.end_frame} ({window_time_formatted})"
                )

            try:
                # Analyze this window using SSIM analyzer
                ssim_candidates = ssim_analyzer.analyze_video(
                    query_frame,
                    ref_path,
                    start_time=start_time_str,
                    end_time=end_time_str,
                )

                if ssim_candidates:
                    # Get best match from this window
                    best_in_window = ssim_candidates[0]  # Already sorted by score
                    confidence = best_in_window.score

                    # Count frames processed
                    total_frames_processed += len(ssim_candidates)

                    if self.verbose:
                        time_formatted = format_timestamp(best_in_window.timestamp)
                        print(
                            f"         → confidence {confidence:.3f} at frame {best_in_window.frame_number} ({time_formatted})"
                        )

                    # Update global best
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_timestamp = best_in_window.timestamp
                        best_frame_number = best_in_window.frame_number

                    candidates_checked += 1

                    # Smart early stopping
                    if confidence >= self.config.confidence_threshold:
                        if self.verbose:
                            print("         - Confidence threshold met, stopping")
                        break
                else:
                    if self.verbose:
                        print("         → No frames found in window")

            except Exception as e:
                if self.verbose:
                    print(f"         → Error processing window: {e}")
                continue

        return SynchronizationResult(
            timestamp=best_timestamp,
            frame_number=best_frame_number,
            confidence=best_confidence,
            candidates_checked=candidates_checked,
            execution_time=total_frames_processed / fps if fps > 0 else 0.0,
            method_used="WindowVerification",
            frames_processed=total_frames_processed,
        )

    def _perform_ssim_scan(
        self, ref_path: Path, dist_path: Path
    ) -> SynchronizationResult:
        """Perform a full SSIM scan across the entire reference video."""
        if self.verbose:
            print("\n" + "=" * SEPARATOR_LENGTH)
            print("METHOD: SSIM FULL SCAN")
            print("=" * SEPARATOR_LENGTH)
            print("Performing full SSIM scan. This may be slow.")

        # Read query frame from distorted video
        cap_dist = create_video_capture(dist_path)
        try:
            ret, query_frame = cap_dist.read()
            if not ret:
                raise RuntimeError("Cannot read distorted video")
        finally:
            cap_dist.release()

        # Create SSIM analyzer
        ssim_config = SSIMConfig(
            refine_scale=self.config.refine_scale,
            batch_size=100,
            min_score_threshold=0.0,
            verbose=False,
        )
        ssim_analyzer = VideoFrameSSIMAnalyser(ssim_config)

        # Analyze the entire video
        ssim_candidates = ssim_analyzer.analyze_video(query_frame, ref_path)

        if not ssim_candidates:
            return SynchronizationResult(0, 0, 0.0, 0, 0, "SSIM-FullScan", 0)

        best = ssim_candidates[0]
        props = get_video_properties(ref_path)
        total_frames = props.get("frame_count", 0) if props else 0

        return SynchronizationResult(
            timestamp=best.timestamp,
            frame_number=best.frame_number,
            confidence=best.score,
            candidates_checked=1,
            execution_time=0,
            method_used="SSIM-FullScan",
            frames_processed=total_frames,
        )

    def _generate_final_report(self, result: SynchronizationResult) -> dict:
        """
        Generate comprehensive final report with optimization statistics.

        Args:
            result: SynchronizationResult object

        Returns:
            Dictionary with detailed analysis results
        """
        if self.verbose:
            print("\n" + "=" * SEPARATOR_LENGTH)
            print("SYNCHRONIZATION RESULTS")
            print("=" * SEPARATOR_LENGTH)

        # Quality assessment with lookup table
        quality_levels = [
            (CONFIDENCE_EXCELLENT, "Excellent", "excellent"),
            (CONFIDENCE_GOOD, "Good", "good"),
            (CONFIDENCE_FAIR, "Fair", "fair"),
            (CONFIDENCE_MODERATE, "Moderate", "moderate"),
            (CONFIDENCE_MIN, "Low", "low"),
        ]

        quality, reliability = next(
            (q, r)
            for threshold, q, r in quality_levels
            if result.confidence >= threshold
        )

        if self.verbose:
            print(
                f"Match Found: Frame {result.frame_number} at {format_timestamp(result.timestamp)}"
            )
            print(f"Confidence:  {result.confidence:.3f} ({quality})")
            print(f"Method:      {result.method_used}")
            print(f"Runtime:     {result.execution_time:.2f} seconds")

            if result.frames_processed > 0:
                throughput = result.frames_processed / result.execution_time
                print(
                    f"Performance: {result.frames_processed} frames processed at {throughput:.1f} fps"
                )

            # Add verification commands
            print("\nVerification commands:")
            print(
                f'  ffmpeg -ss {result.timestamp:.3f} -i "<reference_video>" -frames:v 1 ref_frame.png'
            )
            print('  ffmpeg -i "<distorted_video>" -frames:v 1 dist_frame.png')

        return {
            "timestamp": result.timestamp,
            "frame_number": result.frame_number,
            "confidence": result.confidence,
            "quality": quality,
            "reliability": reliability,
            "candidates_checked": result.candidates_checked,
            "execution_time": result.execution_time,
            "method_used": result.method_used,
            "frames_processed": result.frames_processed,
            "throughput_fps": result.frames_processed / result.execution_time
            if result.execution_time > 0
            else 0,
        }


# =====================================================================================
# CONVENIENCE FUNCTIONS FOR BACKWARD COMPATIBILITY
# =====================================================================================


def hybrid_sync(
    reference_path: Path, distorted_path: Path, config: SynchronizationConfig
) -> SynchronizationResult:
    """
    Convenience function for backward compatibility.

    Args:
        reference_path: Path to reference video
        distorted_path: Path to distorted video
        config: Synchronization configuration

    Returns:
        SynchronizationResult object
    """
    synchronizer = HybridFrameSynchronizer(config, verbose=True)
    return synchronizer.synchronize(reference_path, distorted_path)


# =====================================================================================
# MAIN FUNCTION AND CLI INTERFACE
# =====================================================================================


def main():
    """Streamlined main function for hybrid frame synchronization."""
    parser = argparse.ArgumentParser(
        description="Hybrid frame synchronization with packet analysis and FAISS fallback"
    )
    parser.add_argument("reference", type=Path, help="Reference video")
    parser.add_argument("distorted", type=Path, help="Distorted video")
    parser.add_argument(
        "--method",
        type=str,
        default="auto",
        choices=["auto", "packet", "faiss", "ssim"],
        help='Synchronization method. "auto" (default): Packet analysis with FAISS fallback and SSIM verification. "packet": Packet analysis only. "faiss": FAISS analysis only. "ssim": Full SSIM scan.',
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=DEFAULT_CONFIDENCE_THRESHOLD,
    )
    parser.add_argument("--max-candidates", type=int, default=DEFAULT_MAX_CANDIDATES)
    parser.add_argument("--template-length", type=int, default=DEFAULT_TEMPLATE_LENGTH)
    parser.add_argument(
        "--search-window",
        type=float,
        default=DEFAULT_SEARCH_WINDOW,
        help="Search window size in seconds",
    )
    parser.add_argument(
        "--faiss-k",
        type=int,
        default=DEFAULT_FAISS_K,
        help="Number of FAISS candidates",
    )
    parser.add_argument(
        "--frame-step",
        type=int,
        default=DEFAULT_FRAME_STEP,
        help="FAISS index frame step",
    )
    parser.add_argument(
        "--thumb-width",
        type=int,
        default=DEFAULT_THUMB_WIDTH,
        help="Thumbnail width for perceptual hashing",
    )
    parser.add_argument(
        "--min-seek-distance",
        type=int,
        default=DEFAULT_MIN_SEEK_DISTANCE,
        help="Minimum seek distance to avoid thrashing",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--temp-dir",
        type=str,
        help="Temporary directory for cache files (default: system temp dir)",
    )

    args = parser.parse_args()

    config = SynchronizationConfig(
        method=args.method,
        confidence_threshold=args.confidence_threshold,
        max_candidates=args.max_candidates,
        template_length=args.template_length,
        search_window=args.search_window,
        faiss_k=args.faiss_k,
        frame_step=args.frame_step,
        thumb_width=args.thumb_width,
        min_seek_distance=args.min_seek_distance,
        temp_dir=getattr(args, "temp_dir", None),
    )

    try:
        synchronizer = HybridFrameSynchronizer(config, verbose=args.verbose)
        result = synchronizer.synchronize(args.reference, args.distorted)

        if args.verbose:
            print(f"\n- Method used: {result.method_used}")

    except Exception as e:
        print(f"[X] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
