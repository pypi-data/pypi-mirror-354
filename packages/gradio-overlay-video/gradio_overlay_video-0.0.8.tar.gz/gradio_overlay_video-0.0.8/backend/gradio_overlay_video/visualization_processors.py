"""
Visualization processors for different overlay types.
Each processor extracts and prepares specific visualization data from JSON.
Supports multiple keypoint formats: MediaPipe, COCO, COCO-WholeBody, Sociopticon.
"""

from typing import Dict, List, Any, Optional, Tuple
import math
from dataclasses import dataclass
from .keypoint_formats import KeypointFormat, SkeletonDefinitions, KeypointFormatDetector, YOLOv11DataConverter


@dataclass
class VisualizationFrame:
    """Unified frame data structure for all visualization types."""
    timestamp: float
    joints: Optional[List[Dict]] = None
    bones: Optional[List[Dict]] = None
    direction_arrow: Optional[Dict] = None
    motion_trail: Optional[List[Dict]] = None
    laban_metrics: Optional[Dict] = None


class JointsProcessor:
    """Processes joint/keypoint data for circle visualization."""
    
    def process_frame(self, frame_data: Dict) -> Optional[List[Dict]]:
        """Extract joint positions from frame data."""
        keypoints_data = frame_data.get('keypoints', [])
        if not keypoints_data or not keypoints_data[0].get('points'):
            return None
        
        joints = []
        points = keypoints_data[0]['points']
        
        for point in points:
            x = point.get('x', 0)
            y = point.get('y', 0)
            confidence = point.get('confidence', 0)
            
            # Filter out low confidence points and 0,0 coordinates (invalid detections)
            if confidence > 0.3 and not (x == 0 and y == 0):
                joints.append({
                    'x': x,
                    'y': y,
                    'confidence': confidence,
                    'name': point.get('name', '')
                })
        
        return joints if joints else None


