import discord
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')
GUILD=os.getenv('GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(
        f'Logged in as {client.user}\n'        
    )
    print(client.guilds)
    user=client.get_user(int(os.getenv('ME')))
    await user.send('Hello')
    
client.run(TOKEN)
