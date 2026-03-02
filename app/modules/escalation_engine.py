def check_escalation(persona: str, message: str, kb_found: bool) -> dict:
    message = message.lower()
    
    # 1. Explicit requests for a human
    escalation_keywords = ["human", "agent", "manager", "real person", "operator", "lawsuit"]
    if any(word in message for word in escalation_keywords):
        return {"escalate": True, "reason": "User explicitly requested a human or used extreme keywords."}
        
    # 2. Critical issues that a bot shouldn't handle alone
    critical_issues = ["security", "breach", "hack", "legal", "compliance"]
    if any(word in message for word in critical_issues):
        return {"escalate": True, "reason": "Critical issue category detected (security/legal)."}
        
    # 3. Frustrated user with no solution
    if persona == "frustrated_user" and not kb_found:
        return {"escalate": True, "reason": "User is frustrated and the bot has no valid KB article to help."}
        
    # Default: No escalation needed
    return {"escalate": False, "reason": "Bot handled the query successfully."}