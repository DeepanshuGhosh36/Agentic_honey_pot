SCAM_KEYWORDS = [
    "urgent", "blocked", "kyc", "verify",
    "bank", "upi", "click", "link",
    "lottery", "prize", "refund", "account"
]

def detect_scam(messages):
    score = 0
    for msg in messages:
        text = msg.content.lower()
        for keyword in SCAM_KEYWORDS:
            if keyword in text:
                score += 1
    return score >= 2
