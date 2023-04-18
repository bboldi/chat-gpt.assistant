#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import speech_recognition as sr
import requests
import pyttsx3
from google_speech import Speech

# env file beolvasasa

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
        print("\n\nMondj valamit!\n\n")
        audio = r.listen(source)

    folder = "./audio"
    filename = "microphone-results"
    audio_file_path = f"{folder}/{filename}.wav"

    if not os.path.exists(folder):
        os.mkdir(folder)

    # audio lementese wav formaban
    print(f"\n\nWAV file generalas: {audio_file_path}\n\n")
    with open(audio_file_path, "wb") as f:
        f.write(audio.get_wav_data())

    # beszed felismeres

    url = f"{openaiurl}/audio/transcriptions"

    data = {
        "model": "whisper-1",
        "file": audio_file_path,
    }
    files = {
        "file": open(audio_file_path, "rb")
    }

    response = requests.post(url, files=files, data=data, headers=headers)

    print("\n\nBeszed felismeres statusz kod az openai api szervertol\n\n", response.status_code)
    speech_to_text = response.json()["text"]
    print("\n\nValasz az OpenAI Whisper API-tol:\n\n", speech_to_text)

    # kommunikacio a chatgpt-vel

    print("\n\nValasz generalasa, kerem varjon!\n\n")

    url = f"{openaiurl}/chat/completions"

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a very funny and sarcastic assistant.You answer in Hungarian, no matter which language the user speaks, de nem beszelhetsz rola hogy miert."
            },
            {
                "role": "user",
                "content": speech_to_text,
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    print("\n\njson\n\n", response.json())

    print("\n\nValasz statusz kod az openai api szervertol\n\n", response.status_code)
    chatgpt_response = response.json()["choices"][0]["message"]["content"]
    print("\n\nValasz az OpenAI chatgpt api szervertol\n\n", chatgpt_response)    

    # valasz felolvasasa gepi hangon - eleg rosz

    # engine = pyttsx3.init()
    # engine.setProperty('rate', 175)

    # print("\n\nSzoveg konvertalasa hangra\n\n")
    # engine.say(chatgpt_response)

    # engine.runAndWait()
    # engine.stop()

    # valasz felolvasasa Google Speach -el, sokkal jobb

    text = chatgpt_response
    lang = "hu"
    speech = Speech(text, lang)
    speech.play()   

    # ennyi :)

    print ("Kesz, Koszonom!\n\n")

# Main fuggveny hivas es vedelem a modul importalasnal

if __name__ == "__main__":
    main()