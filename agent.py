import random

AGENT_PERSONA = [
    "I'm not very tech savvy, can you explain?",
    "I already tried once, it didn't work.",
    "My bank app is slow today.",
    "Is there another way to do this?"
]

def generate_agent_reply(last_message):
    probing_prompts = [
        "Can you send the exact link again?",
        "Which bank account should I use?",
        "Is this UPI or direct transfer?",
        "Can you share the full details?"
    ]

    return f"{random.choice(AGENT_PERSONA)} {random.choice(probing_prompts)}"
