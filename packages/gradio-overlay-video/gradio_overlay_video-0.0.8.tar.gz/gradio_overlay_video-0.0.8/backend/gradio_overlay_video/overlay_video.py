# backend/gradio_overlay_video/overlay_video.py

from __future__ import annotations
from pathlib import Path
from typing import Any, Callable, Optional, Tuple
import json

from gradio_client import handle_file
from gradio_client.documentation import document
import gradio as gr
from gradio.components.base import Component
from gradio.data_classes import FileData, GradioModel
from gradio.events import Events

# This data model expects the raw, pre-processed JSON string
class OverlayVideoData(GradioModel):
    video: Optional[FileData] = None
    json_data: Optional[str] = None


@document()
class OverlayVideo(Component):
    """An output component that plays a video with an interactive, toggleable overlay of pose data."""
    
    data_model = OverlayVideoData
    EVENTS = [Events.change, Events.clear, Events.play, Events.pause, Events.end]

    def __init__(
        self,
        value: Any = None,
        *,
        label: str | None = None,
        interactive: bool | None = None,
        autoplay: bool = False,
        loop: bool = False,
        mode: str = "overlay", # Custom prop for the frontend
        **kwargs
    ):
        self.autoplay = autoplay
        self.loop = loop
        self.mode = mode
        super().__init__(label=label, interactive=interactive, value=value, **kwargs)

    def preprocess(self, payload: OverlayVideoData | None) -> str | None:
        """
        This component is output-only, so preprocess does nothing.
        It is required to satisfy the abstract class requirements.
        """
        # We return None because this component does not handle input.
        return None

    def postprocess(self, value: Tuple[str | None, str | None] | None) -> OverlayVideoData | None:
        """
        Takes video and JSON file paths, preprocesses the JSON with visualization processors,
        and sends streamlined visualization instructions to the frontend.
        """
        if value is None or value[1] is None:
            return None

        video_path, json_path = value
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                full_data = json.load(f)

            # Import and use the new visualization processor
            from .visualization_processors import VisualizationProcessor
            
            # Initialize processor with all visualization types enabled
            processor = VisualizationProcessor(
                enable_joints=True,
                enable_bones=True,
                enable_direction_arrows=True,
                enable_motion_trails=True,
                enable_laban=True,
                trail_length=10
            )
            
            # Process the JSON data into streamlined visualization instructions
            visualization_data = processor.process_json_data(full_data)
            
            # Convert to JSON string for frontend
            json_content = json.dumps(visualization_data)

        except Exception as e:
            print(f"Error processing JSON file: {e}")
            import traceback
            print(traceback.format_exc())
            return None

        return OverlayVideoData(
            video=handle_file(video_path) if video_path else None,
            json_data=json_content
        )

    def example_payload(self) -> Any: return None
    def example_value(self) -> Any: return None