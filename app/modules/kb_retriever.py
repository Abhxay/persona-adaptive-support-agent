import json
import os

# Get the absolute path to the JSON file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KB_PATH = os.path.join(BASE_DIR, "knowledge_base", "articles.json")

def retrieve_knowledge(message: str) -> dict:
    message = message.lower()
    
    try:
        with open(KB_PATH, "r") as file:
            articles = json.load(file)
            
            # Simple search: check if any article keywords are in the user's message
            for article in articles:
                for keyword in article["keywords"]:
                    if keyword in message:
                        return {"found": True, "title": article["title"], "content": article["content"]}
                        
    except FileNotFoundError:
        return {"found": False, "error": "Knowledge base file not found."}
        
    return {"found": False, "content": "No relevant articles found for your query."}