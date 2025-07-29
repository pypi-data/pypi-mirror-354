# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Gradio custom component called `gradio_overlay_video` that enables interactive pose visualization overlays on video content. The component processes JSON pose data from multiple keypoint formats (MediaPipe, COCO, COCO-WholeBody, Sociopticon, YOLOv11) and renders it as interactive overlays on top of video files.

## Architecture

### Backend (`backend/gradio_overlay_video/`)
- **overlay_video.py**: Main component class `OverlayVideo` that extends Gradio's Component base class
  - Uses modular `VisualizationProcessor` to preprocess JSON data into streamlined visualization instructions
  - Supports events: change, clear, play, pause, end
- **visualization_processors.py**: Modular preprocessing system with specialized processors:
  - `JointsProcessor`: Extracts joint/keypoint positions for circle visualization
  - `BonesProcessor`: Processes skeleton connections for line visualization with auto-format detection
  - `DirectionArrowProcessor`: Creates direction arrow data from movement metrics with format-aware center calculation
  - `MotionTrailProcessor`: Generates faded motion trails from pose history
  - `LabanProcessor`: Extracts Laban Movement Analysis metrics for text overlay
  - `VisualizationProcessor`: Main coordinator that combines all processors
- **keypoint_formats.py**: Keypoint format definitions and skeleton configurations:
  - `KeypointFormat`: Enum for supported formats (MediaPipe, COCO, COCO-WholeBody, Sociopticon, YOLOv11)
  - `SkeletonDefinitions`: Skeleton connection definitions for each format
  - `KeypointFormatDetector`: Auto-detection logic based on keypoint count and structure
  - `YOLOv11DataConverter`: Converts YOLOv11 pixel coordinates to normalized format

### Frontend (`frontend/`)
- **Svelte-based** custom Gradio component using TypeScript
- **shared/InteractiveOverlay.svelte**: Handles file uploads for video and JSON
- **shared/OverlayPlayer.svelte**: Core video player with modular overlay rendering
  - Uses streamlined visualization instructions from backend
  - Supports independent toggle controls for: joints, bones, direction arrows, motion trails, Laban metrics
  - FPS-aware playback using video metadata
  - Dynamic control visibility based on data capabilities
- **shared/Video.svelte**: Base video component wrapper
- Uses @gradio/* dependencies and FFmpeg for video processing

### Demo Application (`demo/`)
- **app.py**: Example Gradio app showing component usage
- **space.py**: Hugging Face Space deployment version
- Uses sample files from `files/` directory (balette.mp4 and mediapipe JSON data)

## Common Development Commands

### Python/Backend Development
```bash
# Install in development mode
pip install -e .

# Run demo application
cd demo && python app.py

# Build package
python -m build
```

### Frontend Development
```bash
# Install frontend dependencies
cd frontend && npm install

# Build frontend components
# (No specific build command found - likely handled by Gradio's build system)
```

## Data Format Expectations

### Input JSON Structure
The component expects JSON files with this structure:
- `video_info`: Metadata about the video including `fps`, `width`, `height`, `duration_seconds`
- `movement_analysis.frames[]`: Array of frame data containing:
  - `timestamp`: Frame timing
  - `keypoints[0].points[]`: Array of pose points with x/y coordinates and confidence
  - `metrics`: Laban Movement Analysis metrics (direction, intensity, speed, velocity, etc.)

### Processed Output Structure
The backend preprocesses this into streamlined visualization instructions:
- `video_info`: Original video metadata
- `fps`: Extracted frame rate for proper playback timing
- `keypoint_format`: Detected format type (mediapipe, coco, coco_wholebody, sociopticon, yolo11_pose)
- `capabilities`: Flags indicating which visualization types are available
- `frames[]`: Array of processed frame data containing:
  - `timestamp`: Frame timing
  - `joints`: Array of joint positions for circle rendering
  - `bones`: Array of bone connections for line rendering
  - `direction_arrow`: Arrow data for movement direction visualization
  - `motion_trail`: Array of trail segments for motion path rendering
  - `laban_metrics`: Cleaned metrics for text overlay display

### Visualization Processors
Each processor can be individually enabled/disabled:
- **JointsProcessor**: Filters keypoints by confidence, extracts x/y positions
- **BonesProcessor**: Auto-detects keypoint format and uses appropriate skeleton definitions:
  - MediaPipe Pose (33 keypoints): Full face, body, and hand landmarks
  - COCO Keypoints (17 keypoints): Basic body joints
  - COCO-WholeBody (133 keypoints): Body + face + hands + feet
  - Sociopticon (18-21 keypoints): Enhanced torso detail
  - YOLOv11 Pose (17 keypoints): Uses COCO skeleton with pixel coordinate conversion
- **DirectionArrowProcessor**: Calculates body center using format-specific core points
- **MotionTrailProcessor**: Maintains trail history with configurable length and alpha values
- **LabanProcessor**: Sanitizes and formats movement analysis metrics

## Package Structure

This is a Gradio custom component package with:
- Python backend component in `/backend/gradio_overlay_video/`  
- Svelte frontend in `/frontend/`
- Demo applications in `/demo/`
- Build configuration in `pyproject.toml`
- Version: 0.0.7

## Supported Keypoint Formats

### MediaPipe Pose (33 keypoints)
- Face landmarks (nose, eyes, ears, mouth)
- Body pose (shoulders, elbows, wrists, hips, knees, ankles)
- Hand landmarks (left and right hand keypoints)
- Auto-detected when JSON contains 33 keypoints

### COCO Keypoints (17 keypoints)
- Standard COCO dataset format
- Basic body joints: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles
- Auto-detected when JSON contains 17 keypoints

### COCO-WholeBody (133 keypoints)
- Extended COCO format with additional detail
- Body (17) + Face (68) + Left Hand (21) + Right Hand (21) + Feet (6)
- Auto-detected when JSON contains 133 keypoints

### Sociopticon (18-21 keypoints)
- Custom format with enhanced torso detail
- Similar to COCO but with additional mid-torso points
- Auto-detected when JSON contains 18-21 keypoints

### YOLOv11 Pose (17 keypoints)
- YOLOv11 pose estimation format with pixel coordinates
- Uses COCO keypoint structure but with different data organization
- Auto-detected based on JSON structure (metadata.model contains "yolo" and "pose")
- Automatically converts pixel coordinates to normalized values
- Designed for single-frame pose showcase

### Format Detection
- Automatic detection based on keypoint count and structure
- Special detection for YOLOv11 based on metadata and data organization
- Fallback to MediaPipe format if detection is unclear
- Format information included in processed output for frontend reference