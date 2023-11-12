import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks
from urllib.parse import urljoin
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = 1132481238960181300  
URL = 'https://www.sixfootscience.com/brain-snips'
testing = True

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@tasks.loop(minutes=1)
async def check_blog():
    response = requests.get(URL)

    #beautiful soup literally does everything
    soup = BeautifulSoup(response.content, 'html.parser')
    post = soup.find('a', href=True)
    title = post.get_text(strip=True)
    if(check_blog.title != title):
        check_blog.title = title 
        relative_link = f"{URL}{post['href']}" 
        link = urljoin(URL, relative_link)
        channel = client.get_channel(CHANNEL_ID)
        await channel.send(f"New article!!! {title}\nLink: {link}")

@client.event
async def on_ready():
    print(f'bot started as {client.user.name} ({client.user.id})')
    check_blog.start()

client.run(TOKEN)
