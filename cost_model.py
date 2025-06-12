import ollama
import streamlit as st

def get_cost_model(information: str):
    template = f"""
<|start_of_role|>system<|end_of_role|>  
You are an expert in cloud infrastructure cost optimization. You are cautious, ethical, and technically precise.  
<|end_of_text|>  
<|start_of_role|>user<|end_of_role|>
Given the architectural specifications of a deployment, like the RAM, list of services, data centre locations etc., I want you to:
1) Analyse the cost estimation of the application, determine if it's cost-friendly or not.
2) Recommend ways to minimise the cost by analysing what operations can be cut down without affecting performance and sustainability.
3) For each recommendation:
    Provide specific IBM Cloud service-level changes or configurations if applicable.
    Identify one recommendation as the "best option" overall in terms of cost vs. effort required.

Important Instructions:
- Output ONLY the recommendations and the source links or docuemnts where you referenced this data from. Do not dive into the estimation technique and thought process much, output the recommendation directly.
- Privacy: Exclude any personally identifiable information (PII) such as names, email addresses, phone numbers, device IDs, or system locations.
- Ensure your response is concise, accurate, and unbiased, maintaining a professional and respectful tone.
- Answer only using the information present in the input. Do not fabricate details or make assumptions.
- Focus strictly on technical content; omit any greetings, emotions, or conversational elements.
- Consolidate related information where applicable.
- Acronyms: Do not expand acronyms.
- Output: Do not repeat instructions. If no information is available for a topic, do not mention its unavailability. Do not include the specified summary statements.

Response Format:
        Recommendation 1: [Title]
        Justification: [Why this helps]
        Estimated Impact: [Quantified or rough estimate]
        IBM Cloud-Specific Steps: [What to do]
        (Repeat for up to 4)

Application Details:
{information}

<|end_of_text|>
<|start_of_role|>assistant<|end_of_role|>
"""

    response = ollama.chat(
        model='granite3.3:8b',
        messages=[{"role": "user", "content": template}],
        options={
            'temperature': 0.0,
            'top_p': 1.0,
            'top_k': 1,
            'repetition_penalty': 1.0
        }
    )

    return response['message']['content']
