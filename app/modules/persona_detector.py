import os
from groq import Groq
from dotenv import load_dotenv

# Force Python to find the .env file in the root directory (for local testing)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

def detect_persona(message: str) -> str:
    # LAZY INITIALIZATION: Check for the key only when the function is called
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("WARNING: GROQ_API_KEY is missing. Falling back to general_user.")
        return "general_user"
        
    try:
        # Initialize client here safely
        client = Groq(api_key=api_key)
        
        system_prompt = """
        You are an AI intent classifier for a customer support system. 
        Analyze the user's message and categorize their persona into EXACTLY ONE of these four categories:
        1. "technical_expert" (mentions code, APIs, servers, logs, bugs, architecture)
        2. "frustrated_user" (angry, urgent, using exclamation marks, complaining about broken things, emotional)
        3. "business_executive" (mentions budget, ROI, timelines, managers, costs, impact, enterprise)
        4. "general_user" (polite, simple questions, none of the above)
        
        Respond with ONLY the exact category name. Do not add any other text, punctuation, or explanation.
        """
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.1, 
            max_tokens=10,
        )
        
        detected = chat_completion.choices[0].message.content.strip().lower()
        
        valid_personas = ["technical_expert", "frustrated_user", "business_executive", "general_user"]
        if detected in valid_personas:
            return detected
        else:
            return "general_user"
            
    except Exception as e:
        print(f"AI Detection failed: {e}")
        return "general_user"