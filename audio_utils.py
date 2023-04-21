import tempfile
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
from google.cloud import speech_v1p1beta1 as speech
import webrtcvad
from meter_utils import update_audio_meter

speech_client = speech.SpeechClient()

# Set up webrtcvad for voice activity detection
vad = webrtcvad.Vad(3)

def record_audio(ax, duration, rate):
    print("Recording...")

    def callback(indata, outdata, frames, time, status):
        update_audio_meter(ax, indata, frames, time, status)
        audio_data.extend(indata.tobytes())
        buffer = audio_data[-480 * 2:]  # Keep 30ms of audio data (480 samples at 16-bit)
        if len(buffer) == 480 * 2 and vad.is_speech(buffer, rate):
            sd.stop()

    audio_data = bytearray()
    with sd.Stream(samplerate=rate, channels=1, dtype='int16', callback=callback):
        sd.sleep(duration * 1000)

    print("Finished recording.")
    return bytes(audio_data)  # Convert bytearray to bytes before returning


def transcribe_audio(audio_data, rate):
    speech_client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=rate,
        language_code="en-US",
    )
    audio = speech.RecognitionAudio(content=audio_data)

    print(f"Audio data length: {len(audio_data)}")

    response = speech_client.recognize(config=config, audio=audio)

    if response.results:
        transcribed_text = response.results[0].alternatives[0].transcript
    else:
        transcribed_text = ""

    return transcribed_text
    
def generate_text(conversation_history, transcribed_text):
    prompt = f"{conversation_history}\nUser: {transcribed_text}\nAssistant:"
    openai_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,  # Adjust temperature for more meaningful responses
    )
    return openai_response.choices[0].text.strip()

def play_audio(audio_content):
    with tempfile.NamedTemporaryFile(delete=True) as f:
        f.write(audio_content)
        f.seek(0)
        audio_segment = AudioSegment.from_mp3(f.name)
        play(audio_segment)