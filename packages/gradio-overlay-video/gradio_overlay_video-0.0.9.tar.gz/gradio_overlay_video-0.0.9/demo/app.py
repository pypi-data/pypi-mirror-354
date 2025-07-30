
import gradio as gr
from gradio_overlay_video import OverlayVideo
from pathlib import Path

DEMO_DIR = Path(__file__).parent.parent
sample_video_path = DEMO_DIR / "files/balette.mp4"
sample_json_path = DEMO_DIR / "files/mediapipe_full_kp_balette.json"
mediapipe_json_path = DEMO_DIR / "files/mediapipe_heavy_kp_parkour.json"
movenet_json_path = DEMO_DIR / "files/movenet_thunder_kp_skate.json"
yolo8_json_path = DEMO_DIR / "files/yolov8_kp_dance.json"
yolo11_json_path = DEMO_DIR / "files/yolov11.json"

def prepare_visualization_data(json_path, video_path):
    """
    This function simply validates the inputs and passes them to the
    custom OverlayVideo component for frontend processing.
    """
    if not json_path:
        raise gr.Error("A JSON file is required to generate a visualization.")

    print(f"✅ Preparing visualization with JSON: {json_path}")
    if video_path:
        print(f"✅ Video background provided: {video_path}")
    else:
        print("ℹ️ No video background provided. Visualization will be on a black background.")

    # The backend's job is just to pass the filepaths to the frontend.
    # The return format (video_path, json_path) must match what postprocess expects.
    return (video_path, json_path)


with gr.Blocks(theme=gr.themes.Default(primary_hue="rose", secondary_hue="pink")) as demo:
    gr.Markdown(
        "# 🩰 Interactive Pose Visualization\n"
        "1. **Upload a JSON file** with pose data.\n"
        "2. **(Optional) Upload a video** to use as the background.\n"
        "3. Click 'Display Visualization' to see the interactive result."
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            # Use standard gr.File for robust input handling
            json_upload = gr.File(
                label="Upload Required JSON File",
                file_types=[".json"],
                type="filepath"
            )
            video_upload = gr.File(
                label="Upload Optional Video File",
                file_types=["video"],
                type="filepath",
                value=None 
            )
            btn = gr.Button("Display Visualization", variant="primary")
        
        with gr.Column(scale=1):
            output_ov = OverlayVideo(label="Output", interactive=False, autoplay=True)

    btn.click(
        fn=prepare_visualization_data,
        inputs=[json_upload, video_upload],
        outputs=[output_ov]
    )
    
    gr.Examples(
        examples=[
            [str(mediapipe_json_path), None],
            [str(movenet_json_path), None],
            [str(yolo8_json_path), None],
            [str(sample_json_path), str(sample_video_path)],
            [str(yolo11_json_path), None]
        ],
        inputs=[json_upload, video_upload],
        outputs=output_ov,
        fn=prepare_visualization_data,
        cache_examples=True
    )

if __name__ == "__main__":
    demo.launch(allowed_paths=["/Users/csabi/Develop/overlay_video/files"])