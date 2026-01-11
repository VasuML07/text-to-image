📝 Text to Image Generator (Offline & Deployable)

A Streamlit web application that converts user-entered text into an image and allows downloading the result as a PNG or PDF.

Unlike popular AI tools such as ChatGPT or Gemini, this project is designed to be fully offline, transparent, and reproducible, making it ideal for learning, deployment, and academic use.

🚀 What This Project Provides (Beyond AI Chat Tools)

While tools like ChatGPT and Gemini focus on AI-generated content via cloud APIs, this project offers:

✅ Offline execution (no internet required)

✅ No API keys, no usage limits

✅ Full control over output files

✅ Direct image & PDF downloads

✅ Deployable Streamlit web app

✅ Transparent and explainable pipeline

This makes the project especially suitable for education, demos, and environments where cloud AI tools are restricted.

🚀 Features

✍️ Text input (up to 400 characters)

🖼️ Convert text into a visual image

📥 Download output as PNG or PDF

⚡ Fast and lightweight

🌐 Interactive Streamlit UI

☁️ Fully deployable on Streamlit Cloud

🔒 No external APIs or paid services

🧠 How It Works

User enters text in the input box

The text is rendered onto a fixed-size image canvas

The generated image is displayed instantly

The user can download the result as a PNG or PDF

The image is created locally using Python libraries, ensuring predictability and reproducibility.

🆚 Comparison with AI Models (ChatGPT, Gemini)
Feature	This Project	ChatGPT / Gemini
Offline usage	✅ Yes	❌ No
API key required	❌ No	✅ Yes
Direct image/PDF download	✅ Yes	❌ Limited
Deployable as web app	✅ Yes	❌ No
Full code control	✅ Yes	❌ No
Reproducible output	✅ Yes	❌ No

This project does not replace AI models — it complements them by focusing on control, simplicity, and deployment.

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

This application is fully compatible with Streamlit Cloud.

Steps:

Push the repository to GitHub

Visit https://share.streamlit.io

Click New App

Select:

Repository

Branch: main

File path: speechtoimage.py

Click Deploy

🎯 Use Cases

College mini or major project

Python + Streamlit learning

Text visualization tools

Portfolio demonstration

UI and deployment practice

⚠️ Notes

Maximum input length is limited to 400 characters

Generated files are excluded via .gitignore

This project focuses on text visualization, not AI-generated imagery

📌 Future Enhancements

Text wrapping for long inputs

Custom fonts and themes

Background customization

Batch image generation

Optional local AI image models (e.g., Stable Diffusion)

👨‍💻 Author

Developed as a lightweight, offline, and deployable alternative to cloud-dependent AI tools.

✅ Summary

This project demonstrates:

Practical software engineering

Responsible project scoping

Offline-first design

Deployment-ready Streamlit apps

Clear differentiation from cloud AI models
