import datetime
import json
import logging
import os
import random
from pathlib import Path

import aiohttp
import discord
import motor.motor_asyncio
from discord.ext import commands
from utils.mongo import Document

import utils.json_loader

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

description = '''tu madre'''

"""vou instalar umas cenas pera ai e vou criar o server de testes"""
async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("$")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        if not data or "prefix" not in data:
            return commands.when_mentioned_or("$")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or("$")(bot, message)

config_file = utils.json_loader.read_json('config')

bot = commands.Bot(
    command_prefix=get_prefix,
    description=description,
    owner_id=219410026631135232,
    case_insensitive=True
)

bot.config_token = config_file["token"]
bot.connection_url = config_file["mongo"]
logging.basicConfig(level=logging.INFO)
bot.cwd = cwd

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    print("Bot ID:", bot.user.id)
    print("Bot latency:", bot.latency*1000, 2)
    print("Running discord.py version" + discord.__version__)
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["bot"]
    bot.config = Document(bot.db, "config")

    print("Initialized Database\n-----")
    for document in await bot.config.get_all():
        print(document)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith(f"<@!{bot.user.id}>") and \
        len(message.content) == len(f"<@!{bot.user.id}>"
        ):
        data = await bot.config.get_by_id(message.guild.id)
        if not data or "prefix" not in data:
            prefix = "$"
        else:                           
            prefix = data["prefix"] #dasfa ah
        await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)

    await bot.process_commands(message)



if __name__ == "__main__":
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
            # handler feito xd
    bot.load_extension("jishaku")
    bot.run(bot.config_token)