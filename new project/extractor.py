import re

BANK_REGEX = r"\b\d{9,18}\b"
UPI_REGEX = r"\b[\w.-]+@[\w]+\b"
URL_REGEX = r"https?://[^\s]+"

def extract_intelligence(messages):
    bank_accounts = set()
    upi_ids = set()
    urls = set()

    for msg in messages:
        text = msg.content
        bank_accounts.update(re.findall(BANK_REGEX, text))
        upi_ids.update(re.findall(UPI_REGEX, text))
        urls.update(re.findall(URL_REGEX, text))

    return {
        "bank_accounts": list(bank_accounts),
        "upi_ids": list(upi_ids),
        "phishing_urls": list(urls)
    }
