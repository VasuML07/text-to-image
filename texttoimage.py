#ESSENTIAL LIBRARIES

# it helps us for making a simple web app
import streamlit as st
#it lets python download things from internet
import requests
#helps python to talk to os system
import os
#image creation utilities
from PIL import Image, ImageDraw, ImageFont
import textwrap



#STREAMLIT USER INTERFACE

st.set_page_config(page_title="Text to Image", layout="centered")

st.title("📝 Text to Image (Offline & Free)")
st.caption("Enter text → Generate image → Download as PNG or PDF")

st.sidebar.header("ℹ️ Instructions")
st.sidebar.write(
    """
    • Enter a description (max **1000 characters**)  
    • Each line will contain **max 100 characters**  
    • Image is generated locally  
    • Works **offline**  
    • Download as **PNG or PDF**
    """
)

#TEXT INPUT
text_input = st.text_area(
    "Enter text (max 1000 characters):",
    max_chars=1000,
    height=200,
    placeholder="Example: A dog playing football in a green park..."
)

#BUTTON
if st.button("🎨 Generate Image"):
    with st.spinner("Generating image..."):

        #ensure text fallback
        text = text_input.strip() if text_input.strip() else "Image Generated"

        #wrap text into lines of max 100 chars
        wrapped_lines = textwrap.wrap(text, width=100)

        #paths
        image_path = "generated_image.png"
        pdf_path = "generated_image.pdf"

        #create image
        img = Image.new("RGB", (1024, 1024), color="#f5f5f5")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()

        #calculate total text height
        line_height = font.getbbox("A")[3] + 10
        total_text_height = line_height * len(wrapped_lines)

        #starting Y to vertically center text block
        y_start = (1024 - total_text_height) // 2

        #draw each line centered
        for line in wrapped_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (1024 - text_width) // 2

            draw.text((x, y_start), line, fill="black", font=font)
            y_start += line_height

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
