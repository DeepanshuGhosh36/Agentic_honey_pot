from fastapi import FastAPI, Depends, Request
from auth import verify_api_key
from detector import detect_scam
from agent import generate_agent_reply
from extractor import extract_intelligence
app = FastAPI(title="Agentic HoneyPot API")
@app.post("/scam-detection")
async def scam_endpoint(request: Request, api_key: str = Depends(verify_api_key)):

    try:
        body = await request.json()
    except:
        body = {}

    messages = body.get("messages", [])

    normalized_messages = []
    for msg in messages:
        if isinstance(msg, dict):
            normalized_messages.append(
                type("Msg", (), {
                    "role": msg.get("role", "scammer"),
                    "content": msg.get("content", "")
                })()
            )

    scam_detected = detect_scam(normalized_messages)

    agent_reply = ""
    if scam_detected:
        agent_reply = generate_agent_reply(
            normalized_messages[-1].content if normalized_messages else ""
        )

    intelligence = extract_intelligence(normalized_messages)

    return {
        "scam_detected": bool(scam_detected),
        "agent_activated": bool(scam_detected),
        "agent_reply": agent_reply,
        "engagement_metrics": {
            "conversation_turns": len(normalized_messages),
            "scammer_messages": len(
                [m for m in normalized_messages if m.role == "scammer"]
            )
        },
        "extracted_intelligence": {
            "bank_accounts": intelligence.get("bank_accounts", []),
            "upi_ids": intelligence.get("upi_ids", []),
            "phishing_urls": intelligence.get("phishing_urls", [])
        }
    }



