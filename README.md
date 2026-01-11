📝 Text to Image Generator (Offline & Deployable)

A Streamlit web application that converts user-entered text into a structured image, with options to download the output as PNG or PDF.

Unlike popular AI tools such as ChatGPT or Gemini, this project is designed to be fully offline, transparent, and reproducible, making it ideal for learning, deployment, and academic use.

🚀 What This Project Provides (Beyond AI Chat Tools)

While tools like ChatGPT and Gemini rely on cloud-based AI models and APIs, this project focuses on control, simplicity, and deployability.

It provides:

✅ Offline execution (no internet required after setup)

✅ No API keys, no usage limits

✅ Full control over output files

✅ Direct PNG & PDF downloads

✅ Deployable Streamlit web application

✅ Transparent and explainable processing pipeline

This makes the project especially suitable for education, demos, restricted environments, and academic evaluation.

🚀 Features

✍️ Text input up to 1500 characters

📄 Automatic line-by-line rendering (max 100 characters per line)

🖼️ Convert text into a clean, readable image

📥 Download output as PNG or PDF

⚡ Fast and lightweight

🌐 Interactive Streamlit UI

☁️ Fully deployable on Streamlit Cloud

🔒 No external APIs or paid services

🧠 How It Works

User enters text (up to 1500 characters)

Text is automatically split into readable lines

Each line is rendered onto a fixed-size image canvas

The generated image is displayed instantly

User can download the output as PNG or PDF

All processing happens locally using Python libraries, ensuring predictable and reproducible results.

🆚 Comparison with AI Models (ChatGPT, Gemini)
Feature	This Project	ChatGPT / Gemini
Offline usage	✅ Yes	❌ No
API key required	❌ No	✅ Yes
Usage limits	❌ No	✅ Yes
Direct image/PDF download	✅ Yes	❌ Limited
Deployable as web app	✅ Yes	❌ No
Full code control	✅ Yes	❌ No
Reproducible output	✅ Yes	❌ No

This project does not replace AI models — it complements them by focusing on controlled text visualization and deployment, rather than AI-generated imagery.

🛠️ Tech Stack

Python

Streamlit – Web interface

Pillow (PIL) – Image creation and text rendering

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

Maximum input length is limited to 1500 characters

Each rendered line contains a maximum of 100 characters

Generated files are excluded using .gitignore

This project focuses on text visualization, not AI image generation

📌 Future Enhancements

Dynamic font size scaling

Custom font selection

Background color and theme options

Batch image generation

Optional local AI image models (e.g., Stable Diffusion)

👨‍💻 Author

Developed as a lightweight, offline, and deployable alternative to cloud-dependent AI tools.

✅ Summary

This project demonstrates:

Practical software engineering

Offline-first design

Clean UI and file handling

Deployment-ready Streamlit applications

Clear differentiation from cloud-based AI models
