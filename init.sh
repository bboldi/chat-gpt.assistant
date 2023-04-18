#! /bin/bash

# install libs
sudo apt-get install libasound-dev
sudo apt install python3-pyaudio
sudo apt-get install sox libsox-fmt-mp3

# install python libs
pip install SpeechRecognition
pip install pyttsx3
pip install python-dotenv
pip install google_speech
