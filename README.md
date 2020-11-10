# Subdomains-Tracker
A Discord Bot to help with Recon Stuff

It will scan the target at regular intervals and message user if 
* any new domain is added => New Domain = More attack vectors
* a older domain becomes vulnerable for subdomain takeover

This bot should be run on a VPS(or either you are among the ones whose system runs 24/7)

Run the script and leave it running in background.Once the script runs it will send a message to you through discord to check whether everything is set up correctly.

You can message the bot commands by replying to the bot.
## Setup
1. Clone the repo.
2. Head over to [Discord Developer](https://discord.com/developers/applications) and create a new application.
3. Go to Bot menu and click *add bot*.
4. Allow both *Privileged Gateway Intents*.
5. Copy the TOKEN and store it, this would be your DISCORD_TOKEN.
6. Go to Oauth2 tab, copy the Client ID and complete this url **https://discord.com/api/oauth2/authorize?client_id=PASTE_YOUR_CLIENTID_HERE&permissions=2048&scope=bot**
7. Make your own discord server and then visit the above URL to bring bot in the server.
8. Open Discord app and allow developer mode in your account.
9. Right click on your server icon and Copy ID which would be the GUILD ID, similarly right click on your avatar and copy your User ID(named ME in .env file).
10. Create a file named .env inside the cloned directory with entries as
```
DISCORD_TOKEN="NzY4NzcwMTk2MTgxMDkwMzM***************************"
GUILD="73449262195041****"
ME="65595694492*****"
DELAY="16"
``` 
> Here Delay is the number of hours after which the scan would take place.You can modify to fit it according to your needs.

## Commands

Currently, there are only two commands for the bot,
* `Track add domain DOMAIN_NAME`
>EX: Track add domain twitter.com 
* `Track add command COMMAND_NAME`
> Ex: Track add command amass enum -d

> You can add more than 1 subdomain enumeration tool's command(as far as that tool is installed on the system and set up correctly).

> All the command and domains are fetched from REPO\_DIRECTORY/tmp/domains\_list and REPO\_DIRECTORY/tmp/commands\_list which can be cross checked and edited manually.

## How this works

The Bot script will run each command given in ~/tmp/commansd\_list at regular specified intervals with all the domains specified in ~/tmp/domains\_list to check for new subdomains under the specified domain and alerts through a message of any new subdomain found.

It also runs subjack at every 12 hours to check if any present subdomain becomes vulnerable to subdomain takeover and alerts accordingly.

### Note:
If you found any error while running the script do let me know through raising an issue on github, I'll try to help as much as I can.

- Do check that subjack is correctly installed and GO directory is present in the PATH variable.
