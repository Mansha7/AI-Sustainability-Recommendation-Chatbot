from fastapi import FastAPI, Request
from pydantic import BaseModel
import asyncio

# Async optimizer functions
from optimisers.cost_optimiser import get_cost_model
from optimisers.sustainability_optimiser import recommend_sustainable_changes
from optimisers.performance_optimiser import recommend_performance_changes
from optimisers.merged_optimiser import get_consolidated_recommendations_with_ollama

# Sync validator functions
from validators.input_validator import analyze_deployment_context, parse_deployment_output

app = FastAPI()

class RecommendationRequest(BaseModel):
    input_text: str
    focus: str

@app.post("/recommend")
async def generate_recommendations(req: RecommendationRequest):
    try:
        print("Focus", req.focus)
        # Step 1: Validate input
        validation_output = analyze_deployment_context(req.input_text)
        if parse_deployment_output(validation_output) is None:
            return {"error": "❗ Please provide valid deployment-related information."}

        # Step 2: Run async optimizations
        cost_task = get_cost_model(req.input_text)
        sustain_task = recommend_sustainable_changes(req.input_text)
        perf_task = recommend_performance_changes(req.input_text)

        try:
            # cost, sustain, perf = await asyncio.gather(cost_task, sustain_task, perf_task)

            cost = await cost_task
            sustain = await sustain_task
            perf =  await perf_task
        except Exception as e:
            print(f"Error occured in first await {e}")
            return {"error": str(e)}   

        # Step 3: Merge recommendations
        if(req.focus == None or req.focus == "None"):
            merged = get_consolidated_recommendations_with_ollama(
                sustain, cost, perf
            )
        else:
            merged = get_consolidated_recommendations_with_ollama(
                sustain, cost, perf, req.focus
            )
        output = {
            "base_recommendations": {
                "Cost": cost,
                "Sustainability": sustain,
                "Performance": perf
            },
            "recommendation": merged
        }
        print(f"Outgoing output: {output}")
        return output
        # return {"recommendation": merged}
    except Exception as e:
        print(f"Error occured in second await {e}")
        return {"error": str(e)}
