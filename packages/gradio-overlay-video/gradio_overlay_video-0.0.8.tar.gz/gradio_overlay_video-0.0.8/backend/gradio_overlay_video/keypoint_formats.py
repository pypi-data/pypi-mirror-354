"""
Keypoint format definitions and skeleton configurations for different pose estimation models.
Supports: MediaPipe, COCO, COCO-WholeBody, and Sociopticon formats.
"""

from typing import Dict, List, Tuple, Optional
from enum import Enum


class KeypointFormat(Enum):
    """Supported keypoint formats."""
    MEDIAPIPE = "mediapipe"
    COCO = "coco"
    COCO_WHOLEBODY = "coco_wholebody"
    SOCIOPTICON = "sociopticon"
    YOLO11_POSE = "yolo11_pose"


class SkeletonDefinitions:
    """Skeleton connection definitions for different keypoint formats."""
    
    # MediaPipe pose skeleton connections (33 keypoints)
    MEDIAPIPE_SKELETON = [
        # Face connections
        (0, 1), (1, 2), (2, 3), (3, 7),  # left eye region
        (0, 4), (4, 5), (5, 6), (6, 8),  # right eye region
        (9, 10),  # mouth
        # Upper body
        (11, 12),  # shoulders
        (11, 13), (13, 15),  # left arm
        (12, 14), (14, 16),  # right arm
        (11, 23), (12, 24),  # shoulders to hips
        (23, 24),  # hips
        # Lower body
        (23, 25), (25, 27), (27, 29), (27, 31),  # left leg
        (24, 26), (26, 28), (28, 30), (28, 32),  # right leg
        # Hands
        (15, 17), (15, 19), (15, 21),  # left hand
        (16, 18), (16, 20), (16, 22),  # right hand
    ]
    
    # COCO keypoint skeleton connections (17 keypoints)
    # Order: nose, left_eye, right_eye, left_ear, right_ear, left_shoulder, right_shoulder,
    #        left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip,
    #        left_knee, right_knee, left_ankle, right_ankle
    COCO_SKELETON = [
        # Head connections
        (0, 1), (0, 2),  # nose to eyes
        (1, 3), (2, 4),  # eyes to ears
        # Upper body
        (5, 6),  # shoulders
        (5, 7), (7, 9),  # left arm
        (6, 8), (8, 10),  # right arm
        (5, 11), (6, 12),  # shoulders to hips
        (11, 12),  # hips
        # Lower body
        (11, 13), (13, 15),  # left leg
        (12, 14), (14, 16),  # right leg
    ]
    
    # COCO-WholeBody skeleton connections (133 keypoints total)
    # Body (17) + Face (68) + Left Hand (21) + Right Hand (21) + Feet (6)
    COCO_WHOLEBODY_SKELETON = [
        # Body connections (same as COCO)
        (0, 1), (0, 2), (1, 3), (2, 4),  # head
        (5, 6),  # shoulders
        (5, 7), (7, 9),  # left arm
        (6, 8), (8, 10),  # right arm
        (5, 11), (6, 12),  # shoulders to hips
        (11, 12),  # hips
        (11, 13), (13, 15),  # left leg
        (12, 14), (14, 16),  # right leg
        
        # Face outline connections (simplified from 68 points for performance)
        (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26),  # jaw
        (27, 28), (28, 29), (29, 30),  # nose bridge
        (31, 32), (32, 33), (33, 34), (34, 35),  # nose
        (36, 37), (37, 38), (38, 39), (39, 40), (40, 41), (41, 36),  # left eye
        (42, 43), (43, 44), (44, 45), (45, 46), (46, 47), (47, 42),  # right eye
        (48, 49), (49, 50), (50, 51), (51, 52), (52, 53), (53, 54), (54, 55), (55, 56), (56, 57), (57, 58), (58, 59), (59, 48),  # outer lip
        (60, 61), (61, 62), (62, 63), (63, 64), (64, 65), (65, 66), (66, 67), (67, 60),  # inner lip
        
        # Left hand connections (21 points starting at index 91)
        (91, 92), (92, 93), (93, 94), (94, 95),  # thumb
        (91, 96), (96, 97), (97, 98), (98, 99),  # index finger
        (91, 100), (100, 101), (101, 102), (102, 103),  # middle finger
        (91, 104), (104, 105), (105, 106), (106, 107),  # ring finger
        (91, 108), (108, 109), (109, 110), (110, 111),  # pinky
        
        # Right hand connections (21 points starting at index 112)
        (112, 113), (113, 114), (114, 115), (115, 116),  # thumb
        (112, 117), (117, 118), (118, 119), (119, 120),  # index finger
        (112, 121), (121, 122), (122, 123), (123, 124),  # middle finger
        (112, 125), (125, 126), (126, 127), (127, 128),  # ring finger
        (112, 129), (129, 130), (130, 131), (131, 132),  # pinky
    ]
    
    # Sociopticon skeleton connections (assuming extended COCO-like format)
    SOCIOPTICON_SKELETON = [
        # Head connections
        (0, 1), (0, 2), (1, 3), (2, 4),  # head structure
        # Upper body with more detail
        (5, 6),  # shoulders
        (5, 7), (7, 9),  # left arm
        (6, 8), (8, 10),  # right arm
        (5, 11), (6, 12),  # shoulders to hips
        (11, 12),  # hips
        # Additional torso points (if available)
        (5, 17), (6, 18),  # shoulder to mid-torso
        (17, 18), (17, 11), (18, 12),  # torso connections
        # Lower body
        (11, 13), (13, 15),  # left leg
        (12, 14), (14, 16),  # right leg
    ]
    
    @classmethod
    def get_skeleton(cls, format_type: KeypointFormat) -> List[Tuple[int, int]]:
        """Get skeleton connections for the specified format."""
        if format_type == KeypointFormat.MEDIAPIPE:
            return cls.MEDIAPIPE_SKELETON
        elif format_type == KeypointFormat.COCO:
            return cls.COCO_SKELETON
        elif format_type == KeypointFormat.COCO_WHOLEBODY:
            return cls.COCO_WHOLEBODY_SKELETON
        elif format_type == KeypointFormat.SOCIOPTICON:
            return cls.SOCIOPTICON_SKELETON
        elif format_type == KeypointFormat.YOLO11_POSE:
            return cls.COCO_SKELETON  # YOLOv11 uses COCO format
        else:
            return cls.MEDIAPIPE_SKELETON  # default