class BonesProcessor:
    """Processes skeleton/bone connections for line visualization."""
    
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
    # Order: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles
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
        
        # Face outline (simplified from 68 points)
        (17, 18), (18, 19), (19, 20), (20, 21),  # jaw line (partial)
        (22, 23), (23, 24), (24, 25), (25, 26),  # eyebrow left
        (27, 28), (28, 29), (29, 30), (30, 31),  # eyebrow right
        (36, 37), (37, 38), (38, 39), (39, 40), (40, 41), (41, 36),  # left eye
        (42, 43), (43, 44), (44, 45), (45, 46), (46, 47), (47, 42),  # right eye
        (48, 49), (49, 50), (50, 51), (51, 52), (52, 53),  # mouth outline (partial)
        
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
    
    # Sociopticon skeleton connections (custom format)
    # Assuming similar to COCO but with additional torso detail
    SOCIOPTICON_SKELETON = [
        # Head connections
        (0, 1), (0, 2), (1, 3), (2, 4),  # head structure
        # Upper body with more detail
        (5, 6),  # shoulders
        (5, 7), (7, 9),  # left arm
        (6, 8), (8, 10),  # right arm
        (5, 11), (6, 12),  # shoulders to hips
        (11, 12),  # hips
        # Torso detail (if available)
        (5, 17), (6, 18),  # shoulder to mid-torso
        (17, 18), (17, 11), (18, 12),  # torso connections
        # Lower body
        (11, 13), (13, 15),  # left leg
        (12, 14), (14, 16),  # right leg
    ]
    
    def __init__(self):
        self.detected_format: Optional[KeypointFormat] = None
    
    def detect_keypoint_format(self, points: List[Dict]) -> KeypointFormat:
        """Detect the keypoint format based on number of points and structure."""
        return KeypointFormatDetector.detect_format(points)
    
    def get_skeleton_connections(self, format_type: KeypointFormat) -> List[Tuple[int, int]]:
        """Get skeleton connections for the specified format."""
        return SkeletonDefinitions.get_skeleton(format_type)
    
    def process_frame(self, frame_data: Dict) -> Optional[List[Dict]]:
        """Extract bone connections from frame data with auto-format detection."""
        keypoints_data = frame_data.get('keypoints', [])
        if not keypoints_data or not keypoints_data[0].get('points'):
            return None
        
        points = keypoints_data[0]['points']
        
        # Auto-detect keypoint format if not already detected
        if not self.detected_format:
            self.detected_format = self.detect_keypoint_format(points)
            format_info = KeypointFormatDetector.format_info(self.detected_format)
            print(f"Detected keypoint format: {format_info['name']} ({len(points)} points)")
        
        # Get appropriate skeleton connections
        skeleton_connections = self.get_skeleton_connections(self.detected_format)
        
        # Try index-based approach first (more reliable for standard formats)
        bones = self._process_by_index(points, skeleton_connections)
        
        # Fallback to name-based approach if index-based fails
        if not bones:
            bones = self._process_by_name(points, skeleton_connections)
        
        return bones if bones else None
    
    def _process_by_index(self, points: List[Dict], skeleton_connections: List[Tuple[int, int]]) -> List[Dict]:
        """Process skeleton connections using point indices."""
        bones = []
        
        for connection in skeleton_connections:
            idx1, idx2 = connection
            
            # Check if indices are valid
            if idx1 < len(points) and idx2 < len(points):
                p1 = points[idx1]
                p2 = points[idx2]
                
                p1_x, p1_y = p1.get('x', 0), p1.get('y', 0)
                p2_x, p2_y = p2.get('x', 0), p2.get('y', 0)
                p1_conf, p2_conf = p1.get('confidence', 0), p2.get('confidence', 0)
                
                # Check confidence, validity, and filter out 0,0 coordinates
                if (p1_conf > 0.3 and p2_conf > 0.3 and
                    not math.isnan(p1_x) and not math.isnan(p1_y) and
                    not math.isnan(p2_x) and not math.isnan(p2_y) and
                    not (p1_x == 0 and p1_y == 0) and
                    not (p2_x == 0 and p2_y == 0)):
                    
                    bones.append({
                        'start': {'x': p1_x, 'y': p1_y},
                        'end': {'x': p2_x, 'y': p2_y},
                        'confidence': min(p1_conf, p2_conf),
                        'connection': f"{idx1}-{idx2}",
                        'format': self.detected_format.value
                    })
        
        return bones
    
    def _process_by_name(self, points: List[Dict], skeleton_connections: List[Tuple[int, int]]) -> List[Dict]:
        """Fallback: Process skeleton connections using point names (MediaPipe style)."""
        # Create lookup dict by keypoint name
        points_by_name = {p.get('name', ''): p for p in points}
        
        # Get keypoint names in order
        keypoint_names = [p.get('name', '') for p in points]
        
        bones = []
        
        for connection in skeleton_connections:
            idx1, idx2 = connection
            
            if idx1 < len(keypoint_names) and idx2 < len(keypoint_names):
                name1 = keypoint_names[idx1]
                name2 = keypoint_names[idx2]
                
                if name1 in points_by_name and name2 in points_by_name:
                    p1 = points_by_name[name1]
                    p2 = points_by_name[name2]
                    
                    p1_x, p1_y = p1.get('x', 0), p1.get('y', 0)
                    p2_x, p2_y = p2.get('x', 0), p2.get('y', 0)
                    p1_conf, p2_conf = p1.get('confidence', 0), p2.get('confidence', 0)
                    
                    # Check confidence, validity, and filter out 0,0 coordinates
                    if (p1_conf > 0.3 and p2_conf > 0.3 and
                        not math.isnan(p1_x) and not math.isnan(p1_y) and
                        not math.isnan(p2_x) and not math.isnan(p2_y) and
                        not (p1_x == 0 and p1_y == 0) and
                        not (p2_x == 0 and p2_y == 0)):
                        
                        bones.append({
                            'start': {'x': p1_x, 'y': p1_y},
                            'end': {'x': p2_x, 'y': p2_y},
                            'confidence': min(p1_conf, p2_conf),
                            'connection': f"{name1}-{name2}",
                            'format': self.detected_format.value
                        })
        
        return bones


