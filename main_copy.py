import streamlit as st
import ollama
import asyncio
from optimisers.cost_optimiser import get_cost_model
from optimisers.sustainability_optimiser import recommend_sustainable_changes
from optimisers.performance_optimiser import recommend_performance_changes
from validators.input_validator import analyze_deployment_context, parse_deployment_output
from optimisers.merged_optimiser import get_consolidated_recommendations_with_ollama

# ** --- Functions --- **

# ---- Async Call Function ----
async def async_chat_call(prompt, user_input, label, index):
    try:
        print('running for label:', label)
        response = await asyncio.to_thread(
            ollama.chat,
            model="granite3.3:8b",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            options={
                "temperature": 0.3,
                "top_p": 1.0,
                "top_k": 40,
                "repetition_penalty": 1.1
            }
        )
        print(label + "response:" + response['message']['content'])
        return label, response['message']['content']
    except Exception as e:
        return label, f"⚠️ Error: {str(e)}"

# ---- Coroutine Launcher ----
async def run_all_prompts(full_input):
    # focus_note = f"\nPrioritize recommendation on optimizing {selected_focus.lower()}." if selected_focus else ""

    cost_prompt = get_cost_model(full_input)
    sustainability_prompt = recommend_sustainable_changes(full_input)
    performance_prompt = recommend_performance_changes(full_input)

    tasks = [
        asyncio.create_task(async_chat_call(cost_prompt, full_input, "💰 **Cost Recommendations:**", 0)),
        asyncio.create_task(async_chat_call(sustainability_prompt, full_input, "🌿 **Sustainability Recommendations:**", 1)),
        asyncio.create_task(async_chat_call(performance_prompt, full_input, "⚙️ **Performance Recommendations:**", 2))
    ]

    # results = await asyncio.gather(*tasks)
    results = []
    for task in tasks:
        result = await task
        results.append(result)
    return results

def reset_state():
    print("Resetting focus state with user input", st.session_state.get("user_input"))
    # Reset or clear session state keys as needed
    if "messages" in st.session_state:
        st.session_state.messages = []
    focus = st.session_state.get("selected_focus")
    context = st.session_state.get("saved_input")
    if focus and context:
        st.session_state.messages.append({"role": "user", "content": context}) # index 0
        if ("prompt_responses" not in st.session_state or len(st.session_state.prompt_responses) == 0):
            run_task_prompts(context)
        response = consolidate_prompts(focus)
        st.session_state.messages.append({"role": "assistant", "content": response})


def reset_prompts():
    print("Resetting prompts")
    if "prompt_responses" in st.session_state:
        st.session_state.prompt_responses = []
    if st.session_state.get("user_input"):
        user_input = st.session_state.get("user_input")
        st.session_state.saved_input = user_input
        # image_note = "\nAn architecture diagram is also uploaded." if uploaded_image else ""
        full_input = user_input
        # context = full_input
        # if len(st.session_state.messages) > 1:
        #     context += st.session_state.messages[-2]["content"]

        st.session_state.messages.append({"role": "user", "content": full_input}) # index 0

        validation_output = analyze_deployment_context(full_input)

        if parse_deployment_output(validation_output) is not None:
            run_task_prompts(full_input)
            focus = st.session_state.selected_focus
            response = consolidate_prompts(focus)
            st.session_state.messages.append({"role": "assistant", "content": response})

        else:
            response = "❗ Please provide deployment-related information."
            st.session_state.messages.append({"role": "assistant", "content": response})
    

def run_task_prompts(full_input):
    with st.spinner("Gathering recommendations...", show_time=True):
        # responses = asyncio.run(run_all_prompts(full_input))
        cost_response = get_cost_model(full_input)
        sustainability_response = recommend_sustainable_changes(full_input)
        performance_response = recommend_performance_changes(full_input)
    responses = [cost_response, sustainability_response, performance_response]
    st.session_state.prompt_responses = responses

def consolidate_prompts(selected_focus):
    responses = st.session_state.prompt_responses
    with st.spinner("Consolidating response...", show_time=True):
        if selected_focus!=None:
            response = get_consolidated_recommendations_with_ollama(responses[1], responses[0], responses[2], selected_focus)
        else:
            response = get_consolidated_recommendations_with_ollama(responses[1], responses[0], responses[2])
    return response


#******************************************************************************************************************************************
# **--- Application ---**

st.title("🌿 Sustainable Deployment Chatbot")
# st.session_state["user_input"] = ""

st.chat_input(
    "Enter your app deployment details...",
    key="user_input",
    on_submit= reset_prompts
)
context = st.session_state.get("user_input")
st.radio(
    "What do you want to prioritize?",
    options=["Cost", "Performance", "Sustainability"],
    index=None,
    key="selected_focus",
    on_change= reset_state,
    horizontal=True
)
uploaded_image = st.file_uploader("📎 Upload architecture diagram (optional):", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- Input Handling ----
# if user_input:
#     image_note = "\nAn architecture diagram is also uploaded." if uploaded_image else ""
#     full_input = user_input + image_note
#     context = full_input
#     if len(st.session_state.messages) > 1:
#         context += st.session_state.messages[-2]["content"]

#     st.session_state.messages.append({"role": "user", "content": full_input}) # index 0

#     validation_output = analyze_deployment_context(context)

#     if parse_deployment_output(validation_output) is not None:
#         # st.chat_message("user").markdown(full_input)
#         # with st.spinner("Gathering recommendations...", show_time=True):
#         #     # responses = asyncio.run(run_all_prompts(full_input))
#         #     cost_response = get_cost_model(full_input)
#         #     sustainability_response = recommend_sustainable_changes(full_input)
#         #     performance_response = recommend_performance_changes(full_input)

#         run_task_prompts(full_input)
#         # st.session_state.prompt_responses = responses
            
#         # with st.spinner("Consolidating response...", show_time=True):
#         #     if selected_focus!="":
#         #         response = get_consolidated_recommendations_with_ollama(sustainability_response, cost_response, performance_response, selected_focus)
#         #     else:
#         #         response = get_consolidated_recommendations_with_ollama(sustainability_response, cost_response, performance_response)
#         focus = st.session_state.selected_focus
#         response = consolidate_prompts(focus)
#         # st.chat_message("assistant").markdown(response)
#         st.session_state.messages.append({"role": "assistant", "content": response})

#     else:
#         response = "❗ Please provide deployment-related information."
#         # st.chat_message("assistant").markdown(response)
#         st.session_state.messages.append({"role": "assistant", "content": response})

for msg in st.session_state.messages:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
