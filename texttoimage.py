# ============================================================
# Visionary AI — Stable UI Edition
# Buttons stay. Layout stays. Sanity stays.
# ============================================================

import streamlit as st
import requests
import io
import base64
from PIL import Image


# ------------------------------------------------------------
# Page config
# ------------------------------------------------------------
st.set_page_config(
    page_title="Visionary AI",
    page_icon="🌌",
    layout="wide"
)


# ------------------------------------------------------------
# Minimal but effective styling
# ------------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617 70%);
    color: #e5e7eb;
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    height: 3.2rem;
    font-size: 1.05rem;
    font-weight: 600;
    border: none;
}

/* Output frame (always visible) */
.output-frame {
    border: 1px dashed #334155;
    border-radius: 18px;
    padding: 1.2rem;
    background-color: #020617;
    min-height: 420px;   /* THIS is the key: layout stability */
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Mappings (human → API)
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
# API key guardrail
# ------------------------------------------------------------
if "FREEPIK_API_KEY" not in st.secrets:
    st.error("FREEPIK_API_KEY missing in secrets.")
    st.stop()

API_KEY = st.secrets["FREEPIK_API_KEY"]
API_URL = "https://api.freepik.com/v1/ai/text-to-image"


# ------------------------------------------------------------
# Sidebar controls (static, never move)
# ------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    selected_style = st.selectbox(
        "Visual Style",
        list(STYLE_MAP.keys())
    )

    selected_ratio = st.selectbox(
        "Aspect Ratio",
        list(ASPECT_RATIO_MAP.keys())
    )

    st.markdown("---")
    st.caption("Freepik AI backend")


# ------------------------------------------------------------
# Main layout — locked zones
# ------------------------------------------------------------
left, right = st.columns([1, 1.3], gap="large")


# ================= LEFT PANEL =================
with left:
    st.markdown("## 🌌 Visionary AI")
    st.markdown(
        "Describe what you see in your head. "
        "Clear prompts = better images."
    )

    prompt = st.text_area(
        "Describe your masterpiece",
        height=180,
        placeholder="A cyberpunk cat wearing headphones, neon city, cinematic lighting..."
    )

    # Button ALWAYS stays here
    generate_btn = st.button(
        "🚀 Generate Masterpiece",
        use_container_width=True
    )


# ================= RIGHT PANEL =================
with right:
    st.markdown("### 🖼️ Output")

    # Permanent output container (no jumping)
    output_container = st.container()

    with output_container:
        st.markdown('<div class="output-frame">', unsafe_allow_html=True)

        image_placeholder = st.empty()
        download_placeholder = st.empty()
        message_placeholder = st.empty()

        # Default state
        message_placeholder.info("Your generated image will appear here.")

        # Generation logic
        if generate_btn:
            if not prompt.strip():
                message_placeholder.warning("Please enter a description.")
            else:
                message_placeholder.empty()
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
                            message_placeholder.error(
                                f"API Error {response.status_code}"
                            )
                        else:
                            data = response.json().get("data", [])
                            if not data:
                                message_placeholder.error(
                                    "No image returned by API."
                                )
                            else:
                                if "url" in data[0]:
                                    img_bytes = requests.get(
                                        data[0]["url"]
                                    ).content
                                else:
                                    img_bytes = base64.b64decode(
                                        data[0]["base64"]
                                    )

                                img = Image.open(
                                    io.BytesIO(img_bytes)
                                )

                                image_placeholder.image(
                                    img,
                                    use_container_width=True
                                )

                                download_placeholder.download_button(
                                    "⬇️ Download Image",
                                    img_bytes,
                                    "visionary_ai.png",
                                    "image/png",
                                    use_container_width=True
                                )

                    except Exception as e:
                        message_placeholder.error(f"System error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)
