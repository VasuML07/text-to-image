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

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3em;
        background-color: #FF4B4B; color: white; font-weight: bold; border: none;
    }
    .stTextArea>div>div>textarea { border-radius: 10px; }
    .generated-image { border-radius: 15px; box-shadow: 0px 4px 20px rgba(0,0,0,0.5); }
    </style>
    """, unsafe_allow_html=True)

# SAFE API KEY RETRIEVAL
if "CLIPDROP_API_KEY" in st.secrets:
    API_KEY = st.secrets["CLIPDROP_API_KEY"]
else:
    st.error("🔑 API Key not found! Please add 'CLIPDROP_API_KEY' to your Streamlit secrets.")
    st.stop() # Stops execution so the app doesn't crash later

API_URL = "https://clipdrop-api.co/text-to-image/v1"

with st.sidebar:
    st.title("⚙️ Configuration")
    st.info("Powered by Stability AI")
    style_preset = st.selectbox(
        "Artistic Style",
        ["None", "Photographic", "Digital Art", "Comic Book", "Fantasy Art", "Neonpunk", "Cinematic"],
        index=1
    )
    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        ["1:1 (Square)", "16:9 (Widescreen)", "4:3 (Standard)", "2:3 (Portrait)"],
        index=0
    )
    st.divider()
    st.caption("Credits are deducted per generation.")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.title("🌌 Visionary AI")
    st.subheader("Transform thoughts into art.")
    prompt = st.text_area("Describe your masterpiece:", height=200)
    generate_btn = st.button("🚀 Generate Masterpiece")

with col2:
    if generate_btn:
        if not prompt.strip():
            st.error("Please enter a description.")
        else:
            with st.status("🎨 Rendering your vision...", expanded=True) as status:
                try:
                    payload = {"prompt": (None, prompt.strip())}
                    if style_preset != "None":
                        payload["style_preset"] = (None, style_preset.lower().replace(" ", "-"))

                    response = requests.post(API_URL, headers={"x-api-key": API_KEY}, files=payload)

                    if response.ok:
                        image_bytes = response.content
                        img = Image.open(io.BytesIO(image_bytes))
                        status.update(label="✅ Image Generated!", state="complete", expanded=False)
                        st.image(img, use_container_width=True)
                        
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            st.download_button("🖼️ Download PNG", data=image_bytes, file_name="art.png", mime="image/png")
                        with btn_col2:
                            pdf_buffer = io.BytesIO()
                            img.convert("RGB").save(pdf_buffer, format="PDF")
                            st.download_button("📄 Download PDF", data=pdf_buffer.getvalue(), file_name="art.pdf", mime="application/pdf")
                    else:
                        st.error(f"API Error {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Your image will appear here.")
