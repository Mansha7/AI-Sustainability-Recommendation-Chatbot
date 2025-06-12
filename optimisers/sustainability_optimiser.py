from utils.ollama_client import call_ollama 

async def recommend_sustainable_changes(deployment_context):
    prompt = f"""
    You are an expert in cloud infrastructure sustainability and optimization. Given the context of a deployment on IBM Cloud and a list of services being used, provide no more than 4 of the most impactful recommendations to make the deployment more environmentally sustainable. For each recommendation:
    Explain why it helps reduce environmental impact (e.g., energy efficiency, carbon footprint reduction).
    Attempt to quantify the benefit in terms of reduced energy usage, CO₂ emissions, or cost—either using rough industry averages or clearly stated assumptions.
    Provide specific IBM Cloud service-level changes or configurations if applicable.
    Identify one recommendation as the "best option" overall in terms of sustainability impact vs. effort required.
    
    Deployment context:
    {deployment_context}

    Response Format:
        Recommendation 1: [Title]
        Justification: [Why this helps]
        Estimated Impact: [Quantified or rough estimate]
        IBM Cloud-Specific Steps: [What to do]
        (Repeat for up to 4)
    """

    response = await call_ollama(prompt)
    print(f"Response from Sustainability: {response}")
    return response