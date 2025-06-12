import os
import asyncio
from ollama import AsyncClient as OllamaClient
from openai import AsyncOpenAI
import google.generativeai as genai

# Configure API keys
os.environ["GOOGLE_API_KEY"] = "<your_google_api_key>"
os.environ["OPENAI_API_KEY"] = "<your_openai_api_key>"

# Initialize Gemini API
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Unified function
async def call_model(prompt: str, backend: str = "ollama", model: str = None):
    print(f"Sending request to {backend.upper()} for: '{prompt[:30]}...'")

    try:
        if backend == "ollama":
            client = OllamaClient()
            response = await client.generate(
                model=model or "granite3.3:8b",
                prompt=prompt,
                options={
                    'temperature': 0.0,
                    'top_p': 1.0,
                    'top_k': 1,
                    'repetition_penalty': 1.0
                }
            )
            return response['response'].strip()

        elif backend == "openai":
            client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
            response = await client.chat.completions.create(
                model=model or "gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()

        elif backend == "google":
            model = genai.GenerativeModel(model or "gemini-pro")
            response = model.generate_content(prompt)
            return response.text.strip()

        else:
            raise ValueError(f"Unsupported backend: {backend}")

    except Exception as e:
        raise RuntimeError(f"{backend.upper()} request failed: {e}")

# from ollama import AsyncClient

# async def call_ollama(prompt):
#     client = AsyncClient() 
#     try:
#         print(f"Sending request for: '{prompt[:30]}...'")
#         response = await client.generate(
#             model='granite3.3:8b',
#             prompt=prompt,
#             options={
#                 'temperature': 0.0,       
#                 'top_p': 1.0,
#                 'top_k': 1,
#                 'repetition_penalty': 1.0
#             }
#         )
#         content = response['response'].strip()
#         print(f"Received response for: '{prompt[:30]}...' - {content[:50]}...")
#         return content
#     except Exception as e:
#         # Raise instead of returning a string
#         raise RuntimeError(f"Ollama request failed: {e}")