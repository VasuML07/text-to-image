# 🎤 Speech to Image (Offline & Free)

This project converts spoken audio into text using an offline
speech recognition model (Vosk) and generates an image or PDF
based on the recognized speech.

The application is built using Streamlit and runs fully offline.

---

## 🚀 Features
- Voice input (10 seconds)
- Offline speech-to-text (Vosk)
- Image generation from speech text
- Download output as PNG or PDF
- Clean Streamlit UI

---

## 🧠 Tech Stack
- Streamlit
- SoundDevice & Wavio
- Vosk (offline speech recognition)
- Pillow (image creation)
- Python

---

## ▶️ How to Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run speechtoimage.py

## 📁 Project Structure
PRO/
├── speechtoimage.py
├── requirements.txt
├── .gitignore
├── venv/
└── vosk-model/