"""
In the following code, I have added cooldown cmd in 2 cmds. So, any of them can only be used 1 time within the specified time.
This means, if I take my code into consideration, eithor rob or beg cmd can only be used 1 time in 12 hours. So, if you use rob, then you can neither use rob nor beg in 12 hours.
"""

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

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 43200, commands.BucketType.user) #The cooldown system. All the cmds in this class will have the same cooldown if specified in cmds.
    @commands.Cog.listener()
    async def on_ready(self):
      print("Bot is online")
  
    @commands.command(aliases = ["Balance", "bal"])
    async def balance(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        walletamt = users[str(user.id)]["Credits"]
        zero = str(0)
        em = discord.Embed(
            title= (f"{user.name}'s balance"),color= discord.Color.random())
        em.add_field(name = "Credits", value = (f"<a:Coin:1088127439990947910> {walletamt}"))
        em.set_thumbnail(url = ctx.author.avatar)
        await ctx.send(embed = em)
        


    @commands.command(aliases = ["b_of", "bal_of"])
    async def balance_of(self, ctx,member: discord.Member):
        await open_account(ctx.author)
        await open_account (member)
        user = ctx.author
        users = await get_bank_data()
        
        walletamt = users[str(member.id)]["Credits"]
        zero = str(0)
        em = discord.Embed(
            title= (f"{member.name}'s balance"),color= discord.Color.random())
        em.add_field(name = "Credits", value = (f"<a:Coin:1088127439990947910> {walletamt}"))
        await ctx.send(embed = em)

    @commands.command()
    async def rob(self, ctx, member: discord.Member):
      bucket = self._cd.get_bucket(ctx.message) #Cooldown cmd
      retry_after = bucket.update_rate_limit()
      if retry_after:
        await ctx.send(f"The command is on cooldown. Please try again in {round(retry_after, 1)} seconds!", delete_after = 10)
      else:
          await open_account(ctx.author)
          await open_account (member)
          bal = await update_bank(member)
          if bal[0]<100:
            await ctx.send("Its not worth it!")
            return
          earnings=random.randrange(0, bal[0]) #The maximum you can rob is the account's balance of the person whom you are robbing.
          await update_bank(ctx.author,earnings, "Credits")
          await update_bank(member, -1*earnings, "Credits")
          em = discord.Embed(title=(f'Robbed from {member}'), description=(f'You robbed <a:Coin:1088127439990947910> {earnings} from {member}!'), color = discord.Color.random())
          await ctx.send(embed=em)
      
    @commands.command()
    async def beg(self, ctx):
        bucket = self._cd.get_bucket(ctx.message) #Cooldown cmd
      retry_after = bucket.update_rate_limit()
      if retry_after:
        await ctx.send(f"The command is on cooldown. Please try again in {round(retry_after, 1)} seconds!", delete_after = 10)
      else:
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        
        earning = random.randrange(101) #the maximum you can get from begging is 100 credits
        print (earning)
        em=discord.Embed(title="Beg", description=f"You got <a:Coin:1088127439990947910> {earning} Credits from begging!", color=discord.Color.random())
        await ctx.send (embed=em)
        users[str(user.id)]["Credits"] += earning

        with open ("file.json", "w") as f:
            json.dump(users,f)

    @commands.command()
    async def pay(self, ctx,member: discord.Member, amount = None):
        user = ctx.author
        users = await get_bank_data()
        balance = (users[str(user.id)]["Credits"])
        amount = int(amount)
        result = balance < int(amount)
        print(f'{balance} and {amount} and {result}')
        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send("Enter the amount")
            return 
        if result is True:
            await ctx.send("Insufficient Credits")
            return
        if int(amount)<0:
            await ctx.send("Invaild Amount")
            return
        await update_bank(ctx.author,-1* int(amount), "Credits")
        await update_bank(member, amount, "Credits")
        em = discord.Embed(title=(f'Paid to {member}'), description=(f'You paid <a:Coin:1088127439990947910> {amount} to {member}!'), color = discord.Color.random())
        await ctx.send(embed=em)
      
    @commands.command(aliases=['store'])
    async def shop(self, ctx):
      em = discord.Embed(title = "Shop", color=discord.Color.random())
      for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")
      await ctx.send(embed = em)

    @commands.command()
    async def buy(self, ctx,item,amount = 1):
      await open_account(ctx.author)
      #await open_bankacc(ctx.author)
      res = await buy_this(ctx.author,item,amount)
      if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!", delete_after=10)
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}", delete_after=10)
            return
      em = discord.Embed(title='Item bought!', description=(f"{ctx.author.mention} bought {item} × {amount}"), color=discord.Color.random())
      await ctx.send(embed=em)

    @commands.command(aliases=['inventory', 'inv'])
    async def bag(self, ctx):
      await open_account(ctx.author)
      user = ctx.author
      users = await get_bank_data()
      try:
        bag = users[str(user.id)]["bag"]
      except:
        bag = []
      em = discord.Embed(title = "Inventory", color=discord.Color.random())
      for item in bag:
        name = item["item"]
        amount = item["amount"]
        em.add_field(name = name, value = amount)
      await ctx.send(embed = em)
    
    @commands.command()
    async def sell(self, ctx, item, amount = 1):
        await open_account(ctx.author)   
        res = await sell_this(ctx.author,item,amount) 
        if not res[0]:
            if res[1]==1:
                await ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1]==3:
                await ctx.send(f"You don't have {item} in your bag.")
                return
        em = discord.Embed(title = "Item sold!", description = f"{ctx.author.mention} just sold {amount} {item} and got half the real price of the item.", color = discord.Color.random())
        await ctx.send(embed = em)
    
    
