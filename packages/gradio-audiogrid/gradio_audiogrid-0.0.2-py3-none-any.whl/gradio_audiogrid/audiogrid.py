from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from gradio.components.base import Component, FormComponent
from gradio.data_classes import FileData
from gradio.events import Events
from gradio.i18n import I18nData

if TYPE_CHECKING:
    from gradio.components import Timer


class AudioGrid(FormComponent):
    """
    Creates a drag and drop audio file upload component with sortable squares for audio merging workflows.

    Example usage:
        import gradio as gr
        from your_module import AudioGrid

        def merge_audio_files(audio_files):
            # Process the list of audio file paths
            print(f'Received {len(audio_files)} audio files')
            for i, file_path in enumerate(audio_files):
                print(f'  {i+1}. {file_path}')
            return f'Merged {len(audio_files)} audio files successfully!'

        with gr.Blocks() as demo:
            audio_grid = AudioGrid(
                label="Upload Audio Files to Merge",
            )
            output = gr.Textbox(label="Result")
            merge_btn = gr.Button("Merge Audio Files")

            merge_btn.click(
                merge_audio_files,
                inputs=audio_grid,
                outputs=output
            )

        demo.launch()
    """

    EVENTS = [
        Events.change,
        Events.input,
        Events.submit,
        Events.upload,
    ]

    def __init__(
            self,
            value: list[str] | Callable | None = None,
            *,
            label: str | I18nData | None = None,
            every: Timer | float | None = None,
            inputs: Component | Sequence[Component] | set[Component] | None = None,
            show_label: bool | None = None,
            scale: int | None = None,
            min_width: int = 160,
            interactive: bool | None = None,
            visible: bool = True,
            elem_id: str | None = None,
            elem_classes: list[str] | str | None = None,
            render: bool = True,
            key: int | str | tuple[int | str, ...] | None = None,
            preserved_by_key: list[str] | str | None = "value",
    ):
        """
        Parameters: value: default list of audio file paths. If a function is provided, the function will be called
        each time the app loads to set the initial value of this component. label: the label for this component,
        displayed above the component if `show_label` is `True` and is also used as the header if there are a table
        of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the
        parameter this component corresponds to. every: Continuously calls `value` to recalculate it if `value` is a
        function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides
        the regular interval for the reset Timer. inputs: Components that are used as inputs to calculate `value` if
        `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.
        show_label: if True, will display label. scale: relative size compared to adjacent Components. For example if
        Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should
        be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
        min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain
        scale value results in this Component being narrower than min_width, the min_width parameter will be
        respected first. interactive: if True, will be rendered as an editable upload area; if False, editing will be
        disabled. If not provided, this is inferred based on whether the component is used as an input or output.
        visible: If False, component will be hidden. elem_id: An optional string that is assigned as the id of this
        component in the HTML DOM. Can be used for targeting CSS styles. elem_classes: An optional list of strings
        that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
        render: If False, component will not render be rendered in the Blocks context. Should be used if the
        intention is to assign event listeners now but render the component later. key: in a gr.render, Components
        with the same key across re-renders are treated as the same component, not a new component. Properties set in
        'preserved_by_key' are not reset across a re-render. preserved_by_key: A list of parameters from this
        component's constructor. Inside a gr.render() function, if a component is re-rendered with the same key,
        these (and only these) parameters will be preserved in the UI (if they have been changed by the user or an
        event listener) instead of re-rendered based on the values provided during constructor.
        """
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
        )

    def preprocess(self, payload: list[FileData] | None) -> list[str]:
        """
        Parameters:
            payload: the list of audio file objects from the component.
        Returns:
            Passes list of file paths as a list[str] into the function.
        """
        return [x['path'] for x in payload] if payload else []

    def postprocess(self, value: list[str]) -> list[FileData] | None:
        """
        Parameters:
            value: list of audio file paths to display in the component.
        Returns:
            List of FileData objects for the frontend component.
        """

        def find_original_filename(path: str) -> str:
            """Extracts the original filename from the file path."""
            return path.split("/")[-1] if path else ""

        return [FileData(path=x, orig_name=find_original_filename(x)) for x in value] if value else []

    def api_info(self) -> dict[str, Any]:
        """
        Returns the API information for this component.
        This defines how the component appears in the API documentation.
        """
        return {
            "type": "array",
            "description": "List of audio files for merging",
            "items": {
                "type": "string",
                "format": "uri",
                "description": "Audio file path or URL"
            },
            "example": [
                "/path/to/audio1.mp3",
                "/path/to/audio2.wav",
                "/path/to/audio3.m4a"
            ]
        }

    def example_payload(self) -> Any:
        """
        Returns an example payload for testing purposes.
        """
        return [
            {"path": "/path/to/sample1.mp3", "orig_name": "sample1.mp3"},
            {"path": "/path/to/sample2.wav", "orig_name": "sample2.wav"}
        ]

    def example_value(self) -> Any:
        """
        Returns an example value for the component.
        """
        return [
            "/path/to/audio1.mp3",
            "/path/to/audio2.wav",
            "/path/to/audio3.m4a"
        ]
