import discord
from discord.ext import commands
import os

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def teste(ctx):

    view = discord.ui.LayoutView()

    container = discord.ui.Container()

    container.add_item(
        discord.ui.TextDisplay(
            "# MOON SOCIETY\n\nTeste do Components V2 🤠"
        )
    )

    view.add_item(container)

    await ctx.send(view=view)

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))
