import os 
import discord
from dotenv import load_dotenv
import subprocess
import random
import shutil

load_dotenv()
TOKEN: str | None = os.getenv("DISCORD_TOKEN")
BOT_ID: str | None = os.getenv("DISCORD_ID")
#// CHANNEL_ID: int = 988215724680052757
#// CHANNEL_ID: int = 988215725367885876

# Set up the client 
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has connected!")
    

# GLOBAL variable to handle the process
pro: subprocess.Popen | None = None
@client.event
async def on_message(message):
    global pro # Allows control of process 
    channel = message.channel
    # Do not trigger when bot sends message
    if str(message.author.id) == BOT_ID:
        return
    # Only when the bot is referenced in the discord group
    if (len(message.content) <= 22):
        return

    # Removes the <@BOT-ID> tag in the message 
    msg: str = message.content[22:].strip()

    if (msg == "status"):
        # Sorts the clips in ascending order then checks if macs config file is there to remove it 
        clips = sorted(os.listdir('security/trigger'))
        if clips[0] == '.DS_Store':
            clips = clips[1:]

        # Empty clips then nothing to report 
        if len(clips) == 0:
            await channel.send("All Good")
            return


        # Send how many clips exist 
        await channel.send(f"You have {len(clips)} clips")
        
        for clip in clips:
            frames = sorted(os.listdir(f'security/trigger/{clip}'))
            if frames[0] == '.DS_Store':
                frames = frames[1:]

            await channel.send(f"Fetching random frame per clip")

            # Fetches random frame to show for each clip 
            choice = random.choice(frames)

            # Send the image to the discord group 
            await channel.send(
                file=discord.File(f"security/trigger/{clip}/{choice}")
            )
    # Arms security system 
    elif (msg == 'arm'):
        await channel.send("Armed for 30 minutes, but I'm not counting.")
        # 30 minutes of footage 15 second clips (120 clips )
        # Runs in a seperate process and saves the details to the global variable pro to then be able to kill it 
        pro = subprocess.Popen(
            "python3.10 arm.py --wait 0 --spv 15 --vid_num 120", shell=True, start_new_session=True, stdout=subprocess.PIPE)
    
    # Clears clips and frames 
    elif (msg == 'clear'):
        clips = os.listdir('security/trigger')
        videos = os.listdir('security/video')
        for clip in clips:
            if clip == '.DS_Store':
                continue
            shutil.rmtree(f'security/trigger/{clip}', ignore_errors=False, onerror=None)
        for video in videos:
            if video == '.DS_Store':
                continue
            os.remove(f'security/video/{video}')

        await channel.send("Cleared Clips")

    # Kills the arm process then sets to None for no process running 
    elif (msg == 'disarm'):
        if not pro:
            await channel.send("Nothing was armed in the first place ")
            return
        await channel.send(f"Disarming process: {pro.pid}")
        pro.kill()
        await channel.send("Disarmed")
        pro = None

    # Kills jeny please do not kill her  
    elif (msg == 'suicide'):
        await channel.send("*Jeny fell off a tall bridge*")
        exit()

client.run(str(TOKEN))