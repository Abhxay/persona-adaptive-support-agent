from pydantic import BaseModel

class PersonaType(BaseModel):
    id: int
    name: str
    description: str

class PersonaDetectionResult(BaseModel):
    detected_persona: PersonaType
    confidence: float

class KBArticle(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
    updated_at: str

class ResponseGeneratorInput(BaseModel):
    user_message: str
    detected_persona: PersonaType

class EscalationContext(BaseModel):
    issue_description: str
    user: str
    detected_persona: PersonaType

class EscalationResult(BaseModel):
    success: bool
    detail: str | None = None

class SupportResponse(BaseModel):
    response_message: str
    articles: list[KBArticle]

class UserMessage(BaseModel):
    message: str
    timestamp: str
    user_id: str
