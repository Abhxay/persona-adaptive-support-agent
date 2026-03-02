def generate_response(persona: str, kb_info: dict) -> str:
    # If we didn't find anything in the database
    if not kb_info.get("found"):
        if persona == "frustrated_user":
            return "I am so sorry, I can't find the exact solution right now, but I am escalating this immediately!"
        return "I don't have a specific article for that. Could you provide a few more details?"

    base_content = kb_info.get("content", "")

    # Apply the correct tone wrapper based on the persona
    if persona == "technical_expert":
        return f"STATUS: Acknowledged.\nDIAGNOSIS: {base_content}\nRECOMMENDATION: Please verify your payload size and implement exponential backoff in your retry logic."

    elif persona == "frustrated_user":
        return f"I am so sorry you're dealing with this! I completely understand how stressful this is. Let's get this fixed for you right now:\n\n{base_content}\n\nDid this resolve the issue for you?"

    elif persona == "business_executive":
        return f"Executive Update: We have identified the root cause of the disruption.\n\nACTION PLAN: {base_content}\n\nBusiness impact is being minimized, and we are monitoring the situation closely."

    else:
        # General user fallback
        return f"Here is some information that might help:\n{base_content}"