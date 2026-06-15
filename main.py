import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("pong 🤠")

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")
    print("discord.py:", discord.__version__)

bot.run(os.getenv("DISCORD_TOKEN"))
