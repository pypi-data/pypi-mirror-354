"""
Base component class for Fumes UI components
"""

import uuid
from typing import Any, Dict, Optional

class Component:
    def __init__(
        self,
        id: Optional[str] = None,
        label: Optional[str] = None,
        value: Any = None,
        **kwargs
    ):
        self.id = id or str(uuid.uuid4())
        self.label = label
        self._value = value
        self.props = kwargs
        
    @property
    def value(self) -> Any:
        """Get the component's value"""
        return self._value
        
    @value.setter
    def value(self, new_value: Any) -> None:
        """Set the component's value"""
        self._value = new_value
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary for frontend rendering"""
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "label": self.label,
            "value": self._value,
            "props": self.props
        }
        
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, label={self.label})"
        
    def __repr__(self) -> str:
        return self.__str__() 