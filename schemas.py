from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: str
    content: str

class ScamRequest(BaseModel):
    conversation_id: Optional[str] = "unknown"
    messages: List[Message] = []

    class Config:
        extra = "allow"  # <-- ACCEPT EXTRA FIELDS

class Intelligence(BaseModel):
    bank_accounts: List[str] = []
    upi_ids: List[str] = []
    phishing_urls: List[str] = []

class ScamResponse(BaseModel):
    scam_detected: bool
    agent_activated: bool
    agent_reply: Optional[str]
    engagement_metrics: Dict[str, int]
    extracted_intelligence: Intelligence

