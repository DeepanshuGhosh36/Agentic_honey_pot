import re

BANK_REGEX = r"\b\d{9,18}\b"
UPI_REGEX = r"\b[\w.-]+@[\w]+\b"
URL_REGEX = r"https?://[^\s]+"
PHONE_REGEX = r"\b\+?\d{10,13}\b"

SUSPICIOUS_KEYWORDS = ["urgent", "verify", "blocked", "suspended", "account", "upi", "click"]

def extract_intelligence(conversation):
    banks, upis, urls, phones, keywords = set(), set(), set(), set(), set()

    for msg in conversation:
        text = msg.get("text", "")
        banks.update(re.findall(BANK_REGEX, text))
        upis.update(re.findall(UPI_REGEX, text))
        urls.update(re.findall(URL_REGEX, text))
        phones.update(re.findall(PHONE_REGEX, text))

        for kw in SUSPICIOUS_KEYWORDS:
            if kw in text.lower():
                keywords.add(kw)

    return {
        "bankAccounts": list(banks),
        "upiIds": list(upis),
        "phishingLinks": list(urls),
        "phoneNumbers": list(phones),
        "suspiciousKeywords": list(keywords)
    }
