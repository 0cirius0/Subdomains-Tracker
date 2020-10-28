import discord
import subprocess
from dotenv import load_dotenv
import os
import time
import threading
import subprocess

intents = discord.Intents.default()
intents.members = True 
#intents.messages = True

load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')
GUILD=os.getenv('GUILD')


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(
        f'Logged in as {client.user}'        
    )
    print(client.guilds)
    await client.wait_until_ready()
    user = client.get_user(655956944929947656)
    await user.send('Hello')
    
    
client.run(TOKEN)
    
