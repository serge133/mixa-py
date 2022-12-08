import requests
from dotenv import load_dotenv
import os
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ENDPOINT="https://discord.com/api/v9/channels/1040743231983468614/messages"

payload = {
    'content': ""
}

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

for i in range(5):
    send_message(str(i))