class DirectionArrowProcessor:
    """Processes movement direction data for arrow visualization."""
    
    def process_frame(self, frame_data: Dict) -> Optional[Dict]:
        """Extract direction arrow data from frame metrics."""
        metrics = frame_data.get('metrics', {})
        keypoints_data = frame_data.get('keypoints', [])
        
        direction = metrics.get('direction', 'stationary')
        if direction == 'stationary':
            return None
        
        # Calculate body center from keypoints
        if keypoints_data and keypoints_data[0].get('points'):
            points = keypoints_data[0]['points']
            valid_points = [p for p in points 
                          if p.get('confidence', 0) > 0.3 and 
                             not math.isnan(p.get('x', 0)) and 
                             not math.isnan(p.get('y', 0)) and
                             not (p.get('x', 0) == 0 and p.get('y', 0) == 0)]
            
            if valid_points:
                center_x = sum(p['x'] for p in valid_points) / len(valid_points)
                center_y = sum(p['y'] for p in valid_points) / len(valid_points)
                
                # Direction vectors (normalized coordinates)
                direction_vectors = {
                    'up': (0, -0.1),
                    'down': (0, 0.1),
                    'left': (-0.1, 0),
                    'right': (0.1, 0),
                }
                
                if direction in direction_vectors:
                    dx, dy = direction_vectors[direction]
                    
                    return {
                        'start': {'x': center_x, 'y': center_y},
                        'end': {'x': center_x + dx, 'y': center_y + dy},
                        'direction': direction,
                        'intensity': metrics.get('intensity', 'medium'),
                        'speed': metrics.get('speed', 'medium'),
                        'velocity': metrics.get('velocity', 0)
                    }
        
        return None


class MotionTrailProcessor:
    """Processes motion trail data for path visualization."""
    
    def __init__(self, trail_length: int = 10):
        self.trail_length = trail_length
        self.trails = {}  # Store trails for each keypoint
    
    def process_frame(self, frame_data: Dict, frame_index: int) -> Optional[List[Dict]]:
        """Extract and update motion trail data."""
        keypoints_data = frame_data.get('keypoints', [])
        if not keypoints_data or not keypoints_data[0].get('points'):
            return None
        
        points = keypoints_data[0]['points']
        
        # Update trails for each keypoint
        for point in points:
            x, y = point.get('x', 0), point.get('y', 0)
            confidence = point.get('confidence', 0)
            
            # Filter out low confidence and 0,0 coordinates
            if confidence > 0.3 and not (x == 0 and y == 0):
                name = point.get('name', '')
                if name not in self.trails:
                    self.trails[name] = []
                
                # Add current position to trail
                self.trails[name].append({
                    'x': x,
                    'y': y,
                    'frame': frame_index
                })
                
                # Keep only recent positions
                if len(self.trails[name]) > self.trail_length:
                    self.trails[name] = self.trails[name][-self.trail_length:]
        
        # Create trail segments for drawing
        trail_segments = []
        for joint_name, trail in self.trails.items():
            if len(trail) >= 2:
                for i in range(1, len(trail)):
                    p1 = trail[i-1]
                    p2 = trail[i]
                    
                    # Calculate alpha based on age
                    alpha = i / len(trail)
                    
                    trail_segments.append({
                        'start': {'x': p1['x'], 'y': p1['y']},
                        'end': {'x': p2['x'], 'y': p2['y']},
                        'alpha': alpha,
                        'joint': joint_name
                    })
        
        return trail_segments if trail_segments else None


class LabanProcessor:
    """Processes Laban Movement Analysis data for text and visual overlays."""
    
    def process_frame(self, frame_data: Dict) -> Optional[Dict]:
        """Extract Laban notation metrics from frame data."""
        metrics = frame_data.get('metrics', {})
        if not metrics:
            return None
        
        # Extract and clean metrics
        def safe_value(val, default=0):
            if isinstance(val, (int, float)) and not math.isnan(val):
                return val
            return default
        
        laban_data = {
            'direction': metrics.get('direction', 'stationary'),
            'intensity': metrics.get('intensity', 'low'),
            'speed': metrics.get('speed', 'slow'),
            'velocity': safe_value(metrics.get('velocity'), 0),
            'acceleration': safe_value(metrics.get('acceleration'), 0),
            'fluidity': safe_value(metrics.get('fluidity'), 0),
            'expansion': safe_value(metrics.get('expansion'), 0),
            'total_displacement': safe_value(metrics.get('total_displacement'), 0)
        }
        
        # Add center displacement if available
        center_displacement = metrics.get('center_displacement')
        if center_displacement:
            laban_data['center_displacement'] = {
                'x': safe_value(center_displacement.get('x'), 0),
                'y': safe_value(center_displacement.get('y'), 0)
            }
        
        return laban_data


