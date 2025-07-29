"""
File analysis example using Fumes
"""

import os
from pathlib import Path
from fumes import App, FileUpload, Button, Markdown, Chart

app = App(title="File Analyzer")

# Create UI components
file_upload = FileUpload(
    label="Upload File",
    accept=".txt,.csv,.json"
)
analyze_btn = Button("Analyze", variant="primary")

@app.bind(analyze_btn)
def on_analyze():
    if not file_upload.value:
        return "Please upload a file first."
        
    file_path = Path(file_upload.value)
    if not file_path.exists():
        return "File not found."
        
    # Get file stats
    stats = file_path.stat()
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Basic analysis
        lines = content.splitlines()
        words = content.split()
        chars = len(content)
        
        # Create analysis report
        report = f"""## File Analysis Report

### Basic Stats
- File Name: {file_path.name}
- File Size: {stats.st_size:,} bytes
- Created: {stats.st_ctime}
- Modified: {stats.st_mtime}

### Content Analysis
- Lines: {len(lines):,}
- Words: {len(words):,}
- Characters: {chars:,}

### Sample Content
```
{content[:500]}...
```
"""
        return Markdown(report)
        
    except Exception as e:
        return f"Error analyzing file: {str(e)}"

if __name__ == "__main__":
    app.mount() 