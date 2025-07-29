"""
Tests for Fumes components
"""

import pytest
from fumes.components import Textbox, Button, Markdown, FileUpload

def test_textbox_creation():
    textbox = Textbox(label="Test", value="Hello")
    assert textbox.label == "Test"
    assert textbox.value == "Hello"
    assert textbox.id is not None

def test_button_creation():
    button = Button("Click me", variant="primary")
    assert button.label == "Click me"
    assert button.variant == "primary"
    assert button.id is not None

def test_markdown_creation():
    markdown = Markdown(value="# Hello")
    assert markdown.value == "# Hello"
    assert markdown.id is not None

def test_file_upload_creation():
    file_upload = FileUpload(label="Upload", accept=".txt")
    assert file_upload.label == "Upload"
    assert file_upload.accept == ".txt"
    assert file_upload.id is not None

def test_component_to_dict():
    textbox = Textbox(label="Test", value="Hello")
    data = textbox.to_dict()
    assert data["type"] == "Textbox"
    assert data["label"] == "Test"
    assert data["value"] == "Hello"
    assert "id" in data 