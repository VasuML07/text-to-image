import streamlit as st
import requests
import io
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Visionary AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3em;
        background-color: #FF4B4B; color: white; font-weight: bold; border: none;
    }
    .stTextArea>div>div>textarea { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. API Configuration & Mappings
# Freepik expects specific 'slug' names for these parameters
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

# Ensure your key is in .streamlit/secrets.toml as: FREEPIK_API_KEY = "your_key"
if "FREEPIK_API_KEY" in st.secrets:
    API_KEY = st.secrets["FREEPIK_API_KEY"]
else:
    st.error("🔑 API Key not found! Add 'FREEPIK_API_KEY' to your Streamlit secrets.")
    st.stop()

# Using the Freepik "Classic Fast" endpoint for immediate results
API_URL = "https://api.freepik.com/v1/ai/text-to-image"

# 4. Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    st.info("Powered by Freepik AI")
    
    selected_style_name = st.selectbox("Artistic Style", list(STYLE_MAP.keys()), index=1)
    selected_ratio_name = st.selectbox("Aspect Ratio", list(ASPECT_RATIO_MAP.keys()), index=0)
    
    st.divider()
    st.caption("Credits are deducted per generation.")

# 5. Main UI Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.title("🌌 Visionary AI")
    st.subheader("Transform thoughts into art.")
    prompt = st.text_area("Describe your masterpiece:", height=200, placeholder="A futuristic city...")
    generate_btn = st.button("🚀 Generate Masterpiece")

with col2:
    if generate_btn:
        if not prompt.strip():
            st.error("Please enter a description.")
        else:
            with st.status("🎨 Rendering your vision...", expanded=True) as status:
                try:
                    # Authentication Headers
                    headers = {
                        "Content-Type": "application/json",
                        "x-freepik-api-key": API_KEY
                    }

                    # JSON Payload Construction
                    payload = {
                        "prompt": prompt.strip(),
                        "image": {
                            "size": ASPECT_RATIO_MAP[selected_ratio_name]
                        }
                    }
                    
                    api_style = STYLE_MAP[selected_style_name]
                    if api_style:
                        payload["styling"] = {"style": api_style}

                    # Make the POST request
                    response = requests.post(API_URL, headers=headers, json=payload)

                    if response.ok:
                        data = response.json()
                        # Extract the image URL from the 'data' list
                        image_url = data.get("data", [{}])[0].get("url")
                        
                        if image_url:
                            # Fetch image bytes from the URL
                            img_response = requests.get(image_url)
                            image_bytes = img_response.content
                            img = Image.open(io.BytesIO(image_bytes))
                            
                            status.update(label="✅ Image Generated!", state="complete", expanded=False)
                            st.image(img, use_container_width=True)
                            
                            # Download Actions
                            btn_col1, btn_col2 = st.columns(2)
                            with btn_col1:
                                st.download_button("🖼️ Download PNG", data=image_bytes, file_name="vision_art.png", mime="image/png")
                            with btn_col2:
                                pdf_buffer = io.BytesIO()
                                img.convert("RGB").save(pdf_buffer, format="PDF")
                                st.download_button("📄 Download PDF", data=pdf_buffer.getvalue(), file_name="vision_art.pdf", mime="application/pdf")
                        else:
                            st.error("API success, but no image URL was found.")
                    else:
                        st.error(f"API Error {response.status_code}: {response.text}")

                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
    else:
        st.info("Your masterpiece will appear here.")
