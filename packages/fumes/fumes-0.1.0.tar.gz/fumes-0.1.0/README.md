# Fumes

A Python library for building web-based AI/data apps with custom frontends. Fumes provides an intuitive Python API for creating interactive web applications, similar to Streamlit or Gradio, but with a unique design and modern features.

## Features

- 🎨 Intuitive Python API for defining UIs using decorators
- 🔄 Real-time updates via WebSocket
- 🎯 Modern, responsive UI with dark mode
- 🚀 Hot-reload for development
- 📦 Easy deployment with CLI tools
- 🎮 Rich set of UI components
- 🔌 FastAPI backend for high performance

## Installation

```bash
pip install fumes
```

## Quick Start

1. Create a new Fumes app:

```bash
fumes create my_app
cd my_app
```

2. Edit `app.py` to build your UI:

```python
from fumes import App, Textbox, Button

app = App(title="My AI Tool")

input = Textbox(label="Enter text")
btn = Button("Generate")

@app.bind(btn)
def on_click():
    return f"You typed: {input.value}"

if __name__ == "__main__":
    app.mount()
```

3. Run your app:

```bash
fumes run app.py
```

## Available Components

- `Textbox`: Text input field
- `Button`: Interactive button
- `Markdown`: Rich text display
- `Image`: Image display
- `FileUpload`: File upload component
- `Chart`: Data visualization

## CLI Commands

- `fumes create <app_name>`: Create a new Fumes app
- `fumes run <app.py>`: Run a Fumes app in development mode
- `fumes serve <app.py>`: Serve a Fumes app in production mode

## Development

```bash
# Clone the repository
git clone https://github.com/t4zn/fumes.git
cd fumes

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT License - see LICENSE file for details 