"""
Button component for user interactions
"""

from typing import Optional, Any
from fumes.components.base import Component

class Button(Component):
    def __init__(
        self,
        label: str,
        variant: str = "primary",
        size: str = "medium",
        disabled: bool = False,
        **kwargs
    ):
        super().__init__(label=label, value=None, **kwargs)
        self.variant = variant
        self.size = size
        self.disabled = disabled
        
    def to_dict(self) -> dict:
        """Convert component to dictionary for frontend rendering"""
        data = super().to_dict()
        data.update({
            "variant": self.variant,
            "size": self.size,
            "disabled": self.disabled
        })
        return data 