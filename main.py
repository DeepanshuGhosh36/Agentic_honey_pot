from fastapi import FastAPI, Depends, Request
import threading
import requests

from auth import verify_api_key
from detector import detect_scam_from_guvi_format
from agent import generate_agent_reply
from extractor import extract_intelligence
from memory import build_conversation

app = FastAPI(title="Agentic HoneyPot API")

FINAL_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

@app.get("/")
def health():
    return {"status": "ok"}

def send_final_callback_async(payload):
    try:
        requests.post(FINAL_CALLBACK_URL, json=payload, timeout=3)
    except:
        pass

@app.post("/scam-detection")
async def scam_endpoint(request: Request, api_key: str = Depends(verify_api_key)):
    try:
        body = await request.json()
    except:
        return {"status": "error", "reply": ""}

    session_id = body.get("sessionId", "unknown")
    message = body.get("message", {}) or {}
    history = body.get("conversationHistory", []) or []

    conversation = build_conversation(history, message)

    scam_detected = detect_scam_from_guvi_format(conversation)

    if scam_detected:
        reply = generate_agent_reply(message.get("text", ""))
    else:
        reply = "Could you please explain more?"

    intelligence = extract_intelligence(conversation)

    # Non-blocking final callback after enough turns
    if scam_detected and len(conversation) >= 3:
        payload = {
            "sessionId": session_id,
            "scamDetected": True,
            "totalMessagesExchanged": len(conversation),
            "extractedIntelligence": intelligence,
            "agentNotes": "Urgency tactics and payment redirection observed"
        }
        threading.Thread(target=send_final_callback_async, args=(payload,), daemon=True).start()

    # ✅ STRICT GUVI VALIDATOR RESPONSE
    return {
        "status": "success",
        "reply": reply
    }
