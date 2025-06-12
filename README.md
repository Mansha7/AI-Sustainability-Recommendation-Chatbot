# AI-Sustainability-Recommendation-Chatbot

🧠 Overview

The AI-Powered-Sustainability-Recommendation-Chatbot is an intelligent chatbot designed to analyze the architectural deployment details of software applications and generate prioritized recommendations to optimize for sustainability, performance, and cost —with a primary focus on environmental impact.

Users can select which metric to prioritize, and the bot uses LLM-based reasoning to provide context-aware suggestions. It supports asynchronous multi-objective prompting.

🚀 Features

🔍 LLM-based analysis: Uses Huggingface models via Ollama for contextual understanding of deployment data.
⚡ Async optimization: Parallel execution of prompts for sustainability, performance, and cost suggestions.
🧩 Prioritization control: Users can assign a primary focus (e.g., sustainability-first) for tailored advice.

🧰 Tech Stack

Python
FastAPI – API orchestration and integration
Ollama – Lightweight local model runner
Huggingface Transformers – LLMs for prompt handling
Asyncio – For concurrent multi-goal prompt execution

🛠 How It Works
User Input: Deployment architecture text

LLM Processing: Three async prompts sent to Huggingface model via Ollama for:

Sustainability optimization

Performance tuning

Cost reduction

Ranking: Outputs ranked based on user-defined priority

(Future): Ingested knowledge can be used to enhance LLM understanding via RAG

(Future): Extendable to implement actions using DevOps APIs or cloud control SDKs
