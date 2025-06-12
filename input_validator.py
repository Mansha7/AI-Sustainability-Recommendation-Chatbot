import ollama
import re
import json

def analyze_deployment_context(deployment_context):
    prompt = f"""
    You are an intelligent deployment planner.
    Given a string input, determine if it contains a valid deployment context - meaning it describes an actual application, use case, or technical setup.
    This is the deployment context: {deployment_context}
    If the input is vague, trivial, or too generic (e.g., "hello world", "test", "just trying stuff", "deployment"), and does not describe a real use case or system, then return: "no deployment context"

    If the string includes a valid deployment context (like a description of a deployed application, its components, or its architecture), return the following structured response:
    {{
        "deployment_context": "<brief description of the actual application or use case>",
        "services": [
        {{
            "name": "<exact IBM Cloud service name from the official IBM Cloud catalog>",
            "count": "<number>",
        "usage": "<brief description of how this service is used in the deployment>"
    }},]}}
    If the input only describes an application use case or intent, recommend IBM Cloud services that would be appropriate. Your response must follow this format:
    {{
        "deployment_context": "<brief description of the intended application or use case>",
        "recommended_services": [
        {{
            "name": "<exact IBM Cloud service name from the official IBM Cloud catalog>",
            "count": "<number>",
        "usage": "<why this service is needed>"
        }},]}}
    Use only real IBM Cloud service names from the IBM Cloud catalog, such as: IBM Cloud Code Engine,IBM Cloud Kubernetes Service,IBM Cloud Foundry,IBM Cloud Databases for PostgreSQL,IBM Cloud Object Storage,IBM Event Streams,
    IBM Cloud Monitoring,IBM Secrets Manager
    Do not invent or generalize service names like "IBM Cloud Web App" or "IBM Hosting Service." Stick strictly to official service names.
    """

    response = ollama.chat(model='granite3.3:8b', messages=[{"role": "user", "content": prompt}], options={
        'temperature': 0.0,       
        'top_p': 1.0,
        'top_k': 1,  
        'repetition_penalty': 1.0 
    })
    return response['message']['content']

def parse_deployment_output(model_output: str):
    if "no deployment context" in model_output.strip().lower():
        return None
        
    try:
        json_block = re.search(r'\{[\s\S]*\}', model_output).group()
        parsed = json.loads(json_block)
        return parsed
    except Exception as e:
        raise ValueError(f"Failed to parse model output as JSON: {e}")

if __name__ == "__main__":
    #deployment_context = "We have deployed an AI chatbot that uses a VM for processing, a Postgres database for storing conversations, and a Redis cache to manage session data."
    #deployment_context = "I want to build a feedback analyzer that takes customer feedback and classifies it by sentiment and urgency."
    deployment_context = "Hello"
    response = analyze_deployment_context(deployment_context)
    print(response)
    parsed_response = parse_deployment_output(response)
    print(parsed_response)
    print(type(parsed_response))
