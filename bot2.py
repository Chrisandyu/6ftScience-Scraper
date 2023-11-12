import requests
import os
import random
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks
from urllib.parse import urljoin
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = 1132481238960181300  
URL = 'https://www.sixfootscience.com/brain-snips'

intents = discord.Intents.default()
client = discord.Client(intents=intents)

phrases = [
    "New post!!!",
    "New blog update!",
    "Read all about it!",
    "Update:",
    "Fresh post:",
    "New article:",
    "Our latest post:"
    "Check it out:",
    "New topic!!",
    "New blog post:",
    "New brain snip!",
]

@tasks.loop(minutes=1)
async def check_blog():
    response = requests.get(URL)

    #beautiful soup literally does everything
    soup = BeautifulSoup(response.content, 'html.parser')

    title_element = soup.find('h1', class_='blog-title').find('a')

    title = title_element.get_text(strip=True)

    if check_blog.title != title:
        check_blog.title = title 
        print('new post: ' + title)

        relative_link = title_element['href']
        link = urljoin(URL, relative_link)

        random_phrase = random.choice(phrases)
        role = discord.utils.get(client.guilds[0].roles, name="Blog ping")
        mention = role.mention

        channel = client.get_channel(CHANNEL_ID)
        await channel.send(f"{mention} **{random_phrase}** {title}\n{link}")

check_blog.title = None
@client.event


async def on_ready():
    print(f'bot started as {client.user.name} ({client.user.id})')
    check_blog.start()

client.run(TOKEN)
