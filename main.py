from fastapi import FastAPI, Depends, Request
from auth import verify_api_key
from detector import detect_scam
from agent import generate_agent_reply
from extractor import extract_intelligence

app = FastAPI(title="Agentic HoneyPot API")
@app.post("/scam-detection")
async def scam_detection():
    return {
        "scam_detected": false,
        "agent_activated": false,
        "agent_reply": "",
        "engagement_metrics": {
            "conversation_turns": 0,
            "scammer_messages": 0
        },
        "extracted_intelligence": {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_urls": []
        }
    }


