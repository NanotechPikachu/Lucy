import discord
from discord.ext import commands
import asyncio
import os
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import discord.ui
import json
from webserver import keep_alive
from cogs import EXTENSIONS

intents = discord.Intents.all()

intents.members = True
bot = commands.Bot(command_prefix="x!", intents=intents)

bot.remove_command("help")

async def load():
  for extension in EXTENSIONS:
    await bot.load_extension(extension)

keep_alive()

async def main():
  await load()
  await bot.start(TOKEN)
asyncio.run(main())