mainshop = [
{"name":"Pikachu","price":1000,"description":"An electric type Pokémon."},
{"name":"Bulbasaur","price":500,"description":"A grass type Pokemon."},
{"name":"Charmander","price":500,"description":"A fire type Pokemon."},
{"name":"Squirtle","price":500,"description":"A water type Pokémon."}
           ]
#The above are the shop items followed by item name, price and description. 

async def sell_this(user,item_name,amount,price = None):
      item_name = item_name.lower()
      name_ = None
      for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.5* item["price"] #This means, the amount credited on acc will be half the orginal price set for the item. You can change it as you want. :)
                break
      if name_ == None:
          return [False,1]
        
      cost = price*amount  
      users = await get_bank_data()  
      balance = await update_bank(user)

      try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
      except:
        return [False,3]    
      with open("file.json","w") as f:
        dump(users,f)
      await update_bank(user,cost,"Credits")
      return [True,"Worked"]
    
async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break
    if name_ == None:
        return [False,1]

    cost = price*amount
    users = await get_bank_data()
    balance = await update_bank(user)

    if balance[0]<cost:
        return [False,2]
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
              old_amt = thing["amount"]
              new_amt = old_amt + amount
              users[str(user.id)]["bag"][index]["amount"] = new_amt
              t = 1
              break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
      obj = {"item":item_name , "amount" : amount}
      users[str(user.id)]["bag"] = [obj]        
    with open("file.json","w") as f:
      json.dump(users,f)
    await update_bank(user,cost*-1,"Credits")
    return [True,"Worked"]
    
async def open_account(user):        
    users =  await get_bank_data()
    if str(user.id) in users:
      return False
    else:
      users[str(user.id)] = {}
      users[str(user.id)]["Credits"] = 0 
    with open ("file.json", "w") as f:
      json.dump(users,f)
    return True 

async def get_bank_data():
    with open ("file.json", "r") as f:
      users = json.load(f)
    return users

async def update_bank(user, change = 0, mode = "Credits"):
    users = await get_bank_data()
    users[str(user.id)][mode] += int(change)
    with open ("file.json", "w") as f:
        json.dump(users,f)        
    balance = [users[str(user.id)]["Credits"]]
    return balance

async def setup(bot):
   await bot.add_cog(economy(bot))
