"""
Textbox component for text input
"""

from typing import Optional, Any
from fumes.components.base import Component

class Textbox(Component):
    def __init__(
        self,
        label: Optional[str] = None,
        value: str = "",
        placeholder: Optional[str] = None,
        multiline: bool = False,
        rows: int = 1,
        **kwargs
    ):
        super().__init__(label=label, value=value, **kwargs)
        self.placeholder = placeholder
        self.multiline = multiline
        self.rows = rows
        
    def to_dict(self) -> dict:
        """Convert component to dictionary for frontend rendering"""
        data = super().to_dict()
        data.update({
            "placeholder": self.placeholder,
            "multiline": self.multiline,
            "rows": self.rows
        })
        return data 