📝 Text to Image Generator (Offline & Free)

A simple and interactive Streamlit web application that converts user-provided text into an image, with options to download the output as PNG or PDF.

This project is designed to be fully offline, API-free, and easy to deploy, making it ideal for learning, demos, and academic submissions.

🚀 Features

✍️ Text input up to 400 characters

🖼️ Generates an image from the entered text

📄 Download output as PNG or PDF

⚡ Fast and lightweight

🌐 Streamlit-based interactive UI

🔒 No API keys, no paid services

☁️ Compatible with Streamlit Cloud

🧠 How It Works

User enters descriptive text (up to 400 characters)

The app renders the text onto an image canvas using Pillow

The generated image is displayed instantly

The user can download the result as:

PNG image

PDF document

This approach avoids external dependencies and ensures reproducibility.

🛠️ Tech Stack

Python

Streamlit – Web interface

Pillow (PIL) – Image generation

python-dotenv – Environment handling

Requests – Utility support

📁 Project Structure
speech-to-image/
├── speechtoimage.py
├── requirements.txt
├── README.md
└── .gitignore


Generated files (images, PDFs) and virtual environments are excluded using .gitignore.

▶️ Run Locally
1️⃣ Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the app
streamlit run speechtoimage.py


Open your browser at:

http://localhost:8501

☁️ Deployment (Streamlit Cloud)

This project is fully deployable on Streamlit Cloud.

Steps:

Push this repository to GitHub

Go to https://share.streamlit.io

Click New App

Select:

Repository: speech-to-image

Branch: main

File: speechtoimage.py

Click Deploy

🎓 Use Cases

College mini / major project

Streamlit learning project

UI + image processing demo

Offline alternative to API-based tools

Portfolio project

⚠️ Notes

This project intentionally avoids speech input and cloud APIs to remain deployable.

A speech-to-text version (using Vosk) can be run locally but is not suitable for cloud deployment due to microphone restrictions.

For real AI-generated images, local Stable Diffusion can be integrated separately.

📌 Future Enhancements

Text wrapping for long inputs

Custom fonts and colors

Background themes (dark/light)

Image gallery / history

Local Stable Diffusion integration

👨‍💻 Author

Built as a learning-focused, cost-free alternative to API-based text-to-image tools.
