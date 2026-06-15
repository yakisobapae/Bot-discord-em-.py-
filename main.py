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

        STAFF_ROLE_ID = 1498522857356132465
        OWNER_ID = 1496941098009100519
        TICKET_CHANNEL_ID = 1498477718499492069

        canal = interaction.guild.get_channel(
            TICKET_CHANNEL_ID
        )

        if canal is None:
            await interaction.response.send_message(
                "❌ Canal de tickets não encontrado.",
                ephemeral=True
            )
            return

        escolha = self.values[0]

        nome_usuario = interaction.user.name
        id_usuario = interaction.user.id

        try:

            if escolha == "Denúncia":

                nome_thread = (
                    f"Denúncia ✦ {nome_usuario} ✦ {id_usuario}"
                )

                thread = await canal.create_thread(
                    name=nome_thread
                )

                await thread.add_user(interaction.user)

                await thread.send(
                    f"<@&{STAFF_ROLE_ID}>"
                )

                await thread.send(
                    """
🤠 | Alguém da equipe staff logo virá atender.

Por favor, tenha cordialidade e respeito pelos nossos staffs.

Tenha os seguintes itens em mãos:

• Prints do ocorrido
• Nome do infrator (ou o Id)
                    """
                )

            elif escolha == "Dúvidas":

                nome_thread = (
                    f"Dúvidas ✦ {nome_usuario} ✦ {id_usuario}"
                )

                thread = await canal.create_thread(
                    name=nome_thread
                )

                await thread.add_user(interaction.user)

                await thread.send(
                    f"<@&{STAFF_ROLE_ID}>"
                )

                await thread.send(
                    """
😃 | Alguém da equipe staff virá atender.

Tenha cordialidade e respeito.

Apresente-nos a sua dúvida que algum staff irá responder.
                    """
                )

            elif escolha == "Parceria":

                nome_thread = (
                    f"Parceria ✦ {nome_usuario} ✦ {id_usuario}"
                )

                thread = await canal.create_thread(
                    name=nome_thread
                )

                await thread.add_user(interaction.user)

                await thread.send(
                    f"<@{OWNER_ID}>"
                )

                await thread.send(
                    """
😄 | O dono do servidor logo virá.

Tenha paciência e tenha em mente que para fechar parceria, tenha:

• Um servidor com no mínimo 700 pessoas
• Um público ativo
• Que não tenha envolvimento algum com NSFW/conteúdo pornográfico ou +18.
                    """
                )

            await interaction.response.send_message(
                f"✅ Ticket de {escolha} criado com sucesso.",
                ephemeral=True
            )

        except Exception as e:

            await interaction.response.send_message(
                f"❌ Erro: {type(e).__name__}: {e}",
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

> Por favor, não crie tickets caso não for
> um dos motivos abaixo:

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
