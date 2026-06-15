import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=".",
    intents=intents
)

# =========================
# SELECT MENU
# =========================

class TicketSelect(discord.ui.Select):
    def __init__(self):

        options = [

            discord.SelectOption(
                label="Denúncia",
                emoji="⚒️",
                description="Abrir ticket de denúncia"
            ),

            discord.SelectOption(
                label="Dúvidas",
                emoji="❓",
                description="Abrir ticket de dúvidas"
            ),

            discord.SelectOption(
                label="Parceria",
                emoji="⭐",
                description="Abrir ticket de parceria"
            )

        ]

        super().__init__(
            placeholder="➡️ Clique aqui para ver as opções",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        escolha = self.values[0]

        await interaction.response.send_message(
            f"Você selecionou **{escolha}**.",
            ephemeral=True
        )


# =========================
# PAINEL
# =========================

@bot.command()
async def painel(ctx):

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
Seja bem-vindo(a) a central de tickets da moon society 🌙

> Use pra fazer denúncias e fazer
> perguntas sobre o servidor.
>
> Por favor, não crie tickets caso não for
> um dos motivos abaixo:
>
> • Fazer denúncias
> • Tirar dúvidas
> • Fazer parceria

Caso não for nenhum desses motivos, NÃO abra o ticket, pois, você será sujeito a uma punição. 💫
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

        print(erro)

        await ctx.send(
            f"❌ Erro:\n```{erro}```"
        )


# =========================
# TESTE
# =========================

@bot.command()
async def ping(ctx):
    await ctx.send("pong 🤠")


# =========================
# READY
# =========================

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")


# =========================
# START
# =========================

bot.run(os.getenv("DISCORD_TOKEN"))
