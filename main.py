import discord
from discord_slash import SlashCommand
from discord_slash import SlashContext
import platform
import os
import sys
from discord.ext import tasks
from discord.ext.commands import Bot
from discord import message
from time import sleep
import asyncio
import json
import random

#Globals
bot = Bot(command_prefix="*")
slash = SlashCommand(bot, sync_commands=True)
num = 1
gameOver = True
inProgress = False
streak = 0
gameAuthor = ''
with open('data.txt') as file2:
  try:
    leaderboardRaw = json.loads(file2.read())
  except Exception as e:
    print(e)
  

def checkKey(dict, key):
    if key in dict.keys():
        return True
    else:
        return False

#Executes on login
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    print('current leaderboardRaw: ' + str(leaderboardRaw))

#Initializes the command/game
@bot.command()
async def start(ctx):
  global gameOver
  global inProgress
  global gameAuthor
  gameAuthor = str(ctx.message.author)
  if gameOver and not inProgress:
    await ctx.send("Starting...")
    sleep(1)
    await ctx.send("Choose a number. One or two.")
    gameOver = False
    inProgress = True
  else:
    await ctx.send("Please end your current game before you start a new one")


@bot.event
async def on_message(message):
  global number
  number = random.randint(1,2)
  await bot.process_commands(message)


@bot.command()
async def g(ctx, arg):
  global number
  global gameOver
  global inProgress
  global streak
  global gameAuthor
  gameOver = False
  inProgress = True
  author = str(ctx.message.author)
  if author == gameAuthor:
    if not gameOver and inProgress:
      if arg == str(number):
        await ctx.message.add_reaction('✔️')
        streak+=1
      else:
        await ctx.message.add_reaction('❌')
        await ctx.send("Your streak was " + str(streak))
        if leaderboardRaw.get(author) is None:
          leaderboardRaw[author] = streak
        elif checkKey(leaderboardRaw, author):
          if leaderboardRaw[author] < streak:
            leaderboardRaw[author] = streak
        gameOver = True
        inProgress = False
        print(leaderboardRaw)
        streak = 0
    else:
      await ctx.send("Please start a game in order to guess.")
  else:
    pass

async def save():
  while not bot.is_closed():
    try:
      with open('data.txt', 'w+') as f:
        strLeader = json.dumps(leaderboardRaw)
        f.write(strLeader)
        print('saved')
      await asyncio.sleep(10)
    except Exception as e:
      print(e)
      await asyncio.sleep(10)


@bot.command()
async def leaderboard(ctx):
  sort = dict(sorted(leaderboardRaw.items(), key=lambda x: x[1], reverse = True))
  sort = str(sort).replace(',', '\n')
  sort = str(sort).replace('{', '')
  sort = str(sort).replace('}', '')
  sort = str(sort).replace("'", ' ')
  await ctx.send("** Keep in mind this is a _global_  leaderboard **")
  await ctx.send(sort)


@bot.command()
async def highscore(ctx):
  if checkKey(leaderboardRaw, str(ctx.message.author)):
     await ctx.send("**" + str(ctx.message.author) + "'s** highscore is: **" + str(leaderboardRaw[str(ctx.message.author)])) + "**"
  else:
    await ctx.send("Please play the game before asking for your highscore.")
 

bot.loop.create_task(save())

bot.run('ODk0MzQ5OTM4OTkxOTU1OTk4.YVouSQ.WNDVbh0UCOr4qe-oAiZJddww_Gk')