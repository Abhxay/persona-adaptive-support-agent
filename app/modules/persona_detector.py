def detect_persona(message: str) -> str:
    message = message.lower()
    
    # 1. Check for Frustrated User
    frustrated_keywords = ["!", "why", "not working", "broken", "terrible", "urgent", "fix this"]
    if any(word in message for word in frustrated_keywords):
        return "frustrated_user"
        
    # 2. Check for Business Executive
    business_keywords = ["budget", "roi", "timeline", "cost", "deadline", "impact", "manager"]
    if any(word in message for word in business_keywords):
        return "business_executive"
        
    # 3. Check for Technical Expert
    technical_keywords = ["api", "json", "timeout", "server", "code", "database", "endpoint", "logs"]
    if any(word in message for word in technical_keywords):
        return "technical_expert"
        
    # Default fallback
    return "general_user"