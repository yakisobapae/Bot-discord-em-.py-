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
LOG_CHANNEL_ID = None  # coloca ID do canal de logs depois se quiser

# =========================
# EMBED PADRÃO
# =========================

def ticket_embed(title, description, color=0x2B2D31):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    return embed

def dm_embed(title, description):
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x000000  # preto
    )
    return embed

# =========================
# STORAGE SIMPLES (ANTI DUPLICATE)
# =========================

open_tickets = {}

# =========================
# SELECT MENU
# =========================

class TicketSelect(discord.ui.Select):
    def __init__(self):

        options = [

            discord.SelectOption(label="Denúncia", emoji="<a:warn:1520533946914308426>"),
            discord.SelectOption(label="Suporte", emoji="<:logodc:1520533477613895802>"),
            discord.SelectOption(label="Parceria", emoji="<:istrelinhaxxa1:1520533561805901844>"),
            discord.SelectOption(label="Tornar Staff", emoji="<:istefi:1520533621398700043>")

        ]

        super().__init__(
            placeholder="Selecione uma opção",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user

        canal = guild.get_channel(TICKET_CHANNEL_ID)

        if user.id in open_tickets:
            return await interaction.response.send_message(
                "❌ Você já tem um ticket aberto.",
                ephemeral=True
            )

        escolha = self.values[0]

        nome = f"{escolha} ✦ {user.name} ✦ {user.id}"

        thread = await canal.create_thread(name=nome)
        await thread.add_user(user)

        open_tickets[user.id] = thread.id

        # =========================
        # MENSAGENS POR TIPO
        # =========================

        if escolha == "Denúncia":

            await thread.send(f"<@&{STAFF_ROLE_ID}>")
            await thread.send(embed=ticket_embed(
                "⚒️ Denúncia",
                "Envie provas e explique o ocorrido."
            ))

        elif escolha == "Suporte":

            await thread.send(f"<@&{STAFF_ROLE_ID}>")
            await thread.send(embed=ticket_embed(
                "❓ Suporte",
                "Explique sua dúvida."
            ))

        elif escolha == "Parceria":

            await thread.send(f"<@{OWNER_ID}>")
            await thread.send(embed=ticket_embed(
                "⭐ Parceria",
                "Pedido de parceria em análise."
            ))

        elif escolha == "Tornar Staff":

            await thread.send(f"<@{OWNER_ID}>")
            await thread.send(embed=ticket_embed(
                "👮 Staff",
                "Explique por que quer entrar na equipe."
            ))

        await interaction.response.send_message(
            f"✅ Ticket criado!\n{thread.mention}",
            ephemeral=True
        )

# =========================
# VIEW
# =========================

class TicketView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        container = discord.ui.Container()

        container.add_item(discord.ui.TextDisplay("# MOON SOCIETY"))

        container.add_item(discord.ui.TextDisplay(
            "Escolha uma opção abaixo para abrir seu ticket 🌙"
        ))

        container.add_item(discord.ui.Separator())

        row = discord.ui.ActionRow()
        row.add_item(TicketSelect())

        container.add_item(row)

        self.add_item(container)

# =========================
# BOTÕES DE AÇÃO (ASSUMIR / FECHAR)
# =========================

class TicketActions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Assumir", style=discord.ButtonStyle.success)
    async def assumir(self, interaction: discord.Interaction, button: discord.ui.Button):

        if STAFF_ROLE_ID not in [r.id for r in interaction.user.roles]:
            return await interaction.response.send_message(
                "❌ Sem permissão.",
                ephemeral=True
            )

        embed = ticket_embed(
            "📌 Ticket Assumido",
            f"O ticket foi assumido por {interaction.user.mention}🌙\n> - tenha respeito e cordialidade"
        )

        await interaction.channel.send(embed=embed)

        # DM pro criador (último usuário no thread)
        async for msg in interaction.channel.history(limit=50, oldest_first=True):
            if msg.author != bot.user:
                user = msg.author
                break

        try:
            await user.send(embed=dm_embed(
                "📌 Ticket Assumido",
                f"Seu ticket foi assumido por {interaction.user.name}"
            ))
        except:
            pass

        await interaction.response.send_message("✅ Assumido.", ephemeral=True)

    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.channel.send("🔒 Fechando ticket...")

        user = None
        async for msg in interaction.channel.history(limit=50, oldest_first=True):
            if msg.author != bot.user:
                user = msg.author
                break

        if user:
            try:
                await user.send(embed=dm_embed(
                    "🔒 Ticket Fechado",
                    "Seu ticket foi fechado pela staff."
                ))
            except:
                pass

        if user and user.id in open_tickets:
            del open_tickets[user.id]

        await interaction.channel.delete()

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
