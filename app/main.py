from fastapi import FastAPI
from pydantic import BaseModel
from app.modules.persona_detector import detect_persona
from app.modules.kb_retriever import retrieve_knowledge
from app.modules.response_generator import generate_response
from app.modules.escalation_engine import check_escalation

app = FastAPI()

class SupportRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(request: SupportRequest):
    # Step 1: Detect Persona
    detected_persona = detect_persona(request.message)
    
    # Step 2: Retrieve Knowledge Base info
    kb_info = retrieve_knowledge(request.message)
    
    # Step 3: Adapt Tone
    final_response = generate_response(detected_persona, kb_info)
    
    # Step 4: Check if Escalation is needed
    escalation_decision = check_escalation(
        persona=detected_persona, 
        message=request.message, 
        kb_found=kb_info.get("found", False)
    )
    
    # Override the bot response if we are escalating
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