# Persona-Adaptive AI Support Agent 🤖

A context-aware, AI-driven customer support agent that dynamically detects user intent, retrieves relevant knowledge base articles, and adapts its response tone based on the user's emotional state and technical expertise.

**Live Demo:** [Insert your Render URL here]

## 🏗️ Architecture & Tech Stack

* **Backend Framework:** FastAPI (Python)
* **AI / NLP Engine:** Groq API running `Llama-3.1-8b-instant` for zero-shot intent classification.
* **Knowledge Base:** JSON-based deterministic retrieval system.
* **Frontend:** Vanilla HTML/JS/CSS served directly via FastAPI.
* **Deployment:** Render (Containerized Web Service).

## 🧠 Core Modules

1. **Persona Detector (`persona_detector.py`)**
   Instead of relying on brittle regex or keyword mapping, this module uses a Large Language Model (Llama-3) to perform semantic intent classification. It accurately categorizes the user into one of four personas: `technical_expert`, `frustrated_user`, `business_executive`, or `general_user`, even if they use slang or make typos.

2. **Knowledge Base Retriever (`kb_retriever.py`)**
   A deterministic search engine that scans a local `articles.json` database for matching heuristic keywords to retrieve the correct support solution.

3. **Response Generator (`response_generator.py`)**
   A templating engine that dynamically wraps the retrieved KB article in the appropriate tone (e.g., highly empathetic for frustrated users, purely analytical for technical experts).

4. **Escalation Engine (`escalation_engine.py`)**
   A strict, rule-based safety net. It automatically bypasses the AI and flags the conversation for human routing if:
   * The user explicitly asks for a human/manager.
   * Critical keywords (security, breach, legal) are detected.
   * The user is detected as `frustrated_user` but the KB Retriever fails to find a solution (preventing the bot from frustrating the user further with generic fallback responses).

## 🚀 Engineering Trade-offs & Future Scope
Given the 24-hour assignment constraint, I prioritized integrating an LLM for dynamic intent classification to handle edge cases in user input. For the Knowledge Base Retrieval, I implemented a deterministic keyword-matching heuristic to ensure reliable MVP delivery and prevent AI hallucinations. 

In a production environment, my immediate next step would be upgrading the KB module to use Semantic Vector Search (e.g., ChromaDB with HuggingFace embeddings) for true Retrieval-Augmented Generation (RAG) capabilities.

## 💻 Local Setup
1. Clone the repository.
2. Create a `.env` file in the root directory and add your API key: `GROQ_API_KEY=your_key_here`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `python -m uvicorn app.main:app --reload`
5. Visit `http://127.0.0.1:8000` in your browser.