class KeypointFormatDetector:
    """Detects keypoint format based on data structure and keypoint count."""
    
    # Core body point indices for different formats (used for center calculation)
    CORE_POINT_INDICES = {
        KeypointFormat.MEDIAPIPE: [11, 12, 23, 24],     # shoulders and hips
        KeypointFormat.COCO: [5, 6, 11, 12],            # shoulders and hips
        KeypointFormat.COCO_WHOLEBODY: [5, 6, 11, 12],  # shoulders and hips (body part)
        KeypointFormat.SOCIOPTICON: [5, 6, 11, 12],     # shoulders and hips
        KeypointFormat.YOLO11_POSE: [5, 6, 11, 12]      # shoulders and hips (COCO format)
    }
    
    @classmethod
    def detect_format(cls, points: List[Dict]) -> KeypointFormat:
        """
        Detect keypoint format based on number of points and structure.
        
        Args:
            points: List of keypoint dictionaries
            
        Returns:
            Detected KeypointFormat
        """
        num_points = len(points)
        
        # Detect based on keypoint count
        if num_points == 17:
            return KeypointFormat.COCO
        elif num_points == 133:
            return KeypointFormat.COCO_WHOLEBODY
        elif num_points == 33:
            return KeypointFormat.MEDIAPIPE
        elif num_points in [18, 19, 20, 21]:  # Sociopticon variations
            return KeypointFormat.SOCIOPTICON
        
        # Additional heuristics based on keypoint names (if available)
        if points and isinstance(points[0], dict):
            first_point = points[0]
            if 'name' in first_point:
                name = first_point['name'].lower()
                if 'nose' in name:
                    # MediaPipe uses 'nose', COCO uses indices
                    return KeypointFormat.MEDIAPIPE
        
        # Default fallback
        return KeypointFormat.MEDIAPIPE
    
    @classmethod
    def detect_yolo11_format(cls, data: Dict) -> bool:
        """
        Detect if data is in YOLOv11 format based on structure.
        
        Args:
            data: Raw JSON data dictionary
            
        Returns:
            True if YOLOv11 format detected
        """
        # Check for YOLOv11 specific structure
        if 'metadata' in data and 'keypoints' in data:
            metadata = data['metadata']
            if isinstance(metadata, dict) and 'model' in metadata:
                model_name = metadata['model'].lower()
                if 'yolo' in model_name and 'pose' in model_name:
                    return True
            
            # Check keypoints structure: should be list of lists of [x,y] coordinates
            keypoints = data['keypoints']
            if isinstance(keypoints, list) and len(keypoints) > 0:
                first_frame = keypoints[0]
                if isinstance(first_frame, list) and len(first_frame) == 17:
                    # Check if points are [x,y] coordinate pairs
                    first_point = first_frame[0]
                    if isinstance(first_point, list) and len(first_point) == 2:
                        return True
        
        return False
    
    @classmethod
    def get_core_points(cls, format_type: KeypointFormat) -> List[int]:
        """Get core body point indices for center calculation."""
        return cls.CORE_POINT_INDICES.get(format_type, cls.CORE_POINT_INDICES[KeypointFormat.MEDIAPIPE])
    
    @classmethod
    def format_info(cls, format_type: KeypointFormat) -> Dict:
        """Get information about a keypoint format."""
        info = {
            KeypointFormat.MEDIAPIPE: {
                "name": "MediaPipe Pose",
                "keypoints": 33,
                "description": "Google MediaPipe pose estimation with face, body, and hand landmarks"
            },
            KeypointFormat.COCO: {
                "name": "COCO Keypoints",
                "keypoints": 17,
                "description": "COCO dataset keypoint format with basic body joints"
            },
            KeypointFormat.COCO_WHOLEBODY: {
                "name": "COCO-WholeBody",
                "keypoints": 133,
                "description": "Extended COCO format with face, hands, and feet keypoints"
            },
            KeypointFormat.SOCIOPTICON: {
                "name": "Sociopticon",
                "keypoints": "18-21",
                "description": "Sociopticon keypoint format with enhanced torso detail"
            },
            KeypointFormat.YOLO11_POSE: {
                "name": "YOLOv11 Pose",
                "keypoints": 17,
                "description": "YOLOv11 pose estimation with COCO format keypoints and pixel coordinates"
            }
        }
        
        return info.get(format_type, info[KeypointFormat.MEDIAPIPE])


