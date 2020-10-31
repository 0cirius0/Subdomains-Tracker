import discord
import subprocess
from dotenv import load_dotenv
import os
import time
import asyncio
import threading
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True 

sched = BackgroundScheduler()
sched.start()
load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')
GUILD=os.getenv('GUILD')


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(
        f'Logged in as {client.user}\n'        
    )
    print(client.guilds)
    user=client.get_user(int(os.getenv('ME')))
    #await user.send('Hello')
    in_sec=int(os.getenv('DELAY'))                        #Change this
    print(in_sec)
    await test.start()
    #chec=sched.add_job(test,'interval', seconds = 10)        #Figure out how to call the functions => call execute and check
 
@client.event
async def on_message(message):
    if(message.author == client.user):      #Ignore messages by bot itself
	    return

    prefix="track"
    if(message.author==client.get_user(int(os.getenv('ME')))):
        words=message.content.split(' ')
        if(words[0].lower() == prefix ):
            if(words[1].lower() == "add"):
                if(words[2].lower() == "domain"):
                    print("OK")
                    dom=words[3]
                    domain_file=open("./tmp/domains_list","a+")
                    domain_file.write('\n')
                    domain_file.write(dom)			     
                    await message.author.send("Added!")
                    domain_file.close()
                elif(words[2].lower() == "command"):
                    com=words[3]
                    command_file=open("./tmp/commands_list","a+")
                    command_file.write('\n')
                    command_file.write(com)
                    await message.author.send("Added!")
                    command_file.close()

@tasks.loop(seconds=10.0)
async def test():                     #Problem: Holds the main thread
    print("Worked")
    await atest()
    time.sleep(10)
    #test2()              =>     Run this function in background
    print("Awake")

def execute():
    commands=open("./tmp/commands_list","r+")   
    domains=open("./tmp/domains_list","r+")
    lines=commands.readlines()
    counter=0
    for line in lines:
        counter+=1
        command=line.strip()
        threads=[]
        lines2=domains.readlines()
        for l in lines2:
            domain=l.strip()
            t=threading.Thread(target=run, args=(command,domain,counter,))
            threads.append(t)
            t.start()
        for x in threads:
            x.join()
        domains.seek(0)
    commands.close()
    domains.close() 

def run(what,where,flag):
    cmd=what+" "+where+" > ./tmp/"+where+"_sub.txt" 
    cmd2=what+" "+where+" >> ./tmp/"+where+"_sub.txt"                              
    print(cmd)
    if(flag == 1):
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
    else:
        process = subprocess.Popen(cmd2, shell=True)
        process.wait()
       

def check():
    sites=open("./tmp/domains_list","r+")
    sites_lines=sites.readlines()
    loc="./tmp/"
    for a in sites_lines:
        fname=a.strip()+"_sub.txt"
        f2name="."+fname
        if(os.path.isfile(loc+f2name)):
            subprocess.Popen("diff "+loc+fname+" "+loc+f2name+" | grep '<' | sed 's/^< //g' > ./tmp/changes_"+a.strip(),shell=True).wait()          
            subprocess.Popen("cp "+loc+fname+" "+loc+f2name,shell=True).wait()
        else:
            subprocess.Popen("cp "+loc+fname+" "+loc+f2name,shell=True).wait()
        #if(os.path.isfile(loc+"changes_"+a.strip()):
            
    sites.close()

async def atest():
    user1=client.get_user(int(os.getenv('ME')))
    print("SSleeping")
    #time.sleep(10)
    await user1.send("OK")

def test2():
    time.sleep(20)
    print("Slept")
    
client.run(TOKEN)
