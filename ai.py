import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError

# Set Page Configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="Prescription Upload",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# AWS S3 Configuration
AWS_REGION = "us-east-1"
AWS_ACCESS_KEY = "AKIAW5BDQW63SMBVGJU3"
AWS_SECRET_KEY = "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"
BUCKET_NAME = "prescription-uploads1"

# Initialize S3 Client
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Custom CSS for Styling
st.markdown(
    """
    <style>
        body {
          font-family: Arial, sans-serif;
          background-color: #fff5f5;
          color: #333;
          margin: 0;
          padding: 0;
        }
        .stApp {
          background-color: #fff5f5;
        }
        .about-container {
          max-width: 900px;
          margin: 40px auto;
          padding: 20px;
          background: white;
          border-radius: 10px;
          box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
          text-align: center;
        }
        h1, h2 {
          color: #d9534f;
        }
        p, label {
          font-size: 16px;
          line-height: 1.6;
          color: black;
        }
        .mission-section, .values-section, .team-section {
          margin-top: 30px;
          padding: 20px;
          background: #ffe6e6;
          border-radius: 10px;
        }
        ul {
          list-style-type: none;
          padding: 0;
        }
        li {
          margin: 10px 0;
          font-size: 16px;
        }
        .team-member {
          margin-top: 20px;
          padding: 15px;
          background: white;
          border-radius: 8px;
          box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        }
        .submit-btn {
          background-color: white !important;
          color: black !important;
          font-weight: bold;
          border: 1px solid black;
          padding: 10px;
          border-radius: 5px;
        }
        .clear-history-btn {
          background-color: red !important;
          color: white !important;
          font-weight: bold;
          border: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Custom CSS for Sidebar Text Color
st.sidebar.markdown(
    """
    <style>
        .sidebar-text {
            font-color: white;
            font-size: 16px;
            font-family: Arial, sans-serif;
            margin-bottom: 10px;
        }
        .sidebar-title {
            font-color: white !important;
            font-weight: bold;
            font-size: 20px;
        }
        .stButton>button {
            background-color: #ff4d4d;
            color: white;
            font-weight: bold;
            border: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Title with White Text
st.sidebar.markdown("<h2 class='sidebar-title'>📜 Chat History</h2>", unsafe_allow_html=True)

# Display Chat History
for chat in st.session_state["chat_history"][-5:]:
    st.sidebar.markdown(f"<div class='sidebar-text'>{chat}</div>", unsafe_allow_html=True)

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Styling the sidebar button */
        .stButton>button {
            background-color: white !important;
            color: black !important;
            font-weight: bold;
            border: 2px solid white !important;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: white !important;
            color: black !important;
            border: 2px solid white !important;  
        }
        /* Styling sidebar text */
        .sidebar-text {
            color: white !important;
            font-size: 16px;
            font-family: Arial, sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display Chat History in Sidebar
for chat in st.session_state["chat_history"][-5:]:
    st.sidebar.markdown(f"<p class='sidebar-text'>{chat}</p>", unsafe_allow_html=True)

# Clear Chat History Button (White Text)
if st.sidebar.button("Clear History", key="clear"):
    st.session_state["chat_history"] = []
    st.sidebar.markdown("<p class='sidebar-text'>✅ Chat history cleared!</p>", unsafe_allow_html=True)

# Header Image
st.image("https://wesoftyou.com/wp-content/uploads/2025/01/robot-1280x720_0.jpg", width=700)

# Title
st.markdown("<h1 style='color: #d9534f;'>📄 Talk to AskDoc AI</h1>", unsafe_allow_html=True)
st.write("<p style='color: black;'>Upload your prescription and ask questions about it!</p>", unsafe_allow_html=True)

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

# Divider
st.markdown("---")

# Query Section

st.markdown("<h2 style='color: black;'>💬 Ask about your prescription</h2>", unsafe_allow_html=True)

# User Query Input
user_query = st.text_input("Enter your query")

# Custom Styling for Button and Text
st.markdown(
    """
    <style>
        .submit-btn {
            background-color: #ff4d4d !important;
            color: white !important;
            font-weight: bold;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .query-text {
            color: white;
            font-size: 16px;
            font-family: Arial, sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Submit Button
if st.button("Submit Query", key="submit"):
    if user_query:
        # Process the query (Placeholder response)
        response = f"<p class='query-text'>🔍 Searching for details related to: <b>{user_query}</b></p>"
        st.markdown(response, unsafe_allow_html=True)

        # Save to chat history with white color styling
        st.session_state["chat_history"].append(f"<span class='query-text'>User: {user_query}</span>")
        st.session_state["chat_history"].append(f"<span class='query-text'>AI: Searching for {user_query}...</span>")

        # Refresh chat history in sidebar
        st.sidebar.empty()
        for chat in st.session_state["chat_history"][-5:]:
            st.sidebar.markdown(f"<p class='query-text'>{chat}</p>", unsafe_allow_html=True)
    else:
        st.warning("⚠ Please enter a query before submitting.")
