from ollama import AsyncClient

async def call_ollama(prompt):
    client = AsyncClient() 
    try:
        print(f"Sending request for: '{prompt[:30]}...'")
        response = await client.generate(
            model='granite3.3:8b',
            prompt=prompt,
            options={
                'temperature': 0.0,       
                'top_p': 1.0,
                'top_k': 1,
                'repetition_penalty': 1.0
            }
        )
        content = response['response'].strip()
        print(f"Received response for: '{prompt[:30]}...' - {content[:50]}...")
        return content
    except Exception as e:
        # Raise instead of returning a string
        raise RuntimeError(f"Ollama request failed: {e}")