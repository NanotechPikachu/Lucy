import discord
from discord.ext import commands, tasks
import asyncio
import os
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import discord.ui
from json import load, dump
import random

intents = discord.Intents.all()

intents.members = True
bot = commands.Bot(command_prefix="x!", intents=intents)

class Harvest(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Bot is online")

  @commands.command()
  async def harvestor(self, ctx):
    users = await get_har_data()
    user = ctx.author 
    if str(user.id) not in users:
      await start_har(user) 
    else: 
      embed = discord.Embed(title=f"{ctx.author}'s Harvestor", description=f"Type `x!harvest` to harvest all Khiona-Energy in the Harvestor", color= discord.Color.random())
      current = users[str(user.id)]["harvesting"] 
      embed.add_field(name = "Harvestor", value = current) 
      await ctx.send(embed = embed)
 
    @commands.command()
    async def begin(self, ctx):
      users = await get_har_data()
      await start_har(ctx.author)
      em = discord.Embed(title = "Begin Harvest", description = "Congratulations! You have started your journey of collecting **Khiona-Energy**.", color = discord.Color.random())
      await ctx.send(embed=em)
      user = ctx.author
      @tasks.loop(seconds = 5)
      async def amt(self):
        amt = users[str(user.id)]["harvesting"] + 1
        with open("Khiona.json", "w") as f:
          dump(users,f)

    @commands.command(aliases = ["Balancez", "balz"])
    async def balancez(self, ctx):
        await start_har(ctx.author)   
        user = ctx.author
        users = await get_har_data()
        amt = users[str(user.id)]["Khiona-Energy"]
        zero = str(0)
        em = discord.Embed(
            title= (f"{user.name}'s Khiona-Energy"),color= discord.Color.random())
        em.add_field(name = "Khiona-Energy", value = (f"{amt}"))
        em.set_thumbnail(url = ctx.author.avatar)
        await ctx.send(embed = em)
    
    @commands.command()
    async def harvest(self, ctx):
      await start_har(ctx.author)
      users = await get_har_data()
      user = ctx.author
      current = users[str(user.id)]["harvesting"]
      if current == 0: 
        await ctx.send("The Harvestor haven't harvested any **Khiona-Energy** yet!", delete_after=10)
      else:
        embed = discord.Embed(title = f"{user.name}s Harvest", description=f"{ctx.author.mention} collected **{current} Khiona-Energy** from the Harvestor!")
        await update_khiona(ctx.author,-1* current)
        await ctx.send(embed = embed)

async def update_khiona(user, change = 0): 
  users = await get_har_data()
  users[str(user.id)]["Khiona-Energy"] += int(change)
  with open ("Khiona.json", "w") as f:
    dump(users,f) 
  balance = [users[str(user.id)]["Khiona-Energy"]]
  return balance

async def start_har(user): 
  users = await get_har_data() 
  if str(user.id) in users: 
    return False 
  else: 
    users[str(user.id)] = {}
    users[str(user.id)]["harvesting"] = 0
  with open ("Khiona.json", "w") as f:
    dump(users,f) 
  return True
  
async def get_har_data(): 
  with open ("Khiona.json", "r") as f: 
    users = load(f) 
  return users

async def setup(bot):
   await bot.add_cog(Harvest(bot))
