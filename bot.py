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

print("""

 (                                                                                                                     
 )\ )             )    (                                                 *   )                         )               
(()/(     (    ( /(    )\ )            )        )   (                  ` )  /(   (        )         ( /(     (    (    
 /(_))   ))\   )\())  (()/(    (      (      ( /(   )\    (      (      ( )(_))  )(    ( /(    (    )\())   ))\   )(   
(_))    /((_) ((_)\    ((_))   )\     )\  '  )(_)) ((_)   )\ )   )\    (_(_())  (()\   )(_))   )\  ((_)\   /((_) (()\  
/ __|  (_))(  | |(_)   _| |   ((_)  _((_))  ((_)_   (_)  _(_/(  ((_)   |_   _|   ((_) ((_)_   ((_) | |(_) (_))    ((_) 
\__ \  | || | | '_ \ / _` |  / _ \ | '  \() / _` |  | | | ' \)) (_-<     | |    | '_| / _` | / _|  | / /  / -_)  | '_| 
|___/   \_,_| |_.__/ \__,_|  \___/ |_|_|_|  \__,_|  |_| |_||_|  /__/     |_|    |_|   \__,_| \__|  |_\_\  \___|  |_|   
                                                                                                                       

""")
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(
        f'Logged in as {client.user}\n'        
    )
    print(client.guilds)
    print("<--Ignore all the debug info below! You can now background the process-->")	
    user=client.get_user(int(os.getenv('ME')))
    await user.send('Hello! Script is Running!')
    in_sec=int(os.getenv('DELAY'))*60*60                        
    print(in_sec)
    out.start()
    chec=sched.add_job(execute,'interval', seconds = in_sec)        
    chec2=sched.add_job(takeover,'interval',seconds= in_sec)

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
                    domain_file.write(dom+'\n')			     
                    await message.author.send("Added!")
                    domain_file.close()
                elif(words[2].lower() == "command"):
                    a=' '
                    com=a.join(words[3:])
                    command_file=open("./tmp/commands_list","a+")
                    command_file.write(com+'\n')
                    await message.author.send("Added!")
                    command_file.close()
            if(words[1].lower() == "rm"):
                fl=False
                if(words[2].lower() == "domain"):
                    rem=words[3].lower()
                    domain_file=open("./tmp/domains_list","r")
                    lines=domain_file.readlines()
                    domain_file=open("./tmp/domains_list","w")
                    for line in lines:
                        if(line.strip('\n')==rem):
                            fl=True
                            continue
                        else:
                            domain_file.write(line)
                    if(fl):
                        await message.author.send("Removed!")
                        fl=False
                    else:
                        await message.author.send("Not Found")
                    domain_file.close()
                if(words[2].lower() == "command"):
                    a=' '
                    rem=a.join(words[3:])
                    command_file=open("./tmp/commands_list","r")
                    lines=command_file.readlines()
                    command_file=open("./tmp/commands_list","w")
                    for line in lines:
                        if(line.strip('\n')==rem):
                            fl=True
                            continue
                        else:
                            command_file.write(line)
                    if(fl):
                        await message.author.send("Removed!")
                        fl=False
                    else:
                        await message.author.send("Not Found")
                    command_file.close()

@tasks.loop(hours=12)
async def out():  
    print("Inside out1")                  
    data=check("new")
    if(data):
        user=client.get_user(int(os.getenv('ME')))
        await user.send("New Subdomain/s Found")
        for l in data:
            await user.send(l.strip())         
    print("Inside out2")
    data=check("to")
    if(data):
        user=client.get_user(int(os.getenv('ME')))
        await user.send("Subdomain Takeover Vulnerable Domain Found")
        for l in data:
            await user.send(l.strip())  

def execute():
    print("Inside execute")
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
    print("Inside run")
    cmd=what+" "+where+" > ./tmp/"+where+"_sub.txt" 
    cmd2=what+" "+where+" >> ./tmp/"+where+"_sub.txt"                              
    print(cmd)
    if(flag == 1):
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
    else:
        process = subprocess.Popen(cmd2, shell=True)
        process.wait()
       
def check(con):
    print("Inside check")  
    data=[]                                              
    if(con=="new"):
        print("debug")
        if(os.path.isfile("./tmp/domains_list")):
            sites=open("./tmp/domains_list","r+")
            sites_lines=sites.readlines()
            loc="./tmp/"
            for a in sites_lines:
                fname=a.strip()+"_sub.txt"
                f2name="."+fname
                subprocess.Popen("touch "+loc+"changes",shell=True).wait()
                if(os.path.isfile(loc+f2name)):
                    subprocess.Popen("diff "+loc+fname+" "+loc+f2name+" | grep '<' | sed 's/^< //g' > ./tmp/changes",shell=True).wait()          
                    subprocess.Popen("cp "+loc+fname+" "+loc+f2name,shell=True).wait()
                else:
                    subprocess.Popen("cp "+loc+fname+" "+loc+f2name,shell=True).wait()
                if(os.stat(loc+"changes").st_size != 0):
                    f=open("./tmp/changes","r")
                    data=f.readlines()
                    f.close()
                    subprocess.Popen("rm ./tmp/changes",shell=True).wait()                                                       
            sites.close()
    if(con=="to"):
        if(os.path.isfile("./tmp/takeover")):
            if(os.stat("./tmp/takeover").st_size != 0):
                file1=open("./tmp/takeover","r")
                data=file1.readlines()
                file1.close()
                subprocess.Popen("rm ./tmp/takeover",shell=True).wait()
    return data

def takeover():
    print("Inside takeover")
    dom=open("./tmp/domains_list","r")
    lines=dom.readlines()
    for l in lines:
        b=l.strip()
        subprocess.Popen("subjack -w ./tmp/"+b+"_sub.txt >> ./tmp/takover",shell=True)
    dom.close()
           
client.run(TOKEN)
