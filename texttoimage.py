# ============================================================
# Visionary AI
# A simple, human-made interface for turning words into images
# ============================================================

# Core UI framework
import streamlit as st

# Talking to the outside world (APIs)
import requests

# Handling raw image bytes
import io
import base64

# Image handling
from PIL import Image


# ------------------------------------------------------------
# Page setup — first impression matters
# ------------------------------------------------------------
st.set_page_config(
    page_title="Visionary AI",
    page_icon="🌌",
    layout="wide"
)


# ------------------------------------------------------------
# Some light CSS to make Streamlit look less... Streamlit
# ------------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617 70%);
    color: #e5e7eb;
}

/* Headings */
h1, h2, h3 {
    font-weight: 700;
}

/* Text area readability */
textarea {
    font-size: 1.05rem !important;
    line-height: 1.6 !important;
}

/* Primary button */
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    height: 3rem;
    font-size: 1.05rem;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    opacity: 0.9;
}

/* Output frame */
.image-frame {
    border: 1px dashed #334155;
    border-radius: 16px;
    padding: 1rem;
    background-color: #020617;
    text-align: center;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Human-readable → API-readable mappings
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# API key check — fail early, fail clearly
# ------------------------------------------------------------
if "FREEPIK_API_KEY" not in st.secrets:
    st.error("🔑 FREEPIK_API_KEY is missing from Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["FREEPIK_API_KEY"]
API_URL = "https://api.freepik.com/v1/ai/text-to-image"


# ------------------------------------------------------------
# Sidebar — configuration lives here, not in the way
# ------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.caption("Adjust the vibe before generating")

    selected_style = st.selectbox(
        "Visual Style",
        list(STYLE_MAP.keys()),
        index=0
    )

    selected_ratio = st.selectbox(
        "Aspect Ratio",
        list(ASPECT_RATIO_MAP.keys()),
        index=0
    )

    st.markdown("---")
    st.caption("Powered by Freepik AI")


# ------------------------------------------------------------
# Main layout — input on the left, magic on the right
# ------------------------------------------------------------
left_col, right_col = st.columns([1, 1.3], gap="large")


# ---------------- LEFT: USER INPUT ----------------
with left_col:
    st.markdown("## 🌌 Visionary AI")
    st.markdown(
        "Describe what you see in your head. "
        "The clearer you are, the better the result."
    )

    prompt = st.text_area(
        "Describe your masterpiece",
        placeholder="A cyberpunk cat wearing headphones, neon city, cinematic lighting...",
        height=180
    )

    generate_btn = st.button(
        "🚀 Generate Masterpiece",
        use_container_width=True
    )


# ---------------- RIGHT: OUTPUT ----------------
with right_col:
    st.markdown("### 🖼️ Output")

    st.markdown('<div class="image-frame">', unsafe_allow_html=True)

    if generate_btn:
        # No prompt, no magic
        if not prompt.strip():
            st.warning("You need to type something first.")
        else:
            with st.spinner("🎨 Rendering your vision..."):
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

                    # Only send style if the user actually picked one
                    if STYLE_MAP[selected_style]:
                        payload["styling"] = {
                            "style": STYLE_MAP[selected_style]
                        }

                    response = requests.post(
                        API_URL,
                        headers=headers,
                        json=payload
                    )

                    if not response.ok:
                        st.error(f"API Error {response.status_code}")
                        st.json(response.json())
                    else:
                        data = response.json().get("data", [])

                        if not data:
                            st.error("The API returned no image.")
                        else:
                            # Handle both possible response formats
                            if "url" in data[0]:
                                img_bytes = requests.get(data[0]["url"]).content
                            else:
                                img_bytes = base64.b64decode(data[0]["base64"])

                            img = Image.open(io.BytesIO(img_bytes))

                            st.image(img, use_container_width=True)

                            st.download_button(
                                "⬇️ Download Image",
                                data=img_bytes,
                                file_name="visionary_ai.png",
                                mime="image/png",
                                use_container_width=True
                            )

                except Exception as e:
                    st.error(f"Unexpected error: {e}")
    else:
        st.info("Your generated image will appear here.")

    st.markdown("</div>", unsafe_allow_html=True)
