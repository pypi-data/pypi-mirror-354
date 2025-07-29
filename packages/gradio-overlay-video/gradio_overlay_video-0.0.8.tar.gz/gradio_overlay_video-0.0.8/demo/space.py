
import gradio as gr
from app import demo as app
import os

_docs = {'OverlayVideo': {'description': 'An output component that plays a video with an interactive, toggleable overlay of pose data.', 'members': {'__init__': {'value': {'type': 'typing.Any', 'default': 'None', 'description': None}, 'label': {'type': 'str | None', 'default': 'None', 'description': None}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': None}, 'autoplay': {'type': 'bool', 'default': 'False', 'description': None}, 'loop': {'type': 'bool', 'default': 'False', 'description': None}, 'mode': {'type': 'str', 'default': '"overlay"', 'description': None}}, 'postprocess': {'value': {'type': 'typing.Optional[typing.Tuple[str | None, str | None]][\n    typing.Tuple[str | None, str | None][\n        str | None, str | None\n    ],\n    None,\n]', 'description': None}}, 'preprocess': {'return': {'type': 'str | None', 'description': None}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the OverlayVideo changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the OverlayVideo using the clear button for the component.'}, 'play': {'type': None, 'default': None, 'description': 'This listener is triggered when the user plays the media in the OverlayVideo.'}, 'pause': {'type': None, 'default': None, 'description': 'This listener is triggered when the media in the OverlayVideo stops for any reason.'}, 'end': {'type': None, 'default': None, 'description': 'This listener is triggered when the user reaches the end of the media playing in the OverlayVideo.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'OverlayVideo': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_overlay_video`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.8%20-%20orange">  
</div>

overlayed video controller
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_overlay_video
```

## Usage

```python

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
    \"\"\"
    This function simply validates the inputs and passes them to the
    custom OverlayVideo component for frontend processing.
    \"\"\"
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
```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `OverlayVideo`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["OverlayVideo"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["OverlayVideo"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.



 ```python
def predict(
    value: str | None
) -> typing.Optional[typing.Tuple[str | None, str | None]][
    typing.Tuple[str | None, str | None][
        str | None, str | None
    ],
    None,
]:
    return value
```
""", elem_classes=["md-custom", "OverlayVideo-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          OverlayVideo: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
