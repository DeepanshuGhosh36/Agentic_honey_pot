from fastapi import FastAPI, Depends, Request
import requests

from auth import verify_api_key
from detector import detect_scam_from_guvi_format
from agent import generate_agent_reply
from extractor import extract_intelligence
from memory import build_conversation

app = FastAPI(title="Agentic HoneyPot API")

FINAL_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

@app.post("/scam-detection")
async def scam_endpoint(request: Request, api_key: str = Depends(verify_api_key)):
    try:
        body = await request.json()
    except:
        return {"status": "error", "reply": ""}

    session_id = body.get("sessionId", "unknown")
    message = body.get("message", {})
    history = body.get("conversationHistory", [])

    conversation = build_conversation(history, message)

    scam_detected = detect_scam_from_guvi_format(conversation)

    if scam_detected:
        reply = generate_agent_reply(message.get("text", ""))
    else:
        reply = "Could you please explain more?"

    # Extract intelligence across turns
    intelligence = extract_intelligence(conversation)

    # If scam detected AND sufficient engagement (>=3 turns), send final callback
    if scam_detected and len(conversation) >= 3:
        payload = {
            "sessionId": session_id,
            "scamDetected": True,
            "totalMessagesExchanged": len(conversation),
            "extractedIntelligence": intelligence,
            "agentNotes": "Urgency tactics and payment redirection observed"
        }

        try:
            requests.post(FINAL_CALLBACK_URL, json=payload, timeout=5)
        except:
            pass 

   
    return {
        "status": "success",
        "reply": reply
    }




