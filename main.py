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


@bot.command()
async def ping(ctx):
    await ctx.send("pong 🤠")


@bot.command()
async def teste2(ctx):

    try:

        view = discord.ui.LayoutView()

        container = discord.ui.Container()

        container.add_item(
            discord.ui.TextDisplay(
                "# MOON SOCIETY"
            )
        )

        container.add_item(
            discord.ui.TextDisplay(
                "Seja bem-vindo(a) à central de tickets."
            )
        )

        container.add_item(
            discord.ui.TextDisplay(
                "Use este teste para verificar se os Containers V2 estão funcionando corretamente."
            )
        )

        view.add_item(container)

        await ctx.send(view=view)

    except Exception as e:

        erro = f"{type(e).__name__}: {e}"

        print("ERRO TESTE2:", erro)

        await ctx.send(
            f"❌ ERRO:\n```{erro}```"
        )


bot.run(os.getenv("DISCORD_TOKEN"))
