from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.modules.persona_detector import detect_persona
from app.modules.kb_retriever import retrieve_knowledge
from app.modules.response_generator import generate_response
from app.modules.escalation_engine import check_escalation

app = FastAPI()

class SupportRequest(BaseModel):
    message: str

# --- THE NEW FRONTEND UI ---
@app.get("/", response_class=HTMLResponse)
def serve_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Support Agent</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .chat-container { width: 100%; max-width: 500px; background: white; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); display: flex; flex-direction: column; height: 80vh; overflow: hidden; }
            .chat-header { background: #000000; color: white; padding: 20px; text-align: center; font-size: 1.2rem; font-weight: bold; }
            .chat-box { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; background: #ffffff; }
            .message { max-width: 80%; padding: 12px 16px; border-radius: 12px; line-height: 1.4; font-size: 0.95rem; }
            .user-msg { align-self: flex-end; background: #007bff; color: white; border-bottom-right-radius: 2px; }
            .bot-msg { align-self: flex-start; background: #f1f3f4; color: #202124; border-bottom-left-radius: 2px; }
            .meta-data { display: block; font-size: 0.75rem; margin-top: 8px; color: #5f6368; font-style: italic; border-top: 1px solid #e0e0e0; padding-top: 5px;}
            .escalated { color: #d93025; font-weight: bold; }
            .input-area { display: flex; padding: 15px; background: white; border-top: 1px solid #e0e0e0; }
            input { flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 20px; outline: none; font-size: 1rem; }
            button { background: #000000; color: white; border: none; padding: 10px 20px; margin-left: 10px; border-radius: 20px; cursor: pointer; font-weight: bold; transition: 0.2s; }
            button:hover { background: #333333; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">Persona-Adaptive AI Agent</div>
            <div class="chat-box" id="chat-box">
                <div class="message bot-msg">Hello! I am your AI support assistant. How can I help you today?</div>
            </div>
            <form class="input-area" id="chat-form">
                <input type="text" id="user-input" placeholder="Type your message..." required autocomplete="off">
                <button type="submit">Send</button>
            </form>
        </div>

        <script>
            const form = document.getElementById('chat-form');
            const input = document.getElementById('user-input');
            const chatBox = document.getElementById('chat-box');

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const message = input.value.trim();
                if (!message) return;

                // Add User Message to UI
                addMessage(message, 'user-msg');
                input.value = '';

                // Add loading indicator
                const loadingId = addMessage('...', 'bot-msg');

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message })
                    });
                    const data = await response.json();
                    
                    // Remove loading indicator
                    document.getElementById(loadingId).remove();

                    // Format bot response with insights
                    let finalHtml = data.bot_response;
                    finalHtml += `<span class="meta-data">🧠 Persona Detected: ${data.persona}</span>`;
                    
                    if (data.escalation_status && data.escalation_status.escalate) {
                        finalHtml += `<span class="meta-data escalated">⚠️ Escalated: ${data.escalation_status.reason}</span>`;
                    }

                    addMessage(finalHtml, 'bot-msg', true);
                } catch (error) {
                    document.getElementById(loadingId).remove();
                    addMessage('Error connecting to the server.', 'bot-msg');
                }
            });

            // FIXED JAVASCRIPT BUG: Added random number generator to ensure unique IDs
            function addMessage(text, className, isHtml = false) {
                const div = document.createElement('div');
                div.className = `message ${className}`;
                div.id = 'msg-' + Date.now() + '-' + Math.floor(Math.random() * 10000);
                if (isHtml) { div.innerHTML = text; } 
                else { div.textContent = text; }
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
                return div.id;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# --- THE EXISTING API ENDPOINTS ---
@app.post("/chat")
def chat_endpoint(request: SupportRequest):
    detected_persona = detect_persona(request.message)
    kb_info = retrieve_knowledge(request.message)
    final_response = generate_response(detected_persona, kb_info)
    escalation_decision = check_escalation(detected_persona, request.message, kb_info.get("found", False))
    
    if escalation_decision["escalate"]:
        final_response = f"TRANSFERRING TO HUMAN AGENT: {escalation_decision['reason']}"
    
    return {
        "original_message": request.message,
        "persona": detected_persona,
        "bot_response": final_response,
        "escalation_status": escalation_decision,
        "status": "Assignment MVP Complete!"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}