import sounddevice as sd
import wavio
import keyboard
import requests
from openai import OpenAI
from playsound import playsound

# Set api key
api_key = 'YOUR_KEY_HERE'

# Define the function to record audio
def record_message():
    # Ask user if they want to record a message
    if input("Record prompt? (y/n) ").lower() != 'y':
        print("Recording aborted.")
        return

    # Define the audio parameters
    fs = 44100  # Sample rate
    seconds = 20  # Maximum recording duration in seconds (for safety)

    print("Recording... Press 'q' to stop.")

    # Start recording
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    # Wait until 'q' is pressed
    #keyboard.wait('q')

    # Stop recording
    sd.stop()

    # Save the recording as a wav file
    wavio.write("recording.wav", recording, fs, sampwidth=2)

# Function to transcribe text
def transcribe_text():
  client = OpenAI(api_key = api_key)

  audio_file = open("recording.wav", "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
  )
  print(transcription)
  return transcription


# Function to create audio
def create_audio(text):
  
  client = OpenAI(api_key = api_key)
  
  response = client.audio.speech.create(
      model="tts-1",
      voice="onyx",
      input=text,
  )
  
  response.stream_to_file("output.mp3")

# Function to translate
def translate_text(text):
  client = OpenAI(api_key = api_key)

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Translate the user prompt into German"},
      {"role": "user", "content": text},
    ]
  )
  return response.choices[0].message.content


def main():
  record_message()
  transcription = transcribe_text()
  translation = translate_text(transcription)
  create_audio(translation)
  playsound("output.mp3")


if __name__ == "__main__":
  main()

