import tempfile

import gradio as gr
import numpy as np
import soundfile as sf

from gradio_audiogrid import AudioGrid


def merge_audio_files(file_objects):
    """
    Merge audio files by concatenating their audio data using soundfile

    Args:
        file_objects: List of file objects from AudioMerger component

    Returns:
        tuple: (sample_rate, merged_audio_array) for Gradio Audio component
               or (None, None) if merging fails
    """
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
        status = f"""✅ Successfully merged {len(file_objects)} audio files!
        
🎵 Result:
  • Total duration: {total_duration:.2f} seconds
  • Sample rate: {sample_rate} Hz
  • Channels: Mono
  • Format: WAV

🎧 Listen to the merged audio below!"""

        return merged_file_path, status

    except Exception as e:
        error_msg = f"❌ Error merging audio files: {str(e)}"
        return None, error_msg


def reset_everything():
    """Reset all components to initial state"""
    return [], None, "Ready to merge audio files! Upload at least 2 files to get started."


def update_file_status(file_objects):
    """Update the live status based on uploaded files"""

    if len(file_objects) == 0:
        return "No valid files uploaded"
    elif len(file_objects) == 1:
        return "📁 1 file uploaded"
    else:
        return f"📁 {len(file_objects)} files ready"


# Create the Gradio interface
with gr.Blocks(title="🎵 Professional Audio Merger") as demo:
    gr.Markdown("""
    # 🎵 Professional Audio Grid

    Upload multiple audio files and sort them. You can apply any effect you want.

    **Features:**
    - 🎯 **Drag & Drop**: Upload by dragging files or clicking
    - 🔄 **Reorder**: Drag uploaded files to change merge order  
    - 📊 **Multiple Formats**: Supports MP3, WAV, FLAC, OGG, M4A, AAC
    """)

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

            gr.Markdown("""
            **Instructions:**
            1. Upload 2+ audio files
            2. Drag to reorder if needed
            3. Click "Merge Audio Files"
            4. Listen to the result!
            """)

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

    gr.Markdown("""
    ---
    ### 🔧 Technical Details

    - **Audio Processing**: Uses SoundFile library for high-quality audio handling
    - **Concatenation**: Audio arrays are concatenated using NumPy for efficiency  
    - **Format Handling**: Automatically converts different sample rates and channels
    - **Output**: Generates WAV format for maximum compatibility
    - **Memory Efficient**: Processes files sequentially to minimize RAM usage

    **Supported Input Formats**: MP3, WAV, FLAC, OGG, M4A, AAC, and more
    **Output Format**: WAV (uncompressed, high quality)
    """)

if __name__ == "__main__":
    demo.launch(debug=True)