class VisualizationProcessor:
    """Main processor that coordinates all visualization types."""
    
    def __init__(self, 
                 enable_joints: bool = True,
                 enable_bones: bool = True,
                 enable_direction_arrows: bool = True,
                 enable_motion_trails: bool = True,
                 enable_laban: bool = True,
                 trail_length: int = 10):
        
        self.enable_joints = enable_joints
        self.enable_bones = enable_bones
        self.enable_direction_arrows = enable_direction_arrows
        self.enable_motion_trails = enable_motion_trails
        self.enable_laban = enable_laban
        self.detected_format = None
        
        # Initialize processors
        self.joints_processor = JointsProcessor() if enable_joints else None
        self.bones_processor = BonesProcessor() if enable_bones else None
        self.direction_processor = DirectionArrowProcessor() if enable_direction_arrows else None
        self.trail_processor = MotionTrailProcessor(trail_length) if enable_motion_trails else None
        self.laban_processor = LabanProcessor() if enable_laban else None
    
    def process_json_data(self, json_data: Dict) -> Dict:
        """Process full JSON data and return streamlined visualization instructions."""
        # Check if this is YOLOv11 format and convert if needed
        if KeypointFormatDetector.detect_yolo11_format(json_data):
            print("Detected YOLOv11 pose format - converting to standard format...")
            
            # Estimate video dimensions from keypoints
            if 'keypoints' in json_data and json_data['keypoints']:
                first_frame_keypoints = json_data['keypoints'][0]
                video_width, video_height = YOLOv11DataConverter.estimate_video_dimensions(first_frame_keypoints)
                print(f"Estimated video dimensions: {video_width}x{video_height}")
            else:
                video_width, video_height = 1920, 1080  # Default
            
            # Convert YOLOv11 to standard format
            json_data = YOLOv11DataConverter.convert_to_standard_format(
                json_data, video_width, video_height
            )
            print("YOLOv11 data converted successfully")
        
        video_info = json_data.get('video_info', {})
        source_frames = json_data.get('movement_analysis', {}).get('frames', [])
        
        processed_frames = []
        
        for frame_index, frame in enumerate(source_frames):
            viz_frame = VisualizationFrame(
                timestamp=frame.get('timestamp', 0)
            )
            
            # Process each visualization type
            if self.joints_processor:
                viz_frame.joints = self.joints_processor.process_frame(frame)
            
            if self.bones_processor:
                viz_frame.bones = self.bones_processor.process_frame(frame)
            
            if self.direction_processor:
                viz_frame.direction_arrow = self.direction_processor.process_frame(frame)
            
            if self.trail_processor:
                viz_frame.motion_trail = self.trail_processor.process_frame(frame, frame_index)
            
            if self.laban_processor:
                viz_frame.laban_metrics = self.laban_processor.process_frame(frame)
            
            # Convert to dict for JSON serialization
            processed_frames.append({
                'timestamp': viz_frame.timestamp,
                'joints': viz_frame.joints,
                'bones': viz_frame.bones,
                'direction_arrow': viz_frame.direction_arrow,
                'motion_trail': viz_frame.motion_trail,
                'laban_metrics': viz_frame.laban_metrics
            })
        
        # Get detected format from bones processor
        detected_format = None
        if self.bones_processor and hasattr(self.bones_processor, 'detected_format'):
            detected_format = self.bones_processor.detected_format
        
        return {
            'video_info': video_info,
            'fps': video_info.get('fps', 30),  # Extract FPS for frontend
            'frames': processed_frames,
            'keypoint_format': detected_format.value if detected_format else None,  # Add detected format info
            'capabilities': {
                'has_joints': self.enable_joints,
                'has_bones': self.enable_bones,
                'has_direction_arrows': self.enable_direction_arrows,
                'has_motion_trails': self.enable_motion_trails,
                'has_laban': self.enable_laban
            }
        }