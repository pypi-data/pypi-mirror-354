from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from gradio.components.base import Component, FormComponent
from gradio.events import Events
from gradio.i18n import I18nData

if TYPE_CHECKING:
    from gradio.components import Timer


class GradioDesigner(Component):
    """
    A visual designer component for building Gradio layouts with all components
    """
    
    EVENTS = [Events.change, Events.input]
    
    # Complete component definitions with their properties
    COMPONENT_DEFINITIONS = {
        "Textbox": {
            "properties": ["label", "placeholder", "lines", "max_length", "type", "value"],
            "defaults": {"label": "Text Input", "placeholder": "Enter text...", "lines": 1, "value": ""},
            "icon": "📝",
            "category": "Input"
        },
        "TextArea": {
            "properties": ["label", "placeholder", "lines", "max_length", "value"],
            "defaults": {"label": "Text Area", "placeholder": "Enter multiple lines...", "lines": 3, "value": ""},
            "icon": "📄",
            "category": "Input"
        },
        "Button": {
            "properties": ["value", "variant", "size"],
            "defaults": {"value": "Click me", "variant": "secondary", "size": "sm"},
            "icon": "🔘",
            "category": "Action"
        },
        "Slider": {
            "properties": ["minimum", "maximum", "step", "value", "label"],
            "defaults": {"label": "Slider", "minimum": 0, "maximum": 100, "step": 1, "value": 50},
            "icon": "🎚️",
            "category": "Input"
        },
        "Number": {
            "properties": ["label", "value", "precision"],
            "defaults": {"label": "Number", "value": 0, "precision": 0},
            "icon": "🔢",
            "category": "Input"
        },
        "Checkbox": {
            "properties": ["label", "value"],
            "defaults": {"label": "Checkbox", "value": False},
            "icon": "☑️",
            "category": "Input"
        },
        "CheckboxGroup": {
            "properties": ["label", "choices", "value"],
            "defaults": {"label": "Checkbox Group", "choices": ["Option 1", "Option 2"], "value": []},
            "icon": "☑️",
            "category": "Input"
        },
        "Radio": {
            "properties": ["label", "choices", "value"],
            "defaults": {"label": "Radio", "choices": ["Option 1", "Option 2"], "value": "Option 1"},
            "icon": "🔘",
            "category": "Input"
        },
        "Dropdown": {
            "properties": ["label", "choices", "value", "multiselect"],
            "defaults": {"label": "Dropdown", "choices": ["Option 1", "Option 2"], "value": "Option 1", "multiselect": False},
            "icon": "📋",
            "category": "Input"
        },
        "Toggle": {
            "properties": ["label", "value"],
            "defaults": {"label": "Toggle", "value": False},
            "icon": "🔄",
            "category": "Input"
        },
        "ColorPicker": {
            "properties": ["label", "value"],
            "defaults": {"label": "Color Picker", "value": "#ff0000"},
            "icon": "🎨",
            "category": "Input"
        },
        "Date": {
            "properties": ["label", "value"],
            "defaults": {"label": "Date", "value": "2025-01-01"},
            "icon": "📅",
            "category": "Input"
        },
        "Time": {
            "properties": ["label", "value"],
            "defaults": {"label": "Time", "value": "12:00"},
            "icon": "⏰",
            "category": "Input"
        },
        "File": {
            "properties": ["label", "file_types"],
            "defaults": {"label": "Upload File", "file_types": [".txt", ".pdf"]},
            "icon": "📁",
            "category": "Input"
        },
        "Image": {
            "properties": ["label", "type", "tool", "interactive"],
            "defaults": {"label": "Image", "type": "pil", "interactive": True},
            "icon": "🖼️",
            "category": "Media"
        },
        "Video": {
            "properties": ["label", "format"],
            "defaults": {"label": "Video", "format": "mp4"},
            "icon": "🎥",
            "category": "Media"
        },
        "Audio": {
            "properties": ["label"],
            "defaults": {"label": "Audio"},
            "icon": "🎵",
            "category": "Media"
        },
        "Dataframe": {
            "properties": ["headers", "datatype", "value"],
            "defaults": {"headers": ["Column 1", "Column 2"], "datatype": ["str", "str"], "value": []},
            "icon": "📊",
            "category": "Data"
        },
        "JSON": {
            "properties": ["value"],
            "defaults": {"value": "{}"},
            "icon": "📋",
            "category": "Data"
        },
        "Markdown": {
            "properties": ["value"],
            "defaults": {"value": "# Markdown Text"},
            "icon": "📝",
            "category": "Display"
        },
        "HTML": {
            "properties": ["value"],
            "defaults": {"value": "<p>HTML Content</p>"},
            "icon": "🌐",
            "category": "Display"
        },
        "Label": {
            "properties": ["value"],
            "defaults": {"value": "Label Text"},
            "icon": "🏷️",
            "category": "Display"
        },
        "Progress": {
            "properties": ["value"],
            "defaults": {"value": 0.5},
            "icon": "📈",
            "category": "Display"
        }
    }
    
    def __init__(
        self,
        value: dict | None = None,
        label: str | None = None,
        **kwargs,
    ):
        self.value = value or {"components": [], "layout": "blocks"}
        super().__init__(label=label, **kwargs)

    def preprocess(self, payload: dict | None) -> dict | None:
        """Process the layout configuration from frontend"""
        if payload is None:
            return None
        return payload

    def postprocess(self, value: dict | None) -> dict | None:
        """Send layout configuration to frontend"""
        if value is None:
            return {"components": [], "layout": "blocks"}
        return value
    
    def api_info(self) -> dict[str, list[str]]:
        """API info for the component"""
        return {
            "info": {
                "type": "object",
                "properties": {
                    "components": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "type": {"type": "string"},
                                "position": {
                                    "type": "object",
                                    "properties": {
                                        "x": {"type": "number"},
                                        "y": {"type": "number"}
                                    }
                                },
                                "size": {
                                    "type": "object", 
                                    "properties": {
                                        "width": {"type": "number"},
                                        "height": {"type": "number"}
                                    }
                                },
                                "props": {"type": "object"}
                            }
                        }
                    },
                    "layout": {"type": "string"}
                }
            },
            "serialized_info": False
        }
    
    def get_component_definitions(self):
        """Get all component definitions for frontend"""
        return self.COMPONENT_DEFINITIONS
    
    def example_payload(self) -> dict:
        return {
            "components": [
                {
                    "id": "textbox_1",
                    "type": "Textbox", 
                    "position": {"x": 100, "y": 50},
                    "size": {"width": 200, "height": 100},
                    "props": {"label": "Input", "placeholder": "Enter text..."}
                }
            ],
            "layout": "blocks"
        }
    
    def example_value(self) -> dict:
        return self.example_payload()
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer
        from gradio.components.base import Component

    
    def change(self,
        fn: Callable[..., Any] | None = None,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        show_progress_on: Component | Sequence[Component] | None = None,
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: Timer | float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | Literal[True] | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
    
        ) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: list of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: list of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, will use the functions name as the endpoint route. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: if True, will scroll to output component on completion
            show_progress: how to show the progress animation while event is running: "full" shows a spinner which covers the output component area as well as a runtime display in the upper right corner, "minimal" only shows the runtime display, "hidden" shows no progress animation at all
            show_progress_on: Component or list of components to show the progress animation on. If None, will show the progress animation on all of the output components.
            queue: if True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: if True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: if False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: if False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: a list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            trigger_mode: if "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: if set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: if set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
            key: A unique key for this event listener to be used in @gr.render(). If set, this value identifies an event as identical across re-renders when the key is identical.
        
        """
        ...
    
    def input(self,
        fn: Callable[..., Any] | None = None,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        show_progress_on: Component | Sequence[Component] | None = None,
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: Timer | float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | Literal[True] | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
    
        ) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: list of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: list of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, will use the functions name as the endpoint route. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: if True, will scroll to output component on completion
            show_progress: how to show the progress animation while event is running: "full" shows a spinner which covers the output component area as well as a runtime display in the upper right corner, "minimal" only shows the runtime display, "hidden" shows no progress animation at all
            show_progress_on: Component or list of components to show the progress animation on. If None, will show the progress animation on all of the output components.
            queue: if True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: if True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: if False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: if False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: a list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            trigger_mode: if "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: if set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: if set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
            key: A unique key for this event listener to be used in @gr.render(). If set, this value identifies an event as identical across re-renders when the key is identical.
        
        """
        ...
