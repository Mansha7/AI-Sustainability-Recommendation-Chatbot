import ollama


def get_consolidated_recommendations_with_ollama(sustainability_recs,cost_recs,performance_recs,prioritization="sustainability",):

    prompt = f"""You are an expert Cloud Solutions Architect specializing in multi-objective optimization for sustainability, performance, and cost. You will be provided with three sets of optimization recommendations for a deployment on IBM Cloud:
                    1. Environmentally Sustainable Recommendations
                    2. Cost Optimized Recommendations
                    3. Performance Optimized Recommendations

                    You will also receive input on which objective to prioritize: **Sustainability**, **Performance**, or **Cost**. If no specific priority is given, default to **Sustainability**.

                    Your task is to analyze all provided recommendations and generate a final, consolidated set of no more than 4 of the most impactful and balanced recommendations. For each final recommendation:
                        * Clearly state the recommendation.
                        * Explain its overall benefits, particularly how it aligns with the prioritized objective while considering the other two.
                        * Attempt to quantify the impact in terms relevant to the prioritized objective (e.g., reduced energy usage for sustainability, cost savings for cost, or performance metrics for performance). If possible, briefly touch on impacts to the other objectives.
                        * Provide specific IBM Cloud service-level changes or configurations if applicable.
                        * Identify one recommendation as the "overall best option" considering the given priority and the balance across all three objectives.
                    Acknowledge any direct conflicts between the initial sets of recommendations and explain how your final recommendations attempt to resolve or balance these conflicts based on the given priority.

                    **Inputs:**

                    1.  **Sustainability Recommendations:**{sustainability_recs}
                    2.  **Cost Optimized Recommendations:**{cost_recs}
                    3.  **Performance Optimized Recommendations:**{performance_recs}
                    4.  **Prioritization Weight (optional, default is Sustainability):** {prioritization}

                    **Response Format:**

                    Overall Prioritization: [State the objective being prioritized based on input or default]

                    Consolidated Recommendation 1: [Title]
                    Overall Benefit & Alignment: [Explanation]
                    Estimated Impact: [Quantified or rough estimate, focusing on prioritized objective]
                    IBM Cloud-Specific Steps: [What to do]
                    (Repeat for up to 4 recommendations)
                """
    response = ollama.chat(model='granite3.3:8b', messages=[{"role": "user", "content": prompt}], options={
        'temperature': 0.0,       
        'top_p': 1.0,
        'top_k': 1,  
        'repetition_penalty': 1.0 
    })
    return response['message']['content']

if __name__ == "__main__":
    sample_sustainability_recs = """
Recommendation 1: Adopt Serverless Architectures (IBM Cloud Functions)
Justification: Reduces energy by only consuming resources when code is executed, eliminating idle server time.
Estimated Impact: Potential 50-90% reduction in energy for event-driven workloads compared to always-on VMs.
IBM Cloud-Specific Steps: Refactor monolithic applications or develop new microservices using IBM Cloud Functions. Configure pay-per-use pricing.

Recommendation 2: Optimize Data Storage Lifecycle (IBM Cloud Object Storage Tiers)
Justification: Moving infrequently accessed data to cooler storage tiers reduces energy for storage and cooling.
Estimated Impact: 10-40% energy saving on storage depending on data access patterns.
IBM Cloud-Specific Steps: Use lifecycle policies in IBM Cloud Object Storage to automatically transition data from Standard to Vault or Cold Vault tiers.
"""

    sample_cost_recs = """
Recommendation 1: Implement Autoscaling for Kubernetes Clusters (IBM Cloud Kubernetes Service)
Justification: Matches resource allocation to demand, avoiding costs for unused capacity during off-peak hours.
Estimated Impact: 15-50% cost reduction for variable workloads.
IBM Cloud-Specific Steps: Configure Horizontal Pod Autoscaler (HPA) and Cluster Autoscaler in IKS based on CPU/memory metrics.

Recommendation 2: Leverage Spot Instances for Batch Processing (IBM Cloud Virtual Servers)
Justification: Offers significant cost savings (up to 80%) for fault-tolerant batch workloads that can handle interruptions.
Estimated Impact: 50-80% cost reduction for suitable batch jobs.
IBM Cloud-Specific Steps: Provision Spot VSIs for non-critical batch processing tasks, ensuring application resilience.
"""

    sample_performance_recs = """
Recommendation 1: Use a Global Load Balancer (IBM Cloud Internet Services - GLB)
Justification: Distributes traffic to the healthiest and geographically closest data centers, reducing latency and improving availability.
Estimated Impact: 10-30% latency improvement for globally distributed users.
IBM Cloud-Specific Steps: Configure GLB in IBM CIS with health checks and appropriate origin pools pointing to your application servers.

Recommendation 2: Enable In-Memory Caching (IBM Cloud Data Engine or Databases for Redis)
Justification: Speeds up access to frequently used data by storing it in memory, reducing database load and response times.
Estimated Impact: Can improve application response times by 20-60% for data-intensive operations.
IBM Cloud-Specific Steps: Integrate IBM Cloud Databases for Redis for session caching or frequently accessed query results.
"""

    print("--- Scenario 1: Prioritizing Sustainability (Default) ---")
    consolidated_output_sustainability = get_consolidated_recommendations_with_ollama(
        sustainability_recs=sample_sustainability_recs,
        cost_recs=sample_cost_recs,
        performance_recs=sample_performance_recs,
        prioritization=[])
    print("\nOllama Response:\n", consolidated_output_sustainability)
    print("\n" + "="*70 + "\n")

    print("--- Scenario 2: Prioritizing Cost ---")
    consolidated_output_cost = get_consolidated_recommendations_with_ollama(
        sustainability_recs=sample_sustainability_recs,
        cost_recs=sample_cost_recs,
        performance_recs=sample_performance_recs,
        prioritization=['prioritize cost']
    )
    print("\nOllama Response:\n", consolidated_output_cost)
    print("\n" + "="*70 + "\n")

    print("--- Scenario 3: Prioritizing Performance with specific balance ---")
    consolidated_output_performance = get_consolidated_recommendations_with_ollama(
        sustainability_recs=sample_sustainability_recs,
        cost_recs=sample_cost_recs,
        performance_recs=sample_performance_recs,
        prioritization=['prioritize cost','prioritize performance']
    )
    print("\nOllama Response:\n", consolidated_output_performance)