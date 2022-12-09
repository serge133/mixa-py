import requests
from dotenv import load_dotenv
import os
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ENDPOINT="https://discord.com/api/v9/channels/1050564309547233385/messages"

payload = {
    'content': ""
}

permission = 8

header: dict[str, str] = {
    'authorization': DISCORD_TOKEN if DISCORD_TOKEN else 'not authorized',
}

def send_message(text: str = "Hello") -> bool:
    payload['content'] = text
    r = requests.post(
        url=ENDPOINT,
        data=payload,
        headers=header
    )
    if r.status_code != 200:
        print(r.status_code)
        return False
    return True
