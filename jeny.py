import os 
import discord
from dotenv import load_dotenv
import subprocess
import random
import shutil

load_dotenv()
TOKEN: str | None = os.getenv("DISCORD_TOKEN")
CHANNEL_ID: int = 988215724680052757
ID: str | None = os.getenv("DISCORD_ID")
# CHANNEL_ID: int = 988215725367885876

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has connected!")
    

pro: subprocess.Popen | None = None
@client.event
async def on_message(message):
    global pro
    channel = message.channel
    if str(message.author.id) == ID:
        return
    if (len(message.content) <= 22):
        return

    msg = message.content[22:].strip()

    if (msg == "status"):
        clips = set(os.listdir('security/trigger'))
        if '.DS_Store' in clips:
            clips.remove('.DS_Store')

        if len(clips) == 0:
            await channel.send("All Good")
            return


        await channel.send(f"You have {len(clips)} clips")
        
        for clip in clips:
            frames = os.listdir(f'security/trigger/{clip}')
            if ".DS_Store" in frames:
                frames.remove(".DS_Store")
            await channel.send(f"Fetching random frame per clip")

            choice = random.choice(frames)

            await channel.send(
                file=discord.File(f"security/trigger/{clip}/{choice}")
            )
    elif (msg == 'arm'):
        await channel.send("Armed for 30 minutes, but I'm not counting.")
        # 30 minutes of footage 15 second clips (120 clips )
        pro = subprocess.Popen(
            "python3.10 arm.py --wait 0 --spv 15 --vid_num 120", shell=True, start_new_session=True, stdout=subprocess.PIPE)
    
    elif (msg == 'clear'):
        clips = os.listdir('security/trigger')
        for clip in clips:
            if clip == '.DS_Store':
                continue
            shutil.rmtree(f'security/trigger/{clip}', ignore_errors=False, onerror=None)

        await channel.send("Cleared Clips")

    elif (msg == 'disarm'):
        if not pro:
            await channel.send("Nothing was armed in the first place ")
            return
        await channel.send(f"Disarming process: {pro.pid}")
        pro.kill()
        await channel.send("Disarmed")
    elif (msg == 'suicide'):
        await channel.send("*Jeny fell off a tall bridge*")
        exit()
    # await channel.send("on message")

client.run(str(TOKEN))