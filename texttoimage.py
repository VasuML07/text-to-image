import streamlit as st
import requests
import io
from PIL import Image

# 1. Page Setup
st.set_page_config(page_title="Visionary AI", page_icon="🌌", layout="wide")

# 2. Corrected 2026 API Slugs
# If 'invalid_params' persists, 'None' is the safest choice to verify connection.
STYLE_MAP = {
    "None": None,
    "Cinematic": "cinematic",
    "Digital Art": "digital_art",
    "Photographic": "photo",
    "Fantasy": "fantasy",
    "Comic Book": "comic",
    "Cyberpunk": "cyberpunk"
}

ASPECT_RATIO_MAP = {
    "1:1 (Square)": "square_1_1",
    "16:9 (Widescreen)": "widescreen_16_9",
    "4:3 (Classic)": "classic_4_3"
}

# 3. API Authentication
if "FREEPIK_API_KEY" in st.secrets:
    API_KEY = st.secrets["FREEPIK_API_KEY"]
else:
    st.error("🔑 API Key 'FREEPIK_API_KEY' not found in Secrets!")
    st.stop()

API_URL = "https://api.freepik.com/v1/ai/text-to-image"

# 4. Main UI Logic
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.title("🌌 Visionary AI")
    prompt = st.text_area("Describe your masterpiece:", height=200)
    
    with st.sidebar:
        st.header("⚙️ Settings")
        selected_style = st.selectbox("Style", list(STYLE_MAP.keys()), index=0)
        selected_ratio = st.selectbox("Aspect Ratio", list(ASPECT_RATIO_MAP.keys()), index=0)

    generate_btn = st.button("🚀 Generate Masterpiece")

with col2:
    if generate_btn:
        if not prompt.strip():
            st.error("Please enter a description.")
        else:
            with st.status("🎨 Rendering...", expanded=True) as status:
                try:
                    headers = {
                        "Content-Type": "application/json",
                        "x-freepik-api-key": API_KEY
                    }

                    # Constructed JSON payload
                    payload = {
                        "prompt": prompt.strip(),
                        "image": {
                            "size": ASPECT_RATIO_MAP[selected_ratio]
                        }
                    }
                    
                    # Only add styling if a style is actually selected
                    api_style = STYLE_MAP[selected_style]
                    if api_style:
                        payload["styling"] = {"style": api_style}

                    response = requests.post(API_URL, headers=headers, json=payload)

                    if response.ok:
                        data = response.json()
                        image_url = data.get("data", [{}])[0].get("url")
                        
                        if image_url:
                            img_data = requests.get(image_url).content
                            st.image(Image.open(io.BytesIO(img_data)), use_container_width=True)
                            status.update(label="✅ Success!", state="complete")
                        else:
                            st.error("No image URL found in response.")
                    else:
                        # 400 Error Debugging
                        st.error(f"❌ API Error {response.status_code}")
                        with st.expander("Show Technical Error Details"):
                            st.json(response.json()) # This will tell you EXACTLY which field is wrong

                except Exception as e:
                    st.error(f"System Error: {e}")
