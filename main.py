import discord,os,schedule,time,asyncio,http.client,urllib,requests
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()


client = commands.Bot(command_prefix = ".", self_bot=True)

token = os.getenv("token")
pushover_app_token = os.getenv("pushover_app_token")
pushover_user_token = os.getenv("pushover_user_token")

client.remove_command("help")



@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching, name="For Deleted Messages"))    
    print ("=" * 40)
    print(f"Logged In As {client.user}")
    print ("=" * 40)


@client.event
async def on_message_delete(message):
    if isinstance(message.channel,discord.channel.DMChannel) and message.author != client.user:
        importantPeople = [1041030518420013086,688493862054133785]

        if message.author.id in importantPeople:

            if message.content.startswith("."):
                pass 
            else:
                conn = http.client.HTTPSConnection("api.pushover.net:443")
                conn.request("POST","/1/messages.json",
                urllib.parse.urlencode({
                    "token": f"{pushover_app_token}",
                    "user": f"{pushover_user_token}",
                    "title": "Logged Deleted Message In DMs",
                    "message": f"Deleted Message From: {message.author}\nContent: {message.content}",
                    "priority": "2",
                    "retry": "60",
                    "expire": "3600"
                }), { "Content-type": "application/x-www-form-urlencoded"})

        else:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST","/1/messages.json",
                urllib.parse.urlencode({
                    "token": f"{pushover_app_token}",
                    "user": f"{pushover_user_token}",
                    "title": "Logged Deleted Message In DMs",
                    "message": f"Deleted Message From: {message.author}\nContent: {message.content}",
                }), { "Content-type": "application/x-www-form-urlencoded"})
    elif isinstance(message.channel,discord.channel.GroupChannel) and message.author != client.user:
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST","/1/messages.json",
        urllib.parse.urlencode({
            "token": f"{pushover_app_token}",
            "user": f"{pushover_user_token}",
            "title": "Logged Deleted Message In Group Chat",
            "message": f"Deleted Message From: {message.author}\nContent: {message.content}",
        }), { "Content-type": "application/x-www-form-urlencoded"})
                

@client.event
async def on_message(message):
        if isinstance(message.channel,discord.channel.DMChannel) and message.author != client.user:
            importantPeople = [1041030518420013086]
            content = message.content[22:]
            if message.author.id in importantPeople:
                if message.mentions:
                    conn = http.client.HTTPSConnection("api.pushover.net:443")
                    conn.request("POST","/1/messages.json",
                    urllib.parse.urlencode({
                        "token": f"{pushover_app_token}",
                        "user": f"{pushover_user_token}",
                        "title": "You Have Been Pinged!",
                        "message": f"You Have Been Pinged By: {message.author}\nContent: {content}",
                    }), { "Content-type": "application/x-www-form-urlencoded"})



client.run(token)

