import streamlit as st
import requests

def process_prompt():
    print("Saved input:", st.session_state.saved_input)
    if st.session_state.user_input or st.session_state.saved_input:
        image_note = "\nAn architecture diagram is also uploaded." if uploaded_image else ""
        user_input = st.session_state.user_input
        full_input_str = user_input + image_note
        st.session_state.saved_input = full_input_str
        selected_focus = st.session_state.selected_focus

        st.chat_message("user").markdown(full_input_str)

        with st.spinner("Sending to async backend for validation + recommendations..."):
            try:
                response = requests.post(
                    "http://localhost:8010/recommend",  # FastAPI backend
                    json={"input_text": full_input_str, "focus": selected_focus}
                )
                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.session_state.data=data["base_recommendations"]
                    st.session_state.recommendations_data = data["recommendation"]
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

def process_focus():
    print("Saved input on changing focus:", st.session_state.saved_input)
    if (st.session_state.saved_input) and st.session_state.selected_focus:
        image_note = "\nAn architecture diagram is also uploaded." if uploaded_image else ""
        user_input = st.session_state.saved_input
        full_input_str = user_input + image_note
        # st.session_state.saved_input = full_input_str
        selected_focus = st.session_state.selected_focus

        st.chat_message("user").markdown(full_input_str)

        with st.spinner("Sending to async backend for validation + recommendations..."):
            try:
                response = requests.post(
                    "http://localhost:8010/recommend",  # FastAPI backend
                    json={"input_text": full_input_str, "focus": selected_focus}
                )
                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.session_state.data=data["base_recommendations"]
                    st.session_state.recommendations_data = data["recommendation"]
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

def process_input():
    st.session_state.saved_input = user_input

st.title("🌿 Sustainable Deployment Chatbot")

if "recommendations_data" not in st.session_state:
    st.session_state.recommendations_data = None

if "saved_input" not in st.session_state:
    st.session_state.saved_input = None

selected_focus = st.radio(
    "What do you want to prioritize?",
    options=["None","Prioritize Cost", "Prioritize Performance", "Prioritize Sustainability"],
    key="selected_focus",
    # index=None,
    on_change=process_focus,
    horizontal=True
)

uploaded_image = st.file_uploader("📎 Upload architecture diagram (optional):", type=["png", "jpg", "jpeg"])
user_input = st.chat_input(
    "Enter your app deployment details...",
    key="user_input",
    on_submit=process_prompt
)

# if user_input or st.session_state.saved_input:
#     print("Processing prompts")
#     image_note = "\nAn architecture diagram is also uploaded." if uploaded_image else ""
#     if user_input:
#         user_input_str = user_input
#     else:
#         user_input_str = st.session_state.saved_input
#     full_input_str = user_input_str + image_note
#     # st.session_state.saved_input = user_input_str

#     st.chat_message("user").markdown(full_input_str)

#     with st.spinner("Sending to async backend for validation + recommendations...", show_time=True):
#         try:
#             response = requests.post(
#                 "http://localhost:8010/recommend",  # FastAPI backend
#                 json={"input_text": full_input_str, "focus": selected_focus}
#             )
#             data = response.json()

#             if "error" in data:
#                 st.error(data["error"])
#             else:
#                 st.session_state.recommendations_data = data["recommendation"]
#         except Exception as e:
#             st.error(f"Failed to connect to backend: {e}")

# Display recommendation
if st.session_state.recommendations_data:
    st.chat_message("assistant").markdown("## ✨ Consolidated Recommendations:")
    st.chat_message("assistant").markdown(st.session_state.recommendations_data)

if("data" in st.session_state):
    data = st.session_state.data
    data["None"] = ""
    data_list = list(st.session_state.data.keys())
    # data_list.append({"None": ""})
    choice = st.selectbox("Select other recommendations", data_list, index=3)
    st.markdown(f"{data[choice]}")