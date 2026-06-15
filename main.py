import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=".",
    intents=intents
)

class TicketSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="➡️ Clique aqui para ver as opções",
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


@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")


@bot.command()
async def moon(ctx):

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
                """
Seja bem-vindo(a) a central de tickets.

Use pra fazer denúncias e fazer perguntas sobre o servidor.

Por favor, não crie tickets caso não for um dos motivos abaixo:

• Fazer denúncias
• Tirar dúvidas
• Fazer parceria

Caso não for nenhum desses motivos, NÃO abra o ticket, pois, você será sujeito a uma punição.
                """
            )
        )

        container.add_item(
            discord.ui.Separator()
        )

        row = discord.ui.ActionRow()

        row.add_item(
            TicketSelect()
        )

        container.add_item(row)

        view.add_item(container)

        await ctx.send(view=view)

    except Exception as e:

        erro = f"{type(e).__name__}: {e}"

        print("ERRO:", erro)

        await ctx.send(
            f"❌ ERRO:\n```{erro}```"
        )


bot.run(os.getenv("DISCORD_TOKEN"))
