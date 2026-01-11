#ESSENTIAL LIBRARIES

# it helps us for making a simple web app
import streamlit as st
#it lets python download things from internet
import requests
#helps python to talk to os system
import os
#image creation utilities
from PIL import Image, ImageDraw, ImageFont



#STREAMLIT USER INTERFACE

st.set_page_config(page_title="Text to Image", layout="centered")

st.title("📝 Text to Image (Offline & Free)")
st.caption("Enter text → Generate image → Download as PNG or PDF")

st.sidebar.header("ℹ️ Instructions")
st.sidebar.write(
    """
    • Enter a description (max **400 characters**)  
    • Image is generated locally  
    • Works **offline**  
    • Download as **PNG or PDF**
    """
)

#TEXT INPUT
text_input = st.text_area(
    "Enter text (max 400 characters):",
    max_chars=400,
    height=150,
    placeholder="Example: A dog playing football in a green park"
)

#BUTTON
if st.button("🎨 Generate Image"):
    with st.spinner("Generating image..."):

        #ensure text fallback
        text = text_input.strip() if text_input.strip() else "Image Generated"

        #paths
        image_path = "generated_image.png"
        pdf_path = "generated_image.pdf"

        #create image
        img = Image.new("RGB", (1024, 1024), color="#f5f5f5")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

        #center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (1024 - text_width) // 2
        y = (1024 - text_height) // 2

        draw.text((x, y), text, fill="black", font=font)

        #save files
        img.save(image_path)
        img.save(pdf_path, "PDF")

        #display image
        st.image(image_path, caption="Generated Image")

        #download buttons
        col1, col2 = st.columns(2)

        with col1:
            with open(image_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Image (PNG)",
                    data=f,
                    file_name="text_image.png",
                    mime="image/png"
                )

        with col2:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Image (PDF)",
                    data=f,
                    file_name="text_image.pdf",
                    mime="application/pdf"
                )

