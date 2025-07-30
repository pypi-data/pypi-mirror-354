from __future__ import annotations
from gradio.components.base import Component
from gradio.events import Events
import json

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
