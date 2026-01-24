import streamlit as st
import requests
import io
import base64  # Added to handle the image data format you received
from PIL import Image

# 1. Page Setup
st.set_page_config(page_title="Visionary AI", page_icon="🌌", layout="wide")

# 2. Verified API Mappings
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
    "4:3 (Classic)": "classic_4_3",
    "2:3 (Portrait)": "portrait_2_3"
}

# 3. API Key Check
if "FREEPIK_API_KEY" in st.secrets:
    API_KEY = st.secrets["FREEPIK_API_KEY"]
else:
    st.error("🔑 API Key 'FREEPIK_API_KEY' not found in Secrets!")
    st.stop()

API_URL = "https://api.freepik.com/v1/ai/text-to-image"

# 4. UI Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.title("🌌 Visionary AI")
    prompt = st.text_area("Describe your masterpiece:", height=200, placeholder="A dog on a cat...")
    
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
            with st.status("🎨 Rendering your vision...", expanded=True) as status:
                try:
                    headers = {
                        "Content-Type": "application/json",
                        "x-freepik-api-key": API_KEY
                    }

                    payload = {
                        "prompt": prompt.strip(),
                        "image": {
                            "size": ASPECT_RATIO_MAP[selected_ratio]
                        },
                        "num_images": 1
                    }
                    
                    if STYLE_MAP[selected_style]:
                        payload["styling"] = {"style": STYLE_MAP[selected_style]}

                    response = requests.post(API_URL, headers=headers, json=payload)

                    if response.ok:
                        res_data = response.json()
                        images = res_data.get("data", [])

                        if images:
                            # --- FIX: CHECK FOR URL OR BASE64 ---
                            if "url" in images[0]:
                                # If it's a link, download it
                                img_data = requests.get(images[0]["url"]).content
                            elif "base64" in images[0]:
                                # If it's Base64 (like in your error), decode it
                                img_data = base64.b64decode(images[0]["base64"])
                            else:
                                st.error("No image data found in response.")
                                st.stop()

                            img = Image.open(io.BytesIO(img_data))
                            status.update(label="✅ Success!", state="complete", expanded=False)
                            st.image(img, use_container_width=True)
                            
                            # Download Buttons
                            st.download_button("🖼️ Download PNG", data=img_data, file_name="ai_art.png", mime="image/png")
                        else:
                            st.error("Empty data list received from API.")
                    else:
                        st.error(f"API Error {response.status_code}")
                        st.json(response.json())

                except Exception as e:
                    st.error(f"System Error: {e}")
    else:
        st.info("Your image will appear here.")
