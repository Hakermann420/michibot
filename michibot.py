import os
import time
import random
import asyncio

import discord
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv('TOKEN')
ANNOY_USER_ID = os.getenv('ANNOY_USER') # Lakus id

SERVERS = {}
SERVER_EMOJIS = []
EMOJI_IDS = []

stop = False

intent = discord.Intents.all()
client = discord.Client(intents=intent)

async def ping_loop():
    global SERVER_EMOJIS

    await client.wait_until_ready()
    await asyncio.sleep(5)

    while client.is_ready:
        for server in client.guilds:
            msg = "michi" + random.choice(SERVER_EMOJIS)
            user = random.choice(SERVERS[server.id]['USERS'])

            msg = user + msg

            channel = client.get_channel(SERVERS[server.id]['MICHI_CHANNEL'])
            await channel.send(msg, tts=True)
        await asyncio.sleep(random.randint(30*60, 60*60*24))

    print("end pingloop")


@client.event
async def on_ready():
    global SERVER_EMOJIS

    for server in client.guilds:
        SERVERS[server.id] = {}

        USERS = []

        for emoji in server.emojis:
            SERVER_EMOJIS.append(" <:" + emoji.name + ":" + str(emoji.id) + "> ")
            EMOJI_IDS.append(emoji.id)

        for user in server.members:
            USERS.append("<@!" + str(user.id) + "> ")

        USERS.append("@everyone ")

        for channel in server.channels:
            if channel.name == "michi":
                SERVERS[server.id]['MICHI_CHANNEL'] = channel.id
        
        SERVERS[server.id]['USERS'] = USERS

    print(SERVERS)

    michi.start()

@client.event
async def on_message(message):
    global stop
    global SERVER_EMOJIS

    role = discord.utils.get(message.guild.roles, name="bots")
    if role in message.author.roles and message.author != client.user:
        EMOJI = client.get_emoji(random.choice(EMOJI_IDS))
        await message.add_reaction(EMOJI)

    if message.content == '!ping':
        await message.channel.send("!pong", tts=True)

    if message.author.id == ANNOY_USER_ID and message.channel.name == "michi":
        EMOJI = client.get_emoji(random.choice(EMOJI_IDS))
        await message.add_reaction(EMOJI)

    if message.channel.name == "zhaeln":
        
        try:
            if not stop:
                i = int(message.content)
                await message.channel.send(str(i+1), tts=True)
                time.sleep(0.5)
                return
            else:
                stop = False
                i = 10 * (1/0)
        except:
            if message.author == client.user:
                return

            stop = False
            if message.content == "!stop":
                stop = True
            else:
                await message.channel.send("Michi ist zu dumm Zahlen, die nicht integer sind, zu erhöhen", tts=True)

@tasks.loop(minutes=1)
async def michi():
    global SERVER_EMOJIS

    for server in client.guilds:
        msg = "michi" + random.choice(SERVER_EMOJIS)

        channel = client.get_channel(SERVERS[server.id]['MICHI_CHANNEL'])
        await channel.send(msg, tts=True)

client.loop.create_task(ping_loop())
client.run(TOKEN)