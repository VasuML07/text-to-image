📝 Text to Image Generator

A simple Streamlit web application that converts user-entered text into an image and allows downloading the result as a PNG or PDF.

The project is lightweight, runs offline, and requires no external APIs or paid services.

🚀 Features

✍️ Text input (up to 400 characters)

🖼️ Generate an image from text

📥 Download output as PNG or PDF

⚡ Fast and lightweight

🌐 Interactive Streamlit UI

☁️ Fully deployable on Streamlit Cloud

🧠 How It Works

User enters text in the input box

The text is rendered onto a fixed-size image canvas

The generated image is displayed instantly

The user can download the image as PNG or PDF

The image is created locally using Python libraries without any external services.

🛠️ Tech Stack

Python

Streamlit – Web interface

Pillow (PIL) – Image creation and rendering

📁 Project Structure
text-to-image/
├── speechtoimage.py
├── requirements.txt
├── README.md
└── .gitignore

▶️ Run Locally
1️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
streamlit run speechtoimage.py


Open in browser:

http://localhost:8501

☁️ Deployment (Streamlit Cloud)

This application is compatible with Streamlit Cloud.

Steps:

Push this repository to GitHub

Visit https://share.streamlit.io

Click New App

Select:

Repository

Branch: main

File path: speechtoimage.py

Click Deploy

🎯 Use Cases

College mini project

Python + Streamlit practice

Text visualization demo

Portfolio project

UI prototyping

⚠️ Notes

Maximum input length is limited to 400 characters

Generated files are excluded from version control via .gitignore

This project focuses on text rendering, not AI image generation

📌 Future Enhancements

Text wrapping for long inputs

Custom font selection

Background color themes

Image export formats

Batch image generation

👨‍💻 Author

Developed as a simple, clean, and deployable Streamlit application.

✅ Summary

This project demonstrates:

Clean UI design

Proper file handling

Streamlit deployment readiness

Responsible project scoping
