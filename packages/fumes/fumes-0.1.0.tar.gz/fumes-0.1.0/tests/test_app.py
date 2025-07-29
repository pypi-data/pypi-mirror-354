"""
Tests for Fumes App class
"""

import pytest
from fumes import App
from fumes.components import Textbox, Button

def test_app_creation():
    app = App(title="Test App")
    assert app.title == "Test App"
    assert app.fastapi_app is not None
    assert app.state is not None
    assert app.ws_manager is not None

def test_app_bind():
    app = App(title="Test App")
    textbox = Textbox(label="Test")
    button = Button("Click")
    
    @app.bind(button)
    def on_click():
        return f"Clicked: {textbox.value}"
    
    assert button.id in app.callbacks
    assert len(app.callbacks[button.id]) == 1

def test_app_state():
    app = App(title="Test App")
    app.state.set("test_key", "test_value")
    assert app.state.get("test_key") == "test_value"
    
    app.state.update({"key1": "value1", "key2": "value2"})
    assert app.state.get("key1") == "value1"
    assert app.state.get("key2") == "value2"
    
    app.state.delete("key1")
    assert app.state.get("key1") is None
    
    app.state.clear()
    assert app.state.get("test_key") is None
    assert app.state.get("key2") is None 