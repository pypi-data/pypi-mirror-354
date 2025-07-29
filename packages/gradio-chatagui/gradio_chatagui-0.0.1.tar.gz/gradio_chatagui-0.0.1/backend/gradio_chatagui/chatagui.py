from __future__ import annotations

import asyncio
import json
import uuid
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from gradio.components.base import Component, FormComponent
from gradio.events import Events

if TYPE_CHECKING:
    from gradio.components import Timer


class ChatAGUI(FormComponent):
    """
    AG-UI Chat component that supports real-time streaming and tool execution.
    """

    EVENTS = [
        Events.change,
        Events.input,
        Events.submit,
    ]

    def __init__(
        self,
        value: str | Callable | None = None,
        *,
        api_root: str = "",
        initial_thread_id: str = "",
        label: str | None = "AG-UI Chat",
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = True,
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
        Parameters:
            value: Initial value for the component.
            api_root: Root URL for the AG-UI API endpoints.
            initial_thread_id: Initial thread ID for the conversation.
            label: The label for this component.
            every: Continuously calls `value` to recalculate it if `value` is a function.
            inputs: Components that are used as inputs to calculate `value`.
            show_label: If True, will display label.
            scale: Relative size compared to adjacent Components.
            min_width: Minimum pixel width.
            interactive: If True, will be rendered as editable.
            visible: If False, component will be hidden.
            elem_id: An optional string assigned as the id of this component.
            elem_classes: An optional list of strings assigned as classes.
            render: If False, component will not be rendered.
            key: Used in gr.render for component identity across re-renders.
            preserved_by_key: Parameters preserved across re-renders.
        """
        self.api_root = api_root
        self.initial_thread_id = initial_thread_id or f"thread_{uuid.uuid4()}"
        
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
        )

    def preprocess(self, payload: Dict | None) -> Dict | None:
        """
        Parameters:
            payload: The message data from the frontend.
        Returns:
            Processed message data.
        """
        if payload is None:
            return None
        return payload

    def postprocess(self, value: str | Dict | None) -> Dict | None:
        """
        Parameters:
            value: Value to send to the frontend.
        Returns:
            The value to display in the component.
        """
        if value is None:
            return None
        
        if isinstance(value, str):
            return {"type": "message", "content": value}
        
        return value

    def api_info(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "thread_id": {"type": "string"},
                "type": {"type": "string"}
            }
        }

    def example_payload(self) -> Any:
        return {"message": "Hello, how can you help me?", "thread_id": "thread_123"}

    def example_value(self) -> Any:
        return {"type": "message", "content": "Hello! I'm ready to help."}