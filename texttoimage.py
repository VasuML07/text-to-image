import streamlit as st
import requests
import io
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Visionary AI",
    page_icon="🌌",
    layout="wide"
)

# 2. API Configuration & Mappings
# Freepik requires these specific slugs for the 'size' parameter
STYLE_MAP = {
    "None": None,
    "Photographic": "photo",
    "Digital Art": "digital_art",
    "Comic Book": "comic",
    "Fantasy Art": "fantasy",
    "Cyberpunk": "cyberpunk",
    "Cinematic": "cinematic"
}

ASPECT_RATIO_MAP = {
    "1:1 (Square)": "square_1_1",
    "16:9 (Widescreen)": "widescreen_16_9",
    "4:3 (Standard)": "classic_4_3",
    "2:3 (Portrait)": "portrait_2_3"
}

# Access the API key from .streamlit/secrets.toml
if "FREEPIK_API_KEY" in st.secrets:
    API_KEY = st.secrets["FREEPIK_API_KEY"]
else:
    st.error("🔑 API Key 'FREEPIK_API_KEY' not found in Streamlit Secrets!")
    st.stop()

API_URL = "https://api.freepik.com/v1/ai/text-to-image"

# 3. Sidebar UI
with st.sidebar:
    st.title("⚙️ Configuration")
    selected_style = st.selectbox("Artistic Style", list(STYLE_MAP.keys()), index=1)
    selected_ratio = st.selectbox("Aspect Ratio", list(ASPECT_RATIO_MAP.keys()), index=0)

# 4. Main UI
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.title("🌌 Visionary AI")
    prompt = st.text_area("Describe your masterpiece:", height=200)
    generate_btn = st.button("🚀 Generate Masterpiece")

with col2:
    if generate_btn:
        if not prompt.strip():
            st.error("Please enter a description.")
        else:
            with st.status("🎨 Rendering your vision...", expanded=True) as status:
                try:
                    headers = {
                        "Content-Type": "application/json",
                        "x-freepik-api-key": API_KEY
                    }

                    # Correct JSON payload for Freepik v1
                    payload = {
                        "prompt": prompt.strip(),
                        "image": {
                            "size": ASPECT_RATIO_MAP[selected_ratio]
                        }
                    }
                    
                    if STYLE_MAP[selected_style]:
                        payload["styling"] = {"style": STYLE_MAP[selected_style]}

                    response = requests.post(API_URL, headers=headers, json=payload)

                    if response.ok:
                        data = response.json()
                        # Fix: Freepik returns a list of objects in the 'data' field
                        image_url = data.get("data", [{}])[0].get("url")
                        
                        if image_url:
                            # Step 2: Fetch the actual image from the generated URL
                            img_data = requests.get(image_url).content
                            img = Image.open(io.BytesIO(img_data))
                            
                            status.update(label="✅ Success!", state="complete", expanded=False)
                            st.image(img, use_container_width=True)
                            
                            # Download Logic
                            st.download_button("🖼️ Download PNG", data=img_data, file_name="ai_art.png", mime="image/png")
                        else:
                            st.error("API success, but no image URL was found in the response.")
                    else:
                        st.error(f"API Error {response.status_code}: {response.text}")

                except Exception as e:
                    # Fix: This except block prevents the SyntaxError from your screenshot
                    st.error(f"Request failed: {e}")
    else:
        st.info("Your image will appear here.")
