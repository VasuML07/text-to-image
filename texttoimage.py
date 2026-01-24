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
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextArea>div>div>textarea {
        border-radius: 10px;
    }
    .generated-image {
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

API_KEY = st.secrets["CLIPDROP_API_KEY"]
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
    st.caption("Credits are deducted per generation. Use prompts wisely.")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.title("🌌 Visionary AI")
    st.subheader("Transform your thoughts into high-resolution art.")
    
    prompt = st.text_area(
        "Describe your masterpiece:",
        placeholder="A futuristic laboratory in VIT-AP university, holographic screens, cinematic lighting, 8k resolution...",
        height=200
    )
    
    generate_btn = st.button("🚀 Generate Masterpiece")

with col2:
    if generate_btn:
        if not prompt.strip():
            st.error("Please enter a description to visualize.")
        else:
            with st.status("🎨 Rendering your vision...", expanded=True) as status:
                try:
                    payload = {"prompt": (None, prompt.strip())}
                    if style_preset != "None":
                        payload["style_preset"] = (None, style_preset.lower().replace(" ", "-"))

                    response = requests.post(
                        API_URL,
                        headers={"x-api-key": API_KEY},
                        files=payload
                    )

                    if response.ok:
                        image_bytes = response.content
                        img = Image.open(io.BytesIO(image_bytes))
                        
                        status.update(label="✅ Image Generated!", state="complete", expanded=False)
                        
                        st.image(img, use_container_width=True, caption=f"Style: {style_preset}")
                        
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            st.download_button(
                                label="🖼️ Download PNG",
                                data=image_bytes,
                                file_name="visionary_art.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        with btn_col2:
                            pdf_buffer = io.BytesIO()
                            img.convert("RGB").save(pdf_buffer, format="PDF")
                            st.download_button(
                                label="📄 Download PDF",
                                data=pdf_buffer.getvalue(),
                                file_name="visionary_art.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                    else:
                        status.update(label="❌ Generation Failed", state="error")
                        st.error(f"API Error {response.status_code}: {response.text}")

                except Exception as e:
                    status.update(label="❌ Unexpected Error", state="error")
                    st.error(f"Error: {e}")
    else:
        st.info("Your generated image will appear here.")
        st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop", use_container_width=True)
