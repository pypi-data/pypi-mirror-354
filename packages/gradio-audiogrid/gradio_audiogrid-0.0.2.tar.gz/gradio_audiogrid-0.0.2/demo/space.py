
import gradio as gr
from app import demo as app
import os

_docs = {'AudioGrid': {'description': 'Creates a drag and drop audio file upload component with sortable squares for audio merging workflows.\n\nExample usage:\n    import gradio as gr\n    from your_module import AudioGrid\n\n    def merge_audio_files(audio_files):\n        # Process the list of audio file paths\n        print(f\'Received {len(audio_files)} audio files\')\n        for i, file_path in enumerate(audio_files):\n            print(f\'  {i+1}. {file_path}\')\n        return f\'Merged {len(audio_files)} audio files successfully!\'\n\n    with gr.Blocks() as demo:\n        audio_grid = AudioGrid(\n            label="Upload Audio Files to Merge",\n        )\n        output = gr.Textbox(label="Result")\n        merge_btn = gr.Button("Merge Audio Files")\n\n        merge_btn.click(\n            merge_audio_files,\n            inputs=audio_grid,\n            outputs=output\n        )\n\n    demo.launch()', 'members': {'__init__': {'value': {'type': 'list[str] | Callable | None', 'default': 'None', 'description': 'default list of audio file paths. If a function is provided, the function will be called'}, 'label': {'type': 'str | I18nData | None', 'default': 'None', 'description': 'the label for this component,'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continuously calls `value` to recalculate it if `value` is a'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': 'Components that are used as inputs to calculate `value` if'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label. scale: relative size compared to adjacent Components. For example if'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will be rendered as an editable upload area; if False, editing will be'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden. elem_id: An optional string that is assigned as the id of this'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the'}, 'key': {'type': 'int | str | tuple[int | str, ...] | None', 'default': 'None', 'description': 'in a gr.render, Components'}, 'preserved_by_key': {'type': 'list[str] | str | None', 'default': '"value"', 'description': 'A list of parameters from this'}}, 'postprocess': {'value': {'type': 'list[str] | None', 'description': 'list of audio file paths to display in the component.'}}, 'preprocess': {'return': {'type': 'list[str]', 'description': 'Passes list of file paths as a list[str] into the function.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the AudioGrid changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the AudioGrid.'}, 'submit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses the Enter key while the AudioGrid is focused.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the AudioGrid.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'AudioGrid': []}}}

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
# `gradio_audiogrid`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Audio Grid - Gradio component for drag and drop audio file management and merging workflows
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_audiogrid
```

## Usage

```python
import tempfile

import gradio as gr
import numpy as np
import soundfile as sf

from gradio_audiogrid import AudioGrid


def merge_audio_files(file_objects):
    \"\"\"
    Merge audio files by concatenating their audio data using soundfile

    Args:
        file_objects: List of file objects from AudioMerger component

    Returns:
        tuple: (sample_rate, merged_audio_array) for Gradio Audio component
               or (None, None) if merging fails
    \"\"\"
    if not file_objects or len(file_objects) == 0:
        return None, "❌ No audio files to merge"

    if len(file_objects) == 1:
        return None, "❌ Please upload at least 2 audio files to merge"

    try:
        _merged_audio = []
        sample_rate = None

        for i, file_path in enumerate(file_objects):
            # Read audio file
            audio_data, sr = sf.read(file_path)
            if sample_rate is None:
                sample_rate = sr
            elif sr != sample_rate:
                ratio = sample_rate / sr
                new_length = int(len(audio_data) * ratio)
                audio_data = np.interp(
                    np.linspace(0, len(audio_data), new_length),
                    np.arange(len(audio_data)),
                    audio_data
                )

            # Convert stereo to mono if needed (take average of channels)
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)

            _merged_audio.append(audio_data)
        if not _merged_audio:
            return None, "❌ No valid audio files found"

        # Concatenate all audio arrays
        final_audio = np.concatenate(_merged_audio)

        # Create temporary file for the merged audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            sf.write(tmp_file.name, final_audio, sample_rate)
            merged_file_path = tmp_file.name

        # Create status message
        total_duration = len(final_audio) / sample_rate
        status = f\"\"\"✅ Successfully merged {len(file_objects)} audio files!
        
🎵 Result:
  • Total duration: {total_duration:.2f} seconds
  • Sample rate: {sample_rate} Hz
  • Channels: Mono
  • Format: WAV

🎧 Listen to the merged audio below!\"\"\"

        return merged_file_path, status

    except Exception as e:
        error_msg = f"❌ Error merging audio files: {str(e)}"
        return None, error_msg


def reset_everything():
    \"\"\"Reset all components to initial state\"\"\"
    return [], None, "Ready to merge audio files! Upload at least 2 files to get started."


def update_file_status(file_objects):
    \"\"\"Update the live status based on uploaded files\"\"\"

    if len(file_objects) == 0:
        return "No valid files uploaded"
    elif len(file_objects) == 1:
        return "📁 1 file uploaded"
    else:
        return f"📁 {len(file_objects)} files ready"


# Create the Gradio interface
with gr.Blocks(title="🎵 Professional Audio Merger") as demo:
    gr.Markdown(\"\"\"
    # 🎵 Professional Audio Grid

    Upload multiple audio files and sort them. You can apply any effect you want.

    **Features:**
    - 🎯 **Drag & Drop**: Upload by dragging files or clicking
    - 🔄 **Reorder**: Drag uploaded files to change merge order  
    - 📊 **Multiple Formats**: Supports MP3, WAV, FLAC, OGG, M4A, AAC
    \"\"\")

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 📁 Upload & Arrange Audio Files")

            audio_files = AudioGrid(
                value=[],
                label="Drag files here or click to upload",
                interactive=True,
                elem_classes=["audio-merger-container"]
            )

            # Live status update
            file_status = gr.Textbox(
                value="No files uploaded yet",
                label="📊 Upload Status",
                interactive=False,
                lines=2
            )

        with gr.Column(scale=1):
            gr.Markdown("### 🎛️ Controls")

            merge_btn = gr.Button(
                "🎵 Merge Audio Files",
                variant="primary",
                size="lg",
                elem_classes=["merge-button"]
            )

            clear_btn = gr.Button(
                "🗑️ Clear All",
                variant="secondary",
                size="lg"
            )

            gr.Markdown(\"\"\"
            **Instructions:**
            1. Upload 2+ audio files
            2. Drag to reorder if needed
            3. Click "Merge Audio Files"
            4. Listen to the result!
            \"\"\")

    gr.Markdown("### 🎧 Merged Audio Result")

    with gr.Row():
        with gr.Column(scale=2):
            # Status/info output
            merge_status = gr.Textbox(
                value="Ready to merge audio files! Upload at least 2 files to get started.",
                label="🔍 Merge Status & Details",
                interactive=False,
                lines=8
            )

        with gr.Column(scale=2):
            # Audio output
            merged_audio = gr.Audio(
                label="🎵 Merged Audio Player",
                type="filepath",
                interactive=False
            )

    # Event handlers
    merge_btn.click(
        fn=merge_audio_files,
        inputs=audio_files,
        outputs=[merged_audio, merge_status]
    )

    clear_btn.click(
        fn=reset_everything,
        outputs=[audio_files, merged_audio, merge_status]
    )

    # Live update of file status
    audio_files.change(
        fn=update_file_status,
        inputs=audio_files,
        outputs=file_status
    )

    gr.Markdown(\"\"\"
    ---
    ### 🔧 Technical Details

    - **Audio Processing**: Uses SoundFile library for high-quality audio handling
    - **Concatenation**: Audio arrays are concatenated using NumPy for efficiency  
    - **Format Handling**: Automatically converts different sample rates and channels
    - **Output**: Generates WAV format for maximum compatibility
    - **Memory Efficient**: Processes files sequentially to minimize RAM usage

    **Supported Input Formats**: MP3, WAV, FLAC, OGG, M4A, AAC, and more
    **Output Format**: WAV (uncompressed, high quality)
    \"\"\")

if __name__ == "__main__":
    demo.launch(debug=True)

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `AudioGrid`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["AudioGrid"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["AudioGrid"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes list of file paths as a list[str] into the function.
- **As output:** Should return, list of audio file paths to display in the component.

 ```python
def predict(
    value: list[str]
) -> list[str] | None:
    return value
```
""", elem_classes=["md-custom", "AudioGrid-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          AudioGrid: [], };
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
