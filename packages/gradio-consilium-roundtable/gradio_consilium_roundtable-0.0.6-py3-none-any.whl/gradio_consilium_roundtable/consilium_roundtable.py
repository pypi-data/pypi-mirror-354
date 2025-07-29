from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any
import json

from gradio.components.base import Component, FormComponent
from gradio.events import Events
from gradio.i18n import I18nData

if TYPE_CHECKING:
    from gradio.components import Timer


class consilium_roundtable(FormComponent):
    """
    Creates a visual roundtable component for AI consensus discussions.
    
    Displays AI participants as avatars positioned around an oval table
    with animated speech bubbles, thinking states, and real-time discussion updates.
    Perfect for multi-AI collaboration, decision-making processes, and consensus building.
    
    Supports custom avatar images with emoji fallbacks for enhanced visual representation.
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
        placeholder: str | None = None,
        label: str | I18nData | None = None,
        label_icon: str | None = "🎭",
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 600,
        visible: bool = True,
        rtl: bool = False,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
        preserved_by_key: list[str] | str | None = "value",
    ):
        """
        Parameters:
            value: JSON string containing the discussion state with participants, messages, current speaker, thinking states, and avatar images. If a function is provided, it will be called each time the app loads to set the initial value.
            placeholder: Not used in this component (roundtable displays participants instead).
            label: The label for this component, displayed above the roundtable.
            label_icon: Icon displayed next to the label. Can be an emoji (default: "🎭") or a URL to an image. Set to None to disable.
            every: Continuously calls `value` to recalculate it if `value` is a function (useful for live discussion updates).
            inputs: Components that are used as inputs to calculate `value` if `value` is a function.
            show_label: If True, will display the label above the roundtable.
            scale: Relative size compared to adjacent components in a Row or Blocks layout.
            min_width: Minimum pixel width for the component (default 600px for proper roundtable display).
            visible: If False, component will be hidden.
            rtl: Not used in this component.
            elem_id: An optional string assigned as the id of this component in the HTML DOM.
            elem_classes: Optional list of CSS classes assigned to this component.
            render: If False, component will not be rendered in the Blocks context initially.
            key: For gr.render() - components with the same key are treated as the same component across re-renders.
            preserved_by_key: Parameters preserved across re-renders when using keys.
        """
        self.placeholder = placeholder
        self.rtl = rtl
        self.label_icon = label_icon
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
        )

    def preprocess(self, payload: str | None) -> str | None:
        """
        Parameters:
            payload: JSON string from the frontend containing user interactions or state changes.
        Returns:
            Passes the JSON string value for processing.
        """
        return None if payload is None else str(payload)

    def postprocess(self, value: Any) -> str:
        """
        Convert discussion state to proper JSON string for frontend.
        
        Parameters:
            value: Discussion state as dict or JSON string containing:
                - participants: List of AI model names (e.g., ["Claude", "GPT-4", "Mistral"])
                - messages: List of message objects with speaker and text
                - currentSpeaker: Name of currently speaking participant (or null)
                - thinking: List of participants currently in thinking state
                - showBubbles: List of participants whose bubbles should remain visible
                - avatarImages: Dict mapping participant names to image URLs (optional)
        
        Returns:
            Clean JSON string for frontend consumption.
        """
        if value is None:
            return json.dumps({
                "participants": [], 
                "messages": [], 
                "currentSpeaker": None, 
                "thinking": [], 
                "showBubbles": [], 
                "avatarImages": {}
            })
        
        if isinstance(value, dict):
            # Ensure all required fields are present
            processed_value = {
                "participants": value.get("participants", []),
                "messages": value.get("messages", []),
                "currentSpeaker": value.get("currentSpeaker"),
                "thinking": value.get("thinking", []),
                "showBubbles": value.get("showBubbles", []),
                "avatarImages": value.get("avatarImages", {})
            }
            return json.dumps(processed_value)
        elif isinstance(value, str):
            try:
                parsed = json.loads(value)
                # Ensure avatarImages field exists
                if "avatarImages" not in parsed:
                    parsed["avatarImages"] = {}
                return json.dumps(parsed)
            except json.JSONDecodeError:
                return json.dumps({
                    "participants": [], 
                    "messages": [], 
                    "currentSpeaker": None, 
                    "thinking": [], 
                    "showBubbles": [], 
                    "avatarImages": {}
                })
        
        return json.dumps(value)

    def api_info(self) -> dict[str, Any]:
        return {
            "type": "string",
            "description": "JSON string containing AI discussion state with optional avatar images",
            "example": json.dumps({
                "participants": ["Claude", "GPT-4"], 
                "messages": [{"speaker": "Claude", "text": "Hello"}], 
                "currentSpeaker": "Claude", 
                "thinking": [],
                "showBubbles": [],
                "avatarImages": {
                    "Claude": "https://example.com/claude-avatar.png",
                    "GPT-4": "https://example.com/gpt4-avatar.png"
                }
            })
        }

    def example_payload(self) -> Any:
        return json.dumps({
            "participants": ["Claude", "GPT-4", "Mistral"],
            "messages": [
                {"speaker": "Claude", "text": "I think we should consider multiple perspectives on this issue."},
                {"speaker": "GPT-4", "text": "That's a solid foundation. Let me add some analysis..."}
            ],
            "currentSpeaker": "GPT-4",
            "thinking": ["Mistral"],
            "showBubbles": ["Claude"],
            "avatarImages": {
                "Claude": "https://example.com/claude.png",
                "GPT-4": "https://example.com/gpt4.png"
            }
        })

    def example_value(self) -> Any:
        return json.dumps({
            "participants": ["Claude", "GPT-4", "Mistral", "Gemini", "Search"],
            "messages": [
                {"speaker": "Claude", "text": "Welcome to the Consilium roundtable discussion!"},
                {"speaker": "Search", "text": "I've gathered relevant data for our analysis."}
            ],
            "currentSpeaker": None,
            "thinking": ["GPT-4", "Mistral"],
            "showBubbles": ["Claude"],
            "avatarImages": {
                "Claude": "https://example.com/claude-avatar.jpg",
                "Gemini": "https://example.com/gemini-avatar.png"
            }
        })