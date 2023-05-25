# Speech Assistant using OpenAI

This is a speech assistant built using OpenAI API. It allows you to speak to the microphone and converts your speech into text. The text is sent to OpenAI ChatGPT API which generates a response. The response is then read out loud to you using Google Speech.

## Setup

1. Clone this repository.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Create an `.env` file and include your OpenAI API key like this:
    ```
    OPENAI_KEY=xxxxxxxxxxxxxxxxxxxxxxx
    ```
4. Run the `assistant.py` file using `python assistant.py`.

## How to use

1. Speak clearly into the microphone when prompted.
2. Wait for the response from the assistant.

That's it! You can start speaking to the assistant and it will respond accordingly.
