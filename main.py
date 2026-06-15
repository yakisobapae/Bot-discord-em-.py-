import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class TicketSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="📋 Escolha uma opção...",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label="Denúncias",
                    description="Abrir ticket de denúncia",
                    emoji="🤠"
                ),
                discord.SelectOption(
                    label="Dúvidas",
                    description="Abrir ticket de dúvidas",
                    emoji="😃"
                ),
                discord.SelectOption(
                    label="Parceria",
                    description="Abrir ticket de parceria",
                    emoji="😄"
                )
            ]
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Você escolheu: **{self.values[0]}**",
            ephemeral=True
        )

@bot.command()
async def painel(ctx):

    view = discord.ui.LayoutView()

    container = discord.ui.Container()

    container.add_item(
        discord.ui.TextDisplay(
            "# MOON SOCIETY"
        )
    )

    container.add_item(
        discord.ui.TextDisplay(
            """
Seja bem-vindo(a) a central de tickets.

Use pra fazer denúncias e fazer perguntas sobre o servidor.

Por favor, não crie tickets caso não for um dos motivos abaixo:

- Fazer denúncias
- Tirar dúvidas
- Fazer parceria

Caso não for nenhum desses motivos, NÃO abra o ticket.
"""
        )
    )

    view.add_item(container)

    select_view = discord.ui.View(timeout=None)
    select_view.add_item(TicketSelect())

    await ctx.send(
        view=view
    )

    await ctx.send(
        view=select_view
    )

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))
