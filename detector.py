SCAM_KEYWORDS = [
    "blocked", "verify", "urgent", "account", "upi", "bank", "click",
    "suspended", "immediately", "limited time", "refund", "lottery", "won"
]

def detect_scam_from_guvi_format(conversation):
    score = 0
    for msg in conversation:
        text = msg.get("text", "").lower()
        for kw in SCAM_KEYWORDS:
            if kw in text:
                score += 1
    return score >= 2
