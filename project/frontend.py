import streamlit as st
from PIL import Image
import requests

# Page Configuration
st.set_page_config(
    page_title="Dynamic Anti-Spoofing with GANs",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Styling and Animations
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            color: white;
            font-family: 'Roboto', sans-serif;
        }
        .main-header {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #f953c6, #b91d73);
            -webkit-background-clip: text;
            color: transparent;
            padding: 10px 0;
        }
        .sub-header {
            font-size: 22px;
            text-align: center;
            color: #000111;
            margin-bottom: 20px;
        }
        .sidebar-header {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 20px;
            padding: 10px 0;
            animation: glow 1.5s infinite alternate;
            box-shadow: 0px 4px 10px rgba(0, 191, 255, 0.7);
        }
        .sidebar-header::before {
            content: '🛡️';
            position: absolute;
            left: -40px;
            top: 0;
            font-size: 32px;
        }
        @keyframes glow {
            from {
                text-shadow: 0 0 5px #00c6ff, 0 0 10px #00c6ff;
            }
            to {
                text-shadow: 0 0 20px #00c6ff, 0 0 30px #0072ff;
            }
        }
        .sidebar-section {
            background: linear-gradient(135deg, #282c34, #3c3f47);
            padding: 20px;
            border: 2px solid #00c6ff;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0, 191, 255, 0.5);
        }
        .result-container {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.7);
            animation: fadeIn 1s ease-out;
        }
        .result-text {
            font-size: 32px;
            font-weight: bold;
            padding: 10px;
        }
        .real {
            color: #00ff7f;
        }
        .fake {
            color: #ff4500;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: scale(0.8);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        .upload-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border: 2px dashed #ffe77a;
            border-radius: 10px;
            text-align: center;
            animation: pulse 2s infinite;
        }
        .upload-box:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.05);
            transition: 0.3s ease;
        }
        @keyframes pulse {
            0% {
                border-color: #ffe77a;
                box-shadow: 0 0 5px #ffe77a;
            }
            50% {
                border-color: #ffd700;
                box-shadow: 0 0 20px #ffd700;
            }
            100% {
                border-color: #ffe77a;
                box-shadow: 0 0 5px #ffe77a;
            }
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 18px;
            color: #ffe77a;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main Header
st.markdown(
    """
    <div>
        <h1 class="main-header">Revolutionizing Deepfake Detection with GANs</h1>
        <p class="sub-header">Using Generative AI to combat fake media with cutting-edge anti-spoofing techniques.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar with Prototype Name and Styled Section
st.sidebar.markdown(
    """
    <div class="sidebar-section">
        <h1 class="sidebar-header">SentinelGuard</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar for Image Upload
st.sidebar.title("📤 Upload Your Image")
uploaded_file = st.sidebar.file_uploader(
    "Choose an image to analyze", type=["jpg", "jpeg", "png"]
)

# Main Layout with Two Columns
col1, col2 = st.columns([1, 2])

# Column 1: Image Upload and Display
with col1:
    st.markdown("### Uploaded Image")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
    else:
        st.markdown(
            """
            <div class="upload-box">
                <p>Upload an image to analyze.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Column 2: Analysis Results
with col2:
    st.markdown("### Results")
    if uploaded_file is not None:
        st.markdown("Analyzing the uploaded image... ⏳")
        try:
            # Send image to the backend
            response = requests.post(
                "http://127.0.0.1:5000/api/authenticate",
                files={"file": uploaded_file.getvalue()},
            )

            if response.status_code == 200:
                result = response.json().get("result")
                if result == "Real":
                    st.markdown(
                        """
                        <div class="result-container">
                            <p class="result-text real">✅ The image is classified as <b>Real</b>.</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                elif result == "Fake":
                    st.markdown(
                        """
                        <div class="result-container">
                            <p class="result-text fake">❌ The image is classified as <b>Fake</b>.</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.warning("Unexpected result. Please check the backend.")
            else:
                st.error("Error processing the image. Please try again later.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Upload an image to see the analysis.")


