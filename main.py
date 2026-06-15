import discord
from discord.ext import commands
import os

print("discord.py:", discord.__version__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

    print("LayoutView:", hasattr(discord.ui, "LayoutView"))
    print("Container:", hasattr(discord.ui, "Container"))
    print("TextDisplay:", hasattr(discord.ui, "TextDisplay"))
    print("Section:", hasattr(discord.ui, "Section"))
    print("MediaGallery:", hasattr(discord.ui, "MediaGallery"))


@bot.command()
async def ping(ctx):
    await ctx.send("pong 🤠")


@bot.command()
async def v2(ctx):

    try:

        view = discord.ui.LayoutView()

        container = discord.ui.Container()

        text = discord.ui.TextDisplay(
            "# MOON SOCIETY\n\nTeste do Components V2 🤠"
        )

        container.add_item(text)

        view.add_item(container)

        await ctx.send(
            view=view
        )

    except Exception as e:

        erro = f"{type(e).__name__}: {e}"

        print("ERRO V2:", erro)

        await ctx.send(
            f"❌ ERRO V2:\n```{erro}```"
        )


bot.run(os.getenv("DISCORD_TOKEN"))
