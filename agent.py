import random

PERSONA = [
    "I'm a bit confused about this.",
    "I don’t understand why this is happening.",
    "This is the first time I’m seeing this issue.",
    "Can you explain it again?"
]

PROBES = [
    "Why is my account being suspended?",
    "Can you share the exact steps?",
    "Which bank account should I use?",
    "Can you send the link again?"
]

def generate_agent_reply(last_text: str):
    return f"{random.choice(PERSONA)} {random.choice(PROBES)}"
