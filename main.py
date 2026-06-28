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

FORM_STAFF = "https://forms.gle/ymnid4qmAy3bufew7"

open_tickets = {}

# =========================
# EMBEDS
# =========================

def ticket_embed(title, description):
    return discord.Embed(
        title=title,
        description=description,
        color=0x2B2D31
    )

def dm_embed(title, description):
    return discord.Embed(
        title=title,
        description=description,
        color=0x000000
    )

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

        canal = interaction.guild.get_channel(TICKET_CHANNEL_ID)
        user = interaction.user

        if user.id in open_tickets:
            return await interaction.response.send_message(
                "❌ Você já tem um ticket aberto.",
                ephemeral=True
            )

        escolha = self.values[0]

        nome_thread = f"{escolha} ✦ {user.name} ✦ {user.id}"

        thread = await canal.create_thread(name=nome_thread)
        await thread.add_user(user)

        open_tickets[user.id] = thread.id

        # =========================
        # MENSAGEM EFÊMERA (OBRIGATÓRIO)
        # =========================

        await interaction.response.send_message(
            f"🎟️ Ticket aberto com sucesso!! 🌙\nEste é seu ticket ➡️ {thread.mention}",
            ephemeral=True
        )

        # =========================
        # DENÚNCIA
        # =========================
        if escolha == "Denúncia":

            await thread.send(f"<@&{STAFF_ROLE_ID}>")

            await thread.send(embed=ticket_embed(
                "⚒️ Denúncia",
                "Envie provas do ocorrido e aguarde a staff."
            ))

        # =========================
        # SUPORTE (ATUALIZADO)
        # =========================
        elif escolha == "Suporte":

            await thread.send(f"<@&{STAFF_ROLE_ID}>")

            await thread.send(embed=ticket_embed(
                "<:logodc:1520533477613895802> Suporte",
                """Seja bem vindo ao ticket de suporte!!

Aqui você terá acesso a:
• Tirar dúvidas
• Reportar bugs
• Ser guiado

Tenha calma e aguarde a staff te atender!"""
            ))

        # =========================
        # PARCERIA
        # =========================
        elif escolha == "Parceria":

            await thread.send(f"<@{OWNER_ID}>")

            await thread.send(embed=ticket_embed(
                "⭐ Parceria",
                "Aguarde o dono avaliar sua parceria."
            ))

        # =========================
        # TORNAR STAFF (REDIRECIONA)
        # =========================
        elif escolha == "Tornar Staff":

            await thread.send(embed=ticket_embed(
                "👮 Tornar Staff",
                f"Para solicitar staff, preencha o formulário:\n{FORM_STAFF}"
            ))

# =========================
# VIEW (CONTAINER V2)
# =========================

class TicketView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        container = discord.ui.Container()

        container.add_item(
            discord.ui.TextDisplay(
"""# MOON SOCIETY  | 🌙
Seja bem-vindo(a) a central de tickets da moon society 🌙  

> Use pra fazer denúncias e fazer  
> perguntas sobre o servidor.  

> Por favor, não crie tickets caso não for  
> um dos motivos abaixo:  

> • Fazer denúncias  
> • Pedir suporte  
> • Fazer parceria  
> • se tornar staff  

Caso não for nenhum desses motivos, NÃO abra o ticket, pois, você será sujeito a uma punição. 💫"""
            )
        )

        container.add_item(discord.ui.Separator())

        row = discord.ui.ActionRow()
        row.add_item(TicketSelect())

        container.add_item(row)

        self.add_item(container)

# =========================
# ASSUMIR / FECHAR
# =========================

class TicketActions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Assumir", style=discord.ButtonStyle.success)
    async def assumir(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed = ticket_embed(
            "📌 Ticket Assumido",
            f"O ticket foi assumido por {interaction.user.mention}🌙\n> - tenha respeito e cordialidade"
        )

        await interaction.channel.send(embed=embed)

        await interaction.response.send_message("Assumido.", ephemeral=True)

    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger)
    async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.channel.send("🔒 Fechando ticket...")

        await interaction.channel.delete()

# =========================
# PAINEL
# =========================

@bot.command()
async def painel(ctx):
    await ctx.send(view=TicketView())

# =========================
# READY
# =========================

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    print(f"Logado como {bot.user}")

# =========================
# START
# =========================

bot.run(os.getenv("DISCORD_TOKEN"))
