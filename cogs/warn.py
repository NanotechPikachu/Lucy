import discord
from discord.ext import commands
import asyncio
import os
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import discord.ui
import json
import random

intents = discord.Intents.all()

intents.members = True
bot = commands.Bot(command_prefix="x!", intents=intents)

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
      print("Bot is online-2")

    @commands.command()
    @commands.has_permissions(administrator = True) #Permission finder.
    async def warns(self, ctx): #To find the authors warn
        await open_warn(ctx.author)
        user = ctx.author
        users = await get_warn_data()
        wallet = users[str(user.id)]["Warns"]
        zero = str(0)
        em = discord.Embed(
            title= (f"{user.name}'s Warns"),color= discord.Color.random())
        em.add_field(name = "Warns", value = (f":warning: {wallet}"))
        em.set_thumbnail(url = ctx.author.avatar)
        await ctx.send(embed = em)
    @warns.error #If the user doesnt have the above mentiond perms, the below takes place.
    async def warns_error(self, ctx, error):
      if isinstance(error, MissingPermissions):
        Embed5 = discord.Embed(
          title = "Warns Error",
          description = "⚠️ You don't have enough permissions!", color = discord.Color.red())
        await ctx.message.delete()
        await ctx.send(embed = Embed5, delete_after = 10)

    @commands.command(aliases = ["w_of", "wn_of"]) #To find others warns
    @commands.has_permissions(administrator = True)
    async def warn_of(self, ctx,member: discord.Member):
        await open_warn(ctx.author)
        await open_warn (member)
        user = ctx.author
        users = await get_warn_data()
        
        wallet = users[str(member.id)]["Warns"]
        zero = str(0)
        em = discord.Embed(
            title= (f"{member.name}'s Warns"),color= discord.Color.random())
        em.add_field(name = "Warns", value = (f":warning: {wallet}"))
        await ctx.send(embed = em)
    @warn_of.error
    async def warn_of_error(self, ctx, error):
      if isinstance(error, MissingPermissions):
        Embed5 = discord.Embed(
          title = "Warn_of Error",
          description = "⚠️ You don't have enough permissions!", color = discord.Color.red())
        await ctx.message.delete()
        await ctx.send(embed = Embed5, delete_after = 10)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def warn(self, ctx, member: discord.Member): #To warn others.
        await open_warn(ctx.author)
        await open_warn(member)
        user = ctx.author
        users = await get_warn_data()
        
        amount = 1
        await update_warn(member, amount, "Warns")
        em = discord.Embed(title=(f'Warned {member}'), description=(f'{member.mention} has been **warned** by {ctx.author.mention}'), color = discord.Color.random())
        await ctx.send(embed=em)
    @warn.error
    async def warn_error(self, ctx, error):
      if isinstance(error, MissingPermissions):
        Embed5 = discord.Embed(
          title = "Warn Error",
          description = "⚠️ You don't have enough permissions!", color = discord.Color.red())
        await ctx.message.delete()
        await ctx.send(embed = Embed5, delete_after = 10)

    @commands.command(aliases = ['rem_warn', 'r_warn', 'rem_w'])
    @commands.has_permissions(administrator = True)
    async def remove_warn(self, ctx, member: discord.Member): #To remove others warns
        await open_warn(ctx.author)
        await open_warn(member)
        user = ctx.author
        users = await get_warn_data()
        
        amount = -1
        await update_warn(member, amount, "Warns")
        em = discord.Embed(title=(f'Warn removed of {member}'), description=(f'{member.mention}s **warning has been removed** by {ctx.author.mention}'), color = discord.Color.random())
        await ctx.send(embed=em)
    @warn.error
    async def remove_warn_error(self, ctx, error):
      if isinstance(error, MissingPermissions):
        Embed5 = discord.Embed(
          title = "Remove Warn Error",
          description = "⚠️ You don't have enough permissions!", color = discord.Color.red())
        await ctx.message.delete()
        await ctx.send(embed = Embed5, delete_after = 10)
  
async def open_warn(user):        
    users =  await get_warn_data()
    if str(user.id) in users:
      return False
    else:
      users[str(user.id)] = {}
      users[str(user.id)]["Warns"] = 0 
    with open ("file.json", "w") as f:
      json.dump(users,f)
    return True 

async def get_warn_data():
    with open ("file.json", "r") as f:
      users = json.load(f)
    return users

async def update_warn(user, change = 0, mode = "Warns"):
    users = await get_warn_data()
    users[str(user.id)][mode] += int(change)
    with open ("file.json", "w") as f:
        json.dump(users,f)        
    balance = [users[str(user.id)]["Warns"]]
    return balance

async def setup(bot): #The cog maker
   await bot.add_cog(Warn(bot))
