import os
import platform

from MyExperiments.config import telegramConfig
import requests


messages = ""


def send_message(message, flush=False):
    global messages
    messages += message + "\n"

    if not flush:
        return
    else:
        message = messages
        messages = ""

    if 'Darwin' in platform.system():
        print(message)
        return

    # die chat_id ist die aus der obigen Response
    params = {"chat_id": telegramConfig.chat_id, "text": message}
    url = f"https://api.telegram.org/bot{telegramConfig.token}/sendMessage"
    answer = requests.post(url, params=params)
    if not answer.ok:
        raise requests.ConnectionError
