import streamlit as st
import boto3
import os
import json
from botocore.exceptions import NoCredentialsError
from lambda_function import get_prescription_details
from llm import query_bedrock_llm

# Set Page Configuration
st.set_page_config(
    page_title="AskDoc AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AWS Configuration
AWS_REGION = "us-east-1"
BUCKET_NAME = "prescription-uploads1"

# Initialize S3 Client
try:
    s3 = boto3.client("s3", region_name=AWS_REGION)
except NoCredentialsError:
    st.error("AWS Credentials not found! Make sure your environment variables are set.")

# Custom CSS for ChatGPT-like Styling
st.markdown(
    """
    <style>
        body { background-color: #1e1e2f; color: #ffffff; }
        .stApp { background-color: #1e1e2f; }
        .chat-container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background: #2a2a3d;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        }
        .chat-bubble {
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            width: fit-content;
            max-width: 80%;
        }
        .user-bubble { background-color: #4a4a6a; align-self: flex-end; }
        .ai-bubble { background-color: #0084ff; align-self: flex-start; }
        .input-container {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .stButton>button {
            background-color: #0084ff;
            color: white;
            border: none;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for Chat History
st.sidebar.title("📜 Chat History")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for chat in st.session_state["chat_history"][-5:]:
    st.sidebar.write(chat)

if st.sidebar.button("Clear History"):
    st.session_state["chat_history"] = []
    st.sidebar.write("Chat history cleared!")
# Header Image (Centered)
st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="https://wesoftyou.com/wp-content/uploads/2025/01/robot-1280x720_0.jpg" width="700">
    </div>
    """,
    unsafe_allow_html=True
)

# Chat Container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# File Uploader
uploaded_file = st.file_uploader("Choose a prescription file", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    file_name = f"prescriptions/{uploaded_file.name}"
    try:
        s3.upload_fileobj(uploaded_file, BUCKET_NAME, file_name)
        st.success(f"✅ File uploaded successfully to {BUCKET_NAME}/{file_name}")
    except NoCredentialsError:
        st.error("❌ AWS Credentials not found!")
    except Exception as e:
        st.error(f"❌ Upload failed: {str(e)}")

# Patient Name Input
patient_name = st.text_input("Enter Patient Name:")

if st.button("Fetch Prescription"):
    if patient_name:
        prescription_data = get_prescription_details(patient_name)
        if prescription_data:
            st.markdown("### Prescription Details:")
            for item in prescription_data:
                st.markdown(f"<div class='chat-bubble ai-bubble'>🩺 *{item['medicine_name']}* | 💊 {item['dosage']} | ⏳ {item['duration']}</div>", unsafe_allow_html=True)
        else:
            st.error("No prescription found for this patient.")
    else:
        st.warning("⚠ Please enter a patient name.")

# User Query Input
user_query = st.text_area("Ask a question about the prescription:")

if st.button("Submit Query"):
    if user_query:
        prescription_data = get_prescription_details(patient_name)
        if prescription_data:
            ai_response = query_bedrock_llm(prescription_data, user_query)
            st.markdown(f"<div class='chat-bubble user-bubble'>🗨️ {user_query}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-bubble ai-bubble'>🤖 {ai_response}</div>", unsafe_allow_html=True)
            st.session_state["chat_history"].append(f"User: {user_query}")
            st.session_state["chat_history"].append(f"AI: {ai_response}")
        else:
            st.error("No prescription data found. Please fetch the prescription first.")
    else:
        st.warning("⚠ Please enter a query before submitting.")

st.markdown("</div>", unsafe_allow_html=True)