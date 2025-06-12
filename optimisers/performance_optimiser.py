import asyncio
from utils.ollama_client import call_ollama 

async def recommend_performance_changes(deployment_context):
    prompt = f"""
                You are a cloud performance optimization specialist with deep expertise in IBM Cloud architecture and service tuning. Given a specific deployment scenario, your task is to offer up to 4 highly impactful recommendations to improve performance (e.g., lower latency, faster scaling, optimized throughput).
                For each recommendation:
                 - Clearly explain *how* it enhances performance and under what conditions it is most effective.
                - Provide a rough estimate of the potential gain, referencing common benchmarks or well-known engineering heuristics.
                 - Include IBM Cloud-specific service-level configurations, feature toggles, or architectural adjustments.
                - Flag one recommendation as the "best option" in terms of performance improvement relative to implementation effort.
    
                Deployment context:{deployment_context}
    
            Response Format:
            Recommendation 1: [Title]
            Justification: [Why this helps]
            Estimated Impact: [Quantified or rough estimate]
            IBM Cloud-Specific Steps: [What to do]
            (Repeat for up to 4)
        """

    response = await call_ollama(prompt)
    print(f"Performance Improvements {response}")
    return response

if __name__ == "__main__":
    #deployment_context = "We have deployed an AI chatbot that uses a VM for processing, a Postgres database for storing conversations, and a Redis cache to manage session data."
    deployment_context = [{'deployment_context': 'A system for analyzing customer feedback by classifying it into sentiment (positive, negative, neutral) and urgency (high, medium, low) categories.', 'recommended_services': [{'name': 'IBM Watson Natural Language Understanding', 'count': '1', 'usage': 'This service will be used to analyze the text of customer feedback and extract sentiment and urgency.'}, {'name': 'IBM Cloud Object Storage', 'count': '1', 'usage': 'This service will store the customer feedback data securely and provide easy access for the analysis process.'}, {'name': 'IBM Cloud Functions', 'count': '1', 'usage': 'This serverless compute platform can be used to trigger the sentiment and urgency analysis whenever new feedback is received or stored.'}]}]
    #deployment_context = "I want to build a feedback analyzer that takes customer feedback and classifies it by sentiment and urgency."
    #deployment_context = "Hello World"
    results = asyncio.run(recommend_performance_changes(deployment_context))
    #print(response)
    #parsed_response = parse_deployment_output(response)
    print(results)
    #print(type(parsed_response))