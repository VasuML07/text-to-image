import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(
    page_title="Visionary AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
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

# --- SAFE API KEY RETRIEVAL ---
if "FREEPIK_API_KEY" in st.secrets:
    API_KEY = st.secrets["FREEPIK_API_KEY"]
else:
    st.error("🔑 Freepik API Key not found! Please add 'FREEPIK_API_KEY' to your Streamlit secrets.")
    st.stop()

# Freepik Text-to-Image Endpoint
API_URL = "https://api.freepik.com/v1/ai/text-to-image"

with st.sidebar:
    st.title("⚙️ Configuration")
    st.info("Powered by Freepik AI")
    
    # Mapping friendly names to Freepik-compatible slugs
    style_preset = st.selectbox(
        "Artistic Style",
        ["None", "Photographic", "Digital Art", "Comic Book", "Fantasy Art", "Cyberpunk", "Cinematic"],
        index=1
    )
    
    # Freepik uses specific keywords for aspect ratios
    aspect_ratio_map = {
        "1:1 (Square)": "square",
        "16:9 (Widescreen)": "landscape",
        "4:3 (Standard)": "standard",
        "2:3 (Portrait)": "portrait"
    }
    
    selected_ratio = st.selectbox("Aspect Ratio", list(aspect_ratio_map.keys()), index=0)
    st.divider()
    st.caption("Each generation uses Freepik API credits.")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.title("🌌 Visionary AI")
    st.subheader("Transform thoughts into art.")
    prompt = st.text_area("Describe your masterpiece:", height=200, placeholder="A futuristic city in the style of Van Gogh...")
    generate_btn = st.button("🚀 Generate Masterpiece")

with col2:
    if generate_btn:
        if not prompt.strip():
            st.error("Please enter a description.")
        else:
            with st.status("🎨 Rendering your vision...", expanded=True) as status:
                try:
                    # Headers for Freepik
                    headers = {
                        "Content-Type": "application/json",
                        "x-freepik-api-key": API_KEY
                    }

                    # JSON Body (Freepik expects JSON, not multipart/form-data)
                    payload = {
                        "prompt": prompt.strip(),
                        "image": {
                            "size": aspect_ratio_map[selected_ratio]
                        }
                    }
                    
                    if style_preset != "None":
                        payload["styling"] = {"style": style_preset.lower().replace(" ", "-")}

                    response = requests.post(API_URL, headers=headers, json=payload)

                    if response.ok:
                        # Freepik returns a JSON with an image URL or base64
                        data = response.json()
                        # Adjusting based on Freepik's response structure
                        image_url = data.get("data", [{}])[0].get("url")
                        
                        if image_url:
                            img_response = requests.get(image_url)
                            image_bytes = img_response.content
                            img = Image.open(io.BytesIO(image_bytes))
                            
                            status.update(label="✅ Image Generated!", state="complete", expanded=False)
                            st.image(img, use_container_width=True)
                            
                            # Download Actions
                            btn_col1, btn_col2 = st.columns(2)
                            with btn_col1:
                                st.download_button("🖼️ Download PNG", data=image_bytes, file_name="freepik_art.png", mime="image/png")
                            with btn_col2:
                                pdf_buffer = io.BytesIO()
                                img.convert("RGB").save(pdf_buffer, format="PDF")
                                st.download_button("📄 Download PDF", data=pdf_buffer.getvalue(), file_name="freepik_art.pdf", mime="application/pdf")
                        else:
                            st.error("Could not retrieve image URL from Freepik.")
                    else:
                        st.error(f"API Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Your image will appear here.")
