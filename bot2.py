import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks
from urllib.parse import urljoin


TOKEN = 'MTE3MzA3Mjc1MDUxNzE3ODUwOA.GBwKLU.DtuR2We_TQsoErc3bt9ZoeJ7DIuL54gSmS3AnM'
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
    posts = soup.find_all('a', href=True)

    
    for post in posts[:5]:
        title = post.get_text(strip=True)
        relative_link = f"{URL}{post['href']}"  #relative links suck
        link = urljoin(URL, relative_link)
        channel = client.get_channel(CHANNEL_ID)
        
        await channel.send(f"New article!!! {title}\nLink: {link}")

@client.event
async def on_ready():
    print(f'bot started as {client.user.name} ({client.user.id})')
    check_blog.start()

client.run(TOKEN)
