#ESSENTIAL LIBRARIES

# it helps us for making a simple web app
import streamlit as st
#it lets python download things from internet
import requests
#it lets python use my microphone to reccord sound
import sounddevice as sd
#this lets us to record sound as .wav file
#wav files are audio files and they store uncompresses sound
import wavio
#helps python to talk to os system
import os
#helps us to store openai key securely
from dotenv import load_dotenv
#imports openai client so we can use speech to text to image generation
# (OPENAI REMOVED – USING FREE OFFLINE MODEL)

from vosk import Model, KaldiRecognizer
import json
import wave
from PIL import Image, ImageDraw, ImageFont

load_dotenv()

#creates a instance of OpenAi which helps us in connecting us to openai
# (REMOVED – FREE VERSION DOES NOT USE OPENAI)

#defines function and parameters are name of ausdio file,duration of audio file,sound quality

#AUDIO RECORDING FUNCTION

def record_audio(filename, duration, fs):
    print("Recording.....")
    #this records sound from microphone 
    #duration*fs tells about total no of sound samples
    #samplerate=fs tells how clear sound is
    #channels=2 mixes left+right sound
    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )
    #tells python to wait until recording is finished
    sd.wait()
    #used to save the recorded sound into .wav file
    #sampwidth is for sound quality
    wavio.write(filename, recording, fs, sampwidth=2)
    print("Recording saved as", filename)

#STREAMLIT USER INTERFACE

st.set_page_config(page_title="Speech to Image", layout="centered")

st.title("🎤 Speech to Image (Offline & Free)")
st.caption("Speak → Convert to text → Generate image → Download")

st.sidebar.header("ℹ️ Instructions")
st.sidebar.write(
    """
    • Click the button and speak clearly  
    • Recording duration: **10 seconds**  
    • Works completely **offline**  
    • Output can be downloaded as **PNG or PDF**
    """
)

#used to display text in interface
st.write("Speak here")

#this creates a button and user clicks it inside block runs
if st.button(label="🎙️ Click here to speak"):
    with st.spinner("Listening for 10 seconds and generating image..."):
        #gives the name for audio file
        audio_filename = "input.wav"
        #sets how many seconds does microphone should record
        duration = 10
        #this is sound quality and and 44100 is good quality audio
        fs = 44100
        #calls the functioon we made earlier to record our voice
        record_audio(audio_filename, duration, fs)
        #this opens the audio file of our voice in read binary mode converts to text
        wf = wave.open("input.wav", "rb")

        model = Model("vosk-model")
        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)

        text_output = ""

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text_output += result.get("text", "") + " "

        final_result = json.loads(recognizer.FinalResult())
        text_output += final_result.get("text", "")

        #stores the spoken words as text in variable a
        a = " ".join(text_output.strip().split())
        #used to display a in interface
        st.success("Recognized Text:")
        st.markdown(f"**{a if a else 'No clear speech detected'}**")

        #GENERATING IMAGES FROM OPENAI

        #response sents a request to open ai to generate image
        #model tells openai which model to use and dall-e2 is for image generation
        #prompt this converts the text we spoke to become description of image
        #size decides image's dimensions
        #qualitu sets the image's quality
        #n=1 this is crucial tis asks to 1 image only

        image_path = "generated_image.png"
        pdf_path = "generated_image.pdf"

        img = Image.new("RGB", (1024, 1024), color="#f5f5f5")
        draw = ImageDraw.Draw(img)

        text = a if a else "Image Generated"

        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (1024 - text_width) // 2
        y = (1024 - text_height) // 2

        draw.text((x, y), text, fill="black", font=font)

        img.save(image_path)
        img.save(pdf_path, "PDF")

        #this one shows generate image on streamlit website
        st.image(image_path, caption="Generated Image")

        col1, col2 = st.columns(2)

        with col1:
            with open(image_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Image (PNG)",
                    data=f,
                    file_name="speech_image.png",
                    mime="image/png"
                )

        with col2:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Image (PDF)",
                    data=f,
                    file_name="speech_image.pdf",
                    mime="application/pdf"
                )
