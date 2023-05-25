#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import speech_recognition as sr
import requests
import pyttsx3
from google_speech import Speech

# read env file

load_dotenv()

def main():

    # OpenAI API inicializalasa

    openaiurl = "https://api.openai.com/v1"
    openai_token = os.getenv("OPENAI_KEY")
    if openai_token == "":
        os.exit(1)
    headers = { "Authorization" : f"Bearer {openai_token}" }

    # Audio beolvasas a mikrofonrol
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("\n\nI'm listening!\n\n")
        audio = r.listen(source)

    folder = "./audio"
    filename = "microphone-results"
    audio_file_path = f"{folder}/{filename}.wav"

    if not os.path.exists(folder):
        os.mkdir(folder)

    # saving audio in wav format
    print(f"\n\nGenerating WAV file: {audio_file_path}\n\n")
    with open(audio_file_path, "wb") as f:
        f.write(audio.get_wav_data())

    # speech recognition

    url = f"{openaiurl}/audio/transcriptions"

    data = {
        "model": "whisper-1",
        "file": audio_file_path,
    }
    files = {
        "file": open(audio_file_path, "rb")
    }

    response = requests.post(url, files=files, data=data, headers=headers)

    print("\n\nSpeach recognition using Whisper API\n\n", response.status_code)
    speech_to_text = response.json()["text"]
    print("\n\nResponse from the server:\n\n", speech_to_text)

    # communicating with openai chat api endpoint

    print("\n\nThinking ...\n\n")

    url = f"{openaiurl}/chat/completions"

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a very funny and sarcastic, but helpful assistant."
            },
            {
                "role": "user",
                "content": speech_to_text,
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    print("\n\njson\n\n", response.json())

    print("\n\nResponse from the server\n\n", response.status_code)
    chatgpt_response = response.json()["choices"][0]["message"]["content"]
    print("\n\nText response\n\n", chatgpt_response)   
    
    # text to speech using google's api

    text = chatgpt_response
    lang = "en"
    speech = Speech(text, lang)
    speech.play()   

    # ennyi :)

    print ("Kesz, Koszonom!\n\n")

# main function

if __name__ == "__main__":
    main()
