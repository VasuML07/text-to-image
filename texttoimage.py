# Import Streamlit to build the web app UI
import streamlit as st
# Used to send HTTP requests to external APIs
import requests
# Helps handle raw bytes as file-like objects (needed for images)
import io
# Used to decode Base64 image data returned by the API
import base64
# Pillow library to open and manipulate images in Python
from PIL import Image
# PAGE CONFIGURATION
# Set the app title, browser tab icon, and use full-width layout
st.set_page_config(
    page_title="Visionary AI",
    page_icon="🌌",
    layout="wide"
)
# USER-FRIENDLY → API VALUE MAPPINGS
# Maps dropdown style names to Freepik API-compatible style values
STYLE_MAP = {
    "None": None,              # No styling applied
    "Cinematic": "cinematic",
    "Digital Art": "digital_art",
    "Photographic": "photo",
    "Fantasy": "fantasy",
    "Comic Book": "comic",
    "Cyberpunk": "cyberpunk"
}
# Maps readable aspect ratios to Freepik API size parameters
ASPECT_RATIO_MAP = {
    "1:1 (Square)": "square_1_1",
    "16:9 (Widescreen)": "widescreen_16_9",
    "4:3 (Classic)": "classic_4_3",
    "2:3 (Portrait)": "portrait_2_3"
}

# API KEY VALIDATION
# Check if the Freepik API key exists in Streamlit Secrets
if "FREEPIK_API_KEY" in st.secrets:
    # Load API key securely (never hardcode keys)
    API_KEY = st.secrets["FREEPIK_API_KEY"]
else:
    # Stop the app immediately if the key is missing
    st.error("🔑 API Key 'FREEPIK_API_KEY' not found in Secrets!")
    st.stop()
# Freepik Text-to-Image API endpoint
API_URL = "https://api.freepik.com/v1/ai/text-to-image"
# UI LAYOUT
# Create two columns: left for input, right for output
col1, col2 = st.columns([1, 1.2], gap="large")
# LEFT COLUMN: USER INPUT
with col1:
    # App title shown at the top
    st.title("🌌 Visionary AI")
    # Text area where the user describes the image they want
    prompt = st.text_area(
        "Describe your masterpiece:",
        height=200,
        placeholder="A dog on a cat..."
    )
    # Sidebar for configuration options
    with st.sidebar:
        # Sidebar section title
        st.header("⚙️ Settings")

        # Dropdown to select visual style
        selected_style = st.selectbox(
            "Style",
            list(STYLE_MAP.keys()),
            index=0
        )
        # Dropdown to select image aspect ratio
        selected_ratio = st.selectbox(
            "Aspect Ratio",
            list(ASPECT_RATIO_MAP.keys()),
            index=0
        )
    # Button that triggers image generation
    generate_btn = st.button("🚀 Generate Masterpiece")
# RIGHT COLUMN: OUTPUT
with col2:
    # Only run this block when the button is clicked
    if generate_btn:
        # Prevent API call if prompt is empty or just whitespace
        if not prompt.strip():
            st.error("Please enter a description.")
        else:
            # Show a progress/status indicator while generating
            with st.status("🎨 Rendering your vision...", expanded=True) as status:
                try:
                    # HTTP headers required by Freepik API
                    headers = {
                        "Content-Type": "application/json",
                        "x-freepik-api-key": API_KEY
                    }
                    # Main request payload sent to the API
                    payload = {
                        "prompt": prompt.strip(),  # Clean user input
                        "image": {
                            "size": ASPECT_RATIO_MAP[selected_ratio]
                        },
                        "num_images": 1           # Generate only one image
                    }

                    # Add style only if user selected one
                    if STYLE_MAP[selected_style]:
                        payload["styling"] = {
                            "style": STYLE_MAP[selected_style]
                        }
                    # Send POST request to Freepik API
                    response = requests.post(
                        API_URL,
                        headers=headers,
                        json=payload
                    )
                    # Check if request succeeded
                    if response.ok:
                        # Convert JSON response into Python dictionary
                        res_data = response.json()
                        # Extract image data safely
                        images = res_data.get("data", [])
                        if images:
                            # If API returned a hosted image URL
                            if "url" in images[0]:
                                img_data = requests.get(
                                    images[0]["url"]
                                ).content
                            # If API returned Base64-encoded image data
                            elif "base64" in images[0]:
                                img_data = base64.b64decode(
                                    images[0]["base64"]
                                )
                            # If image data format is unexpected
                            else:
                                st.error("No image data found in response.")
                                st.stop()
                            # Convert raw bytes into an image object
                            img = Image.open(io.BytesIO(img_data))
                            # Update progress status to success
                            status.update(
                                label="✅ Success!",
                                state="complete",
                                expanded=False
                            )
                            # Display the generated image
                            st.image(
                                img,
                                use_container_width=True
                            )
                            # Allow user to download the image
                            st.download_button(
                                "🖼️ Download PNG",
                                data=img_data,
                                file_name="ai_art.png",
                                mime="image/png"
                            )
                        # Handle empty image response
                        else:
                            st.error("Empty data list received from API.")
                    # Handle non-200 API responses
                    else:
                        st.error(f"API Error {response.status_code}")
                        st.json(response.json())
                # Catch unexpected runtime errors
                except Exception as e:
                    st.error(f"System Error: {e}")
    # Default message before any image is generated
    else:
        st.info("Your image will appear here.")

