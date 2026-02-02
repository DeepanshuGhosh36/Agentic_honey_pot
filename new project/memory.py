def get_turn_count(messages):
    return len(messages)

def get_last_scammer_message(messages):
    for msg in reversed(messages):
        if msg.role == "scammer":
            return msg.content
    return ""
