"""
Simple chatbot example using Fumes
"""

from fumes import App, Textbox, Button, Markdown

app = App(title="Fumes Chatbot")

# Create UI components
input_box = Textbox(
    label="Message",
    placeholder="Type your message here...",
    multiline=True,
    rows=3
)
send_btn = Button("Send", variant="primary")
clear_btn = Button("Clear", variant="secondary")

# Store chat history
chat_history = []

@app.bind(send_btn)
def on_send():
    if not input_box.value:
        return
        
    # Add user message to history
    chat_history.append(f"You: {input_box.value}")
    
    # Simulate bot response
    response = f"Bot: I received your message: '{input_box.value}'"
    chat_history.append(response)
    
    # Clear input
    input_box.value = ""
    
    # Return formatted chat history
    return Markdown("\n\n".join(chat_history))

@app.bind(clear_btn)
def on_clear():
    chat_history.clear()
    input_box.value = ""
    return Markdown("Chat cleared!")

if __name__ == "__main__":
    app.mount() 