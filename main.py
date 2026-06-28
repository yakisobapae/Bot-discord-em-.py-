import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# =========================
# CONFIG
# =========================

STAFF_ROLE_ID = 1498522857356132465
OWNER_ID = 1496941098009100519
TICKET_CHANNEL_ID = 1498477718499492069

# =========================
# SELECT MENU
# =========================

class TicketSelect(discord.ui.Select):
    def __init__(self):

        options = [

            discord.SelectOption(
                label="Denúncia",
                emoji="<a:warn:1520533946914308426>"
            ),

            discord.SelectOption(
                label="Suporte",
                emoji="<:logodc:1520533477613895802>"
            ),

            discord.SelectOption(
                label="Parceria",
                emoji="<:istrelinhaxxa1:1520533561805901844>"
            ),

            discord.SelectOption(
                label="Tornar Staff",
                emoji="<:istefi:1520533621398700043>"
            )

        ]

        super().__init__(
            placeholder="Escolha uma opção de ticket",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        canal = interaction.guild.get_channel(TICKET_CHANNEL_ID)

        if not canal:
            return await interaction.response.send_message(
                "Canal de tickets não encontrado.",
                ephemeral=True
            )

        escolha = self.values[0]

        user = interaction.user

        nome_thread = f"{escolha} ✦ {user.name} ✦ {user.id}"

        try:

            thread = await canal.create_thread(
                name=nome_thread
            )

            await thread.add_user(user)

            # =========================
            # DENUNCIA
            # =========================
            if escolha == "Denúncia":

                await thread.send(f"<@&{STAFF_ROLE_ID}>")

                await thread.send("""
<a:warn:1520533946914308426> | Denúncia

Alguém da equipe staff irá te atender.

Por favor mantenha respeito.

Tenha em mãos:
• Prints
• ID ou nome do infrator
""")

            # =========================
            # SUPORTE
            # =========================
            elif escolha == "Suporte":

                await thread.send(f"<@&{STAFF_ROLE_ID}>")

                await thread.send("""
<:logodc:1520533477613895802> | Suporte

Um staff irá te atender em breve.

Explique sua dúvida com clareza.
""")

            # =========================
            # PARCERIA
            # =========================
            elif escolha == "Parceria":

                await thread.send(f"<@{OWNER_ID}>")

                await thread.send("""
<:istrelinhaxxa1:1520533561805901844> | Parceria

O dono do servidor irá te responder.

Requisitos:
• +700 membros
• Público ativo
• Sem conteúdo +18
""")

            # =========================
            # TORNAR STAFF
            # =========================
            elif escolha == "Tornar Staff":

                await thread.send(f"<@{OWNER_ID}>")

                await thread.send("""
<:istefi:1520533621398700043> | Tornar Staff

Explique por que você quer fazer parte da equipe.

O dono irá avaliar sua solicitação.
""")

            await interaction.response.send_message(
                f"Ticket criado com sucesso!\n{thread.mention}",
                ephemeral=True
            )

        except Exception as e:

            await interaction.response.send_message(
                f"Erro: {type(e).__name__}: {e}",
                ephemeral=True
            )

# =========================
# PERSISTENT VIEW
# =========================

class TicketView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        container = discord.ui.Container()

        container.add_item(
            discord.ui.TextDisplay("# MOON SOCIETY")
        )

        container.add_item(
            discord.ui.TextDisplay("""
Seja bem-vindo(a) à central de tickets da Moon Society 🌙

• Denúncia
• Suporte
• Parceria
• Tornar Staff

Escolha abaixo o tipo de atendimento.
""")
        )

        container.add_item(discord.ui.Separator())

        row = discord.ui.ActionRow()
        row.add_item(TicketSelect())

        container.add_item(row)

        self.add_item(container)

# =========================
# PAINEL
# =========================

@bot.command()
async def painel(ctx):
    await ctx.send(view=TicketView())

# =========================
# ON READY
# =========================

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    print(f"Logado como {bot.user}")

# =========================
# START
# =========================

bot.run(os.getenv("DISCORD_TOKEN"))
