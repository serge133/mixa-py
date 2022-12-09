import os 
import discord
from dotenv import load_dotenv
import os
from arm import arm

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
    

@client.event
async def on_message(message):
    channel = message.channel
    if str(message.author.id) == ID:
        return
    if (len(message.content) <= 22):
        return

    msg = message.content[22:].strip()

    if (msg == "status"):
        clips = os.listdir('security/trigger')
        if '.DS_Store' in clips:
            clips.remove('.DS_Store')

        if len(clips) == 0:
            await channel.send("All Good")
            return


        await channel.send(f"You have {len(clips)} clips")
        
        for clip in clips:
            # Look at last clip
            frames = os.listdir(f'security/trigger/{clip}')
            await channel.send(f"In the last clip, you have {len(frames)} frame(s) that triggered")

            for frame in frames:
                if frame == '.DS_Store':
                    continue
                await channel.send(
                    file=discord.File(f"security/trigger/{clip}/{frame}")
                )
    elif (msg == 'arm'):
        await channel.send("Armed for 30 minutes, but I'm not counting.")

    elif (msg == 'disarm'):
        # event.set()
        await channel.send("Disarmed")
    elif (msg == 'suicide'):
        channel.send("*Jeny fell off a tall bridge*")
        exit()
    # await channel.send("on message")

client.run(str(TOKEN))