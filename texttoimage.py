import streamlit as st
import requests
import io
from PIL import Image

# ... (page_config and styles stay the same) ...

# --- STYLE MAPPING ---
# These are the standard slugs Freepik expects
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
    "1:1 (Square)": "square",
    "16:9 (Widescreen)": "landscape",
    "4:3 (Standard)": "standard",
    "2:3 (Portrait)": "portrait"
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configuration")
    selected_style_name = st.selectbox("Artistic Style", list(STYLE_MAP.keys()), index=1)
    selected_ratio_name = st.selectbox("Aspect Ratio", list(ASPECT_RATIO_MAP.keys()), index=0)

# --- MAIN LOGIC ---
if generate_btn:
    if not prompt.strip():
        st.error("Please enter a description.")
    else:
        with st.status("🎨 Rendering your vision...", expanded=True) as status:
            try:
                headers = {
                    "Content-Type": "application/json",
                    "x-freepik-api-key": st.secrets["FREEPIK_API_KEY"]
                }

                # Construct Payload
                payload = {
                    "prompt": prompt.strip(),
                    "image": {
                        "size": ASPECT_RATIO_MAP[selected_ratio_name]
                    }
                }
                
                # Only add styling if it's not "None"
                api_style = STYLE_MAP[selected_style_name]
                if api_style:
                    payload["styling"] = {"style": api_style}

                response = requests.post(API_URL, headers=headers, json=payload)

                if response.ok:
                    data = response.json()
                    # Freepik usually returns a list of images in the 'data' key
                    image_url = data.get("data", [{}])[0].get("url")
                    
                    if image_url:
                        img_response = requests.get(image_url)
                        # ... (rest of the image processing code)
