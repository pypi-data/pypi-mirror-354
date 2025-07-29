class FumesApp {
    constructor(config) {
        this.config = config;
        this.components = new Map();
        this.ws = null;
        this.connectWebSocket();
    }

    connectWebSocket() {
        this.ws = new WebSocket(this.config.wsUrl);
        
        this.ws.onopen = () => {
            console.log('Connected to Fumes server');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onclose = () => {
            console.log('Disconnected from Fumes server');
            // Attempt to reconnect after 1 second
            setTimeout(() => this.connectWebSocket(), 1000);
        };
    }

    handleMessage(data) {
        const { component_id, value } = data;
        const component = this.components.get(component_id);
        
        if (component) {
            if (component.update) {
                component.update(value);
            }
        }
    }

    registerComponent(id, component) {
        this.components.set(id, component);
    }

    sendMessage(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }
}

// Component Classes
class Component {
    constructor(id, type, props = {}) {
        this.id = id;
        this.type = type;
        this.props = props;
        this.element = null;
    }

    render() {
        throw new Error('Component must implement render()');
    }

    update(value) {
        throw new Error('Component must implement update()');
    }
}

class Textbox extends Component {
    render() {
        const container = document.createElement('div');
        container.className = 'fumes-component';
        
        if (this.props.label) {
            const label = document.createElement('label');
            label.className = 'fumes-textbox-label';
            label.textContent = this.props.label;
            container.appendChild(label);
        }
        
        const input = document.createElement(this.props.multiline ? 'textarea' : 'input');
        input.className = 'fumes-textbox';
        input.value = this.props.value || '';
        input.placeholder = this.props.placeholder || '';
        
        if (this.props.multiline) {
            input.rows = this.props.rows || 3;
        }
        
        input.addEventListener('input', (e) => {
            app.sendMessage({
                component_id: this.id,
                event_type: 'change',
                value: e.target.value
            });
        });
        
        container.appendChild(input);
        this.element = container;
        return container;
    }

    update(value) {
        if (this.element) {
            const input = this.element.querySelector('input, textarea');
            if (input) {
                input.value = value;
            }
        }
    }
}

class Button extends Component {
    render() {
        const button = document.createElement('button');
        button.className = `fumes-button fumes-button-${this.props.variant || 'primary'}`;
        button.textContent = this.props.label;
        button.disabled = this.props.disabled || false;
        
        button.addEventListener('click', () => {
            app.sendMessage({
                component_id: this.id,
                event_type: 'click'
            });
        });
        
        this.element = button;
        return button;
    }

    update(props) {
        if (this.element) {
            if (props.disabled !== undefined) {
                this.element.disabled = props.disabled;
            }
        }
    }
}

class Markdown extends Component {
    render() {
        const container = document.createElement('div');
        container.className = 'fumes-markdown';
        container.innerHTML = this.props.value || '';
        this.element = container;
        return container;
    }

    update(value) {
        if (this.element) {
            this.element.innerHTML = value;
        }
    }
}

class FileUpload extends Component {
    render() {
        const container = document.createElement('div');
        container.className = 'fumes-file-upload';
        
        if (this.props.label) {
            const label = document.createElement('label');
            label.className = 'fumes-file-upload-label';
            label.textContent = this.props.label;
            container.appendChild(label);
        }
        
        const input = document.createElement('input');
        input.type = 'file';
        input.className = 'fumes-file-upload-input';
        input.accept = this.props.accept || '*/*';
        
        const button = document.createElement('button');
        button.className = 'fumes-file-upload-button';
        button.textContent = 'Choose File';
        
        button.addEventListener('click', () => {
            input.click();
        });
        
        input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                app.sendMessage({
                    component_id: this.id,
                    event_type: 'change',
                    value: file.name
                });
            }
        });
        
        container.appendChild(input);
        container.appendChild(button);
        this.element = container;
        return container;
    }

    update(value) {
        if (this.element) {
            const button = this.element.querySelector('button');
            if (button) {
                button.textContent = value || 'Choose File';
            }
        }
    }
}

// Initialize global app instance
let app;

// Export components
window.FumesApp = FumesApp;
window.FumesComponents = {
    Textbox,
    Button,
    Markdown,
    FileUpload
}; 