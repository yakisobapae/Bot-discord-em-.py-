import discord
from discord.ext import commands
import os

print("discord.py:", discord.__version__)

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

    print("LayoutView:", hasattr(discord.ui, "LayoutView"))
    print("Container:", hasattr(discord.ui, "Container"))
    print("TextDisplay:", hasattr(discord.ui, "TextDisplay"))
    print("Section:", hasattr(discord.ui, "Section"))
    print("MediaGallery:", hasattr(discord.ui, "MediaGallery"))

bot.run(os.getenv("DISCORD_TOKEN"))
