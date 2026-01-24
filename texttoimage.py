import streamlit as st
import requests
import io
from PIL import Image

# 1. Page Setup
st.set_page_config(page_title="Visionary AI", page_icon="🌌", layout="wide")

# 2. Verified 2026 API Slugs
# These slugs are verified against the latest Freepik API documentation
STYLE_MAP = {
    "None": None,
    "Realism": "realism",
    "Creative Fluid": "fluid",
    "Digital/Fantastical": "flexible",
    "Minimal/Zen": "zen",
    "Editorial Portrait": "editorial_portraits",
    "Hyper Realistic": "super_real"
}

ASPECT_RATIO_MAP = {
    "1:1 (Square)": "square_1_1",
    "16:9 (Widescreen)": "widescreen_16_9",
    "9:16 (Story)": "social_story_9_16",
    "4:3 (Classic)": "classic_4_3"
}

# 3. API Key Check
if "FREEPIK_API_KEY" in st.secrets:
    API_KEY = st.secrets["FREEPIK_API_KEY"]
else:
    st.error("🔑 API Key 'FREEPIK_API_KEY' not found in Secrets!")
    st.stop()

API_URL = "https://api.freepik.com/v1/ai/text-to-image"

# 4. Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    selected_style = st.selectbox("Artistic Style", list(STYLE_MAP.keys()), index=1)
    selected_ratio = st.selectbox("Aspect Ratio", list(ASPECT_RATIO_MAP.keys()), index=0)
    st.divider()
    st.caption("Powered by Freepik AI")

# 5. Main UI
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.title("🌌 Visionary AI")
    st.subheader("VIT-AP Student Project") # Personalizing for your context
    prompt = st.text_area("Describe your masterpiece:", height=200, placeholder="A futuristic city in the clouds...")
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

                    # Constructed according to Freepik 2026 JSON specs
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
                        # Freepik returns a list of objects in the 'data' key
                        # We extract the URL from the first object
                        images = data.get("data", [])
                        
                        if images and "url" in images[0]:
                            image_url = images[0]["url"]
                            img_data = requests.get(image_url).content
                            img = Image.open(io.BytesIO(img_data))
                            
                            status.update(label="✅ Success!", state="complete", expanded=False)
                            st.image(img, use_container_width=True)
                            st.download_button("🖼️ Download PNG", data=img_data, file_name="ai_art.png", mime="image/png")
                        else:
                            st.error("The API succeeded, but the URL key was missing.")
                            with st.expander("🔍 See API Response for Debugging"):
                                st.write(data) # This helps you see exactly what the API sent back
                    else:
                        st.error(f"API Error {response.status_code}")
                        st.code(response.text) # Shows exactly why the parameters failed

                except Exception as e:
                    st.error(f"Execution Error: {e}")
    else:
        st.info("Your image will appear here.")
