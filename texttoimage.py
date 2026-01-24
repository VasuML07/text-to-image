import streamlit as st
import requests
import io
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Visionary AI", page_icon="🌌", layout="wide")

# 2. 2026 Verified API Slugs
# Slugs are strictly validated by Freepik's backend
STYLE_MAP = {
    "None": None,
    "Realism": "realism",
    "Flexible (Stylized)": "flexible",
    "Fluid (Creative)": "fluid",
    "Zen (Minimal)": "zen",
    "Cyberpunk": "cyberpunk",
    "Fantasy": "fantasy"
}

ASPECT_RATIO_MAP = {
    "1:1 (Square)": "square_1_1",
    "16:9 (Widescreen)": "widescreen_16_9",
    "4:3 (Classic)": "classic_4_3",
    "2:3 (Portrait)": "portrait_2_3"
}

# Ensure your key is in .streamlit/secrets.toml
if "FREEPIK_API_KEY" in st.secrets:
    API_KEY = st.secrets["FREEPIK_API_KEY"]
else:
    st.error("🔑 API Key 'FREEPIK_API_KEY' not found in Secrets!")
    st.stop()

# Use the latest text-to-image base endpoint
API_URL = "https://api.freepik.com/v1/ai/text-to-image"

# 3. Sidebar UI
with st.sidebar:
    st.title("⚙️ Configuration")
    selected_style = st.selectbox("Artistic Style", list(STYLE_MAP.keys()), index=0)
    selected_ratio = st.selectbox("Aspect Ratio", list(ASPECT_RATIO_MAP.keys()), index=0)
    st.divider()
    st.caption("Powered by Freepik AI")

# 4. Main UI
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.title("🌌 Visionary AI")
    prompt = st.text_area("Describe your masterpiece:", height=200, placeholder="A futuristic city...")
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
                        "Accept": "application/json",
                        "x-freepik-api-key": API_KEY
                    }

                    # Payload structure for Freepik v1
                    payload = {
                        "prompt": prompt.strip(),
                        "image": {
                            "size": ASPECT_RATIO_MAP[selected_ratio]
                        },
                        "num_images": 1
                    }
                    
                    # Add style slug only if a specific style is selected
                    if STYLE_MAP[selected_style]:
                        payload["styling"] = {"style": STYLE_MAP[selected_style]}

                    response = requests.post(API_URL, headers=headers, json=payload)

                    if response.ok:
                        res_data = response.json()
                        # Freepik 2026 Response: data is a list of objects containing 'url'
                        images_list = res_data.get("data", [])
                        
                        if images_list and "url" in images_list[0]:
                            image_url = images_list[0]["url"]
                            
                            # Step 2: Download image from the generated URL
                            img_response = requests.get(image_url)
                            img_bytes = img_response.content
                            img = Image.open(io.BytesIO(img_bytes))
                            
                            status.update(label="✅ Generation Complete!", state="complete", expanded=False)
                            st.image(img, use_container_width=True)
                            
                            # Download Logic
                            st.download_button("🖼️ Download PNG", data=img_bytes, file_name="ai_art.png", mime="image/png")
                        else:
                            st.error("Success, but no image URL was found in response.")
                            st.json(res_data) # Debugger to see the actual returned structure
                    else:
                        st.error(f"❌ Error {response.status_code}")
                        st.code(response.text) # Reveals why parameters didn't validate

                except Exception as e:
                    st.error(f"Execution Error: {e}")
    else:
        st.info("Your image will appear here.")
