import discord
from discord.ext import commands
import asyncio
import os
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import discord.ui
from datetime import datetime
import random

class Whois(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      print("Bot is online-W")

    @commands.command(aliases = ['user','info'])
    async def whois(self, ctx, member: discord.Member=None):
      if not member:
        member = ctx.message.author
      roles = [role for role in member.roles[1:]]
      embed = discord.Embed(title=f"User Info - {member}", 
timestamp=ctx.message.created_at, colour=discord.Colour.random()) #The timestamp makes timestamp appear on footer as the embed created date.
      embed.add_field(name="Name", value=member)
      embed.add_field(name="ID:", value=member.id)
      if member.bot: #checking if the mentioned member is bot
        a = "Yes"
      else:
        a = "No"
      embed.add_field(name="Bot?", value=a)
      embed.add_field(name="Account created on", value=discord.utils.format_dt(member.created_at)) #This creates a timestamp and hence is better.
      embed.add_field(name="Joined server on", value=discord.utils.format_dt(member.joined_at))
      embed.add_field(name="Roles", value="".join([role.mention for role in roles]))
      embed.add_field(name="Highest Role", value=member.top_role.mention)
      print(member.top_role.mention)
      embed.set_thumbnail(url=member.avatar)
      embed.set_footer(text=f"Requested by {ctx.author}")
      await ctx.send(embed=embed)

async def setup(bot):
   await bot.add_cog(Whois(bot))
