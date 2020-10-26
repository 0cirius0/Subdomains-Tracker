import discord
import subprocess
from dotenv import load_dotenv
import os
import time
import threading
import subprocess

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
    threading.Timer(10,execute, ()).start()  



@client.event
async def on_message(message):
    if(message.author == client.user):      #Ignore messages by bot itself
	    return

    prefix="track"
    words=message.content.split(' ')
    if(words[0].lower() == prefix ):
        if(words[1].lower() == "add"):
            if(words[2].lower() == "domain"):
                print("OK")
                dom=words[3]
                domain_file=open("./tmp/domains_list","a+")
                domain_file.write(dom)			     
                await message.author.send("Added!")
                domain_file.close()
            elif(words[2].lower() == "command"):
                com=words[3]
                command_file=open("./tmp/commands_list","a+")
                command_file.write(com)
                await message.author.send("Added!")
                command_file.close()

async def custom():
    process = subprocess.Popen("echo nice", shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)
    user=client.get_user(int(os.getenv('ME')))
    await user.send('Halo')
    print("OK")

def execute():
    pwd=subprocess.check_output("pwd",shell=True)
    commands=open(pwd.decode('utf-8').strip()+"/tmp/commands_list)","r+")    #Why it is not able to read the file
    domains=open(pwd.decode('utf-8').strip()+"/tmp/domains_list","r+")
    lines=commands.readlines()
    for line in lines:
        command=line.strip()
        lines2=domains.readlines()
        for l in lines2:
            domain=l.strip()
            t=threading.Thread(target=run, args=(command,domain,))
            threads.append(t)
            t.start()
        for x in threads:
            x.join()

def run(what,where):
    cmd=what+where+" >> ./tmp/"+where+"_sub.txt"
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()       

#asyncio.ensure_future(custom(client))

client.run(TOKEN)
