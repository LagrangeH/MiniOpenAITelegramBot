def format_response(prompt: str, raw_response: str):
    if raw_response.lower().startswith(prompt.lower()):
        return f"<b>{prompt}</b> {raw_response[len(prompt):]}"

    elif raw_response[0].isupper():
        return f"<b>{prompt}</b>\n\n{raw_response}"

    else:
        return f"<b>{prompt}</b>"
