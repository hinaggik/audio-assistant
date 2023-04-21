import os
import openai
import tempfile
import sounddevice as sd
import numpy as np
import webrtcvad
import io
import tkinter as tk
import matplotlib.pyplot as plt
import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech_v1 as texttospeech
from google.oauth2 import service_account
from pydub import AudioSegment
from pydub.playback import play
from audio_utils import transcribe_audio, generate_text, record_audio, play_audio
from meter_utils import update_audio_meter, update_plot

# Set up your API keys
openai.api_key = os.environ.get("OPENAI_API_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PATH")


# Set up Google Cloud clients
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Set up sounddevice for recording
duration = 10  # Record for 10 seconds
rate = 16000

# Set up webrtcvad for voice activity detection
vad = webrtcvad.Vad(3)


def text_to_speech(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    tts_response = tts_client.synthesize_speech(input=input_text, voice=voice_params, audio_config=audio_config)
    return tts_response.audio_content


# Start the conversation
generated_text = "Hello! How can I help you today?"
print("Assistant:", generated_text)
audio_content = text_to_speech(generated_text)
play_audio(audio_content)

conversation_history = "Assistant: Hello! How can I help you today?"

# Create the GUI
root = tk.Tk()
root.title("Audio Assistant")

figure = plt.Figure(figsize=(5, 1), dpi=100)
ax = figure.add_subplot(111)
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().pack()

initial_data = np.random.rand(1, 20)
update_plot(ax, initial_data)

while True:
    frames = record_audio(ax, duration, rate)
    transcribed_text = transcribe_audio(frames, rate)
    print("You:", transcribed_text)

    if "quit" in transcribed_text.lower():
        generated_text = "Goodbye! Have a great day!"
        print("Assistant:", generated_text)
        audio_content = text_to_speech(generated_text)
        play_audio(audio_content)
        break

    if not transcribed_text.strip():
        transcribed_text = "I don't have anything to say."

    conversation_history += f"\nUser: {transcribed_text}"
    generated_text = generate_text(conversation_history, transcribed_text)
    conversation_history += f"\nAssistant: {generated_text}"

    print("Assistant:", generated_text)
    audio_content = text_to_speech(generated_text)
    play_audio(audio_content)
    update_plot(ax, np.random.rand(1, 20))

root.mainloop()
