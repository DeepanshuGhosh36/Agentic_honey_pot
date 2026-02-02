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

    # Try all possible places where messages might exist
    messages = (
        body.get("messages")
        or body.get("data", {}).get("messages")
        or body.get("event", {}).get("messages")
        or []
    )

    # Normalize messages
    normalized_messages = []
    for msg in messages:
        if isinstance(msg, dict) and "content" in msg:
            normalized_messages.append(
                type("Msg", (), {
                    "role": msg.get("role", "scammer"),
                    "content": msg.get("content", "")
                })()
            )

    scam_detected = detect_scam(normalized_messages)

    agent_reply = None
    agent_activated = False

    if scam_detected:
        agent_activated = True
        last_message = normalized_messages[-1].content if normalized_messages else ""
        agent_reply = generate_agent_reply(last_message)

    intelligence = extract_intelligence(normalized_messages)

    return {
        "scam_detected": scam_detected,
        "agent_activated": agent_activated,
        "agent_reply": agent_reply,
        "engagement_metrics": {
            "conversation_turns": len(normalized_messages),
            "scammer_messages": len(
                [m for m in normalized_messages if m.role == "scammer"]
            )
        },
        "extracted_intelligence": intelligence
    }
