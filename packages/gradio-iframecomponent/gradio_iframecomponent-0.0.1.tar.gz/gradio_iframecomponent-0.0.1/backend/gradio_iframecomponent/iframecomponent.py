from __future__ import annotations
from typing import Any, Callable, Literal
import gradio as gr
from gradio.components.base import Component
from gradio.events import Events

class IFrame(Component):
    """
    A custom Gradio component for embedding iframes.
    """
    
    EVENTS = [Events.change, Events.input]
    
    def __init__(
        self,
        value: str = "",
        *,
        src: str | None = None,
        width: str | int = "100%", 
        height: str | int = 400,
        sandbox: str | None = None,
        interactive: bool = True,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        label: str | None = None,
        show_label: bool = True,
        **kwargs,
    ):
        self.src = src
        self.width = width
        self.height = height
        self.sandbox = sandbox or "allow-scripts allow-same-origin"
        
        super().__init__(
            value=value,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            label=label,
            show_label=show_label,
            **kwargs,
        )

    def preprocess(self, payload: str | None) -> str | None:
        """Process input from frontend to backend."""
        return payload

    def postprocess(self, value: str | None) -> str | None:
        """Process output from backend to frontend."""
        if value is None:
            return None
            
        if self.src or (value.startswith('http') and '<iframe' not in value):
            url = self.src or value
            return f"""
            <iframe 
                src="{url}"
                width="{self.width}"
                height="{self.height}"
                sandbox="{self.sandbox}"
                frameborder="0"
            ></iframe>
            """
        return value

    def example_payload(self) -> Any:
        """Example input for API usage - must be JSON-serializable."""
        return "https://www.gradio.app"

    def example_value(self) -> Any:
        """Example value for component development."""
        return "https://www.gradio.app"

    def api_info(self) -> dict[str, Any]:
        """JSON-schema representation for API."""
        return {"type": "string"}
