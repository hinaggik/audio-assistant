# Audio Assistant

A voice-controlled AI assistant using OpenAI and Google Cloud Services.

## Known Issues

This project is a work-in-progress, and there may be issues with the current implementation. Any contributions or feedback to help improve the project are welcome.

- Issue 1: Error with matplotlib updating the audio meter in real-time. This issue causes a traceback error, which stops the program from functioning correctly.
- Issue 2: The conversation loop may not work as intended due to issues with the audio recording and transcription.

## Setup

1. Clone this repository.
2. Install the required dependencies using `pip`:

pip install -r requirements.txt

3. Set the following environment variables with your API keys and credentials:
   - `OPENAI_API_KEY`
   - `GOOGLE_APPLICATION_CREDENTIALS_PATH`
4. Run the `Conversation_v4.py` script to start the assistant.

## Usage

Interact with the assistant using your voice. Say "quit" to end the conversation.

## Dependencies

- OpenAI
- Google Cloud Speech-to-Text
- Google Cloud Text-to-Speech
- sounddevice
- webrtcvad
- pydub
- matplotlib
- tkinter

## License

[MIT License](LICENSE)