class YOLOv11DataConverter:
    """Converts YOLOv11 pose data to standard format."""
    
    @classmethod
    def convert_to_standard_format(cls, yolo_data: Dict, video_width: int = 1920, video_height: int = 1080) -> Dict:
        """
        Convert YOLOv11 format to standard format expected by visualization processors.
        
        Args:
            yolo_data: Raw YOLOv11 JSON data
            video_width: Video width for coordinate normalization (default: 1920)
            video_height: Video height for coordinate normalization (default: 1080)
            
        Returns:
            Dictionary in standard format
        """
        # Extract first frame keypoints (YOLOv11 data contains list of frames)
        if 'keypoints' not in yolo_data or not yolo_data['keypoints']:
            raise ValueError("No keypoints found in YOLOv11 data")
        
        first_frame_keypoints = yolo_data['keypoints'][0]
        
        # Convert to standard point format
        points = []
        for i, point_coords in enumerate(first_frame_keypoints):
            x, y = point_coords
            
            # Check if point is valid (YOLOv11 uses [0,0] for invalid points)
            if x == 0 and y == 0:
                # Invalid point - set low confidence
                points.append({
                    'x': 0.0,
                    'y': 0.0,
                    'confidence': 0.0,
                    'index': i
                })
            else:
                # Valid point - normalize coordinates and set high confidence
                points.append({
                    'x': x / video_width,  # Normalize to 0-1 range
                    'y': y / video_height,  # Normalize to 0-1 range
                    'confidence': 0.9,  # Default high confidence for valid points
                    'index': i
                })
        
        # Create standard format structure for single frame
        converted_data = {
            'video_info': {
                'fps': 30,  # Default FPS for single frame
                'width': video_width,
                'height': video_height,
                'duration_seconds': 0.033  # Single frame duration
            },
            'movement_analysis': {
                'frames': [
                    {
                        'timestamp': 0.0,
                        'keypoints': [
                            {
                                'points': points
                            }
                        ],
                        'metrics': {
                            'direction': 'stationary',
                            'intensity': 0.0,
                            'speed': 0.0,
                            'velocity': {'x': 0, 'y': 0}
                        }
                    }
                ]
            }
        }
        
        return converted_data
    
    @classmethod
    def estimate_video_dimensions(cls, keypoints: List[List[float]]) -> Tuple[int, int]:
        """
        Estimate video dimensions based on keypoint coordinates.
        
        Args:
            keypoints: List of [x, y] coordinate pairs
            
        Returns:
            Tuple of (width, height) estimates
        """
        valid_points = [point for point in keypoints if point[0] > 0 or point[1] > 0]
        
        if not valid_points:
            return 1920, 1080  # Default dimensions
        
        max_x = max(point[0] for point in valid_points)
        max_y = max(point[1] for point in valid_points)
        
        # Add some margin and round to common video dimensions
        estimated_width = int(max_x * 1.2)
        estimated_height = int(max_y * 1.2)
        
        # Round to common video dimensions
        common_widths = [1920, 1280, 854, 640]
        common_heights = [1080, 720, 480, 360]
        
        # Find closest common dimensions
        width = min(common_widths, key=lambda w: abs(w - estimated_width))
        height = min(common_heights, key=lambda h: abs(h - estimated_height))
        
        return width, height