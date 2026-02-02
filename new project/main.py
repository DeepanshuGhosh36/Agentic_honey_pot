from fastapi import FastAPI, Depends
from schemas import ScamRequest, ScamResponse, Intelligence
from auth import verify_api_key
from detector import detect_scam
from agent import generate_agent_reply
from extractor import extract_intelligence
from memory import get_turn_count, get_last_scammer_message

app = FastAPI(title="Agentic HoneyPot API")

@app.post("/scam-detection", response_model=ScamResponse)
def scam_endpoint(request: ScamRequest, api_key: str = Depends(verify_api_key)):

    scam_detected = detect_scam(request.messages)
    agent_reply = None
    agent_activated = False

    if scam_detected:
        agent_activated = True
        last_msg = get_last_scammer_message(request.messages)
        agent_reply = generate_agent_reply(last_msg)

    intelligence = extract_intelligence(request.messages)

    return ScamResponse(
        scam_detected=scam_detected,
        agent_activated=agent_activated,
        agent_reply=agent_reply,
        engagement_metrics={
            "conversation_turns": get_turn_count(request.messages),
            "scammer_messages": len([m for m in request.messages if m.role == "scammer"])
        },
        extracted_intelligence=Intelligence(**intelligence)
    )
