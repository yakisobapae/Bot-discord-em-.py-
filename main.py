import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# =========================
# CONTROLE DE TICKETS (ANTI DUPLO)
# =========================
active_tickets = {}

# =========================
# BOTÕES DO TICKET (V2 STYLE)
# =========================

class TicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🕐 Assumir", style=discord.ButtonStyle.primary)
    async def assumir(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.channel.send(f"👮 {interaction.user.mention} assumiu o ticket.")
        await interaction.response.send_message("Ticket assumido.", ephemeral=True)

    @discord.ui.button(label="🗑 Fechar", style=discord.ButtonStyle.danger)
    async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_id = interaction.user.id

        if user_id in active_tickets:
            active_tickets.pop(user_id, None)

        await interaction.channel.send(f"🔒 Ticket fechado por {interaction.user.mention}")
        await interaction.channel.edit(archived=True, locked=True)

        await interaction.response.send_message("Ticket fechado.", ephemeral=True)

    @discord.ui.button(label="🔓 Reabrir", style=discord.ButtonStyle.success)
    async def reabrir(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.channel.edit(archived=False, locked=False)
        await interaction.channel.send(f"🔓 Ticket reaberto por {interaction.user.mention}")

        await interaction.response.send_message("Ticket reaberto.", ephemeral=True)


# =========================
# SELECT MENU
# =========================

class TicketSelect(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label="Denúncia", emoji="⚒️"),
            discord.SelectOption(label="Dúvidas", emoji="❓"),
            discord.SelectOption(label="Parceria", emoji="⭐")
        ]

        super().__init__(
            placeholder="➡️ Escolha uma opção",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        # ❌ ANTI MULTI TICKET
        if user_id in active_tickets:
            return await interaction.response.send_message(
                "❌ Você já tem um ticket aberto.",
                ephemeral=True
            )

        STAFF_ROLE_ID = 1498522857356132465
        OWNER_ID = 1496941098009100519
        TICKET_CHANNEL_ID = 1498477718499492069

        canal = interaction.guild.get_channel(TICKET_CHANNEL_ID)

        escolha = self.values[0]

        nome_thread = f"{escolha} ✦ {interaction.user.name} ✦ {interaction.user.id}"

        thread = await canal.create_thread(name=nome_thread)

        active_tickets[user_id] = thread.id

        await thread.add_user(interaction.user)

        # =========================
        # MENSAGENS POR TIPO
        # =========================

        if escolha == "Denúncia":
            await thread.send(f"<@&{STAFF_ROLE_ID}>")
            await thread.send("""
⚒️ Denúncia

🤠 Staff irá te atender.

• Prints
• Nome/ID do acusado
""")

        elif escolha == "Dúvidas":
            await thread.send(f"<@&{STAFF_ROLE_ID}>")
            await thread.send("""
❓ Dúvidas

😃 Staff irá responder sua dúvida.
""")

        elif escolha == "Parceria":
            await thread.send(f"<@{OWNER_ID}>")
            await thread.send("""
⭐ Parceria

😄 Dono irá analisar.

• 700+ membros
• Ativo
• Sem NSFW
""")

        # BOTÕES STYLE BLOX WORLD
        await thread.send(view=TicketButtons())

        # RESPOSTA BONITA
        await interaction.response.send_message(
            f"""
# 🌙 MOON SOCIETY

✅ Seu ticket de **{escolha}** foi criado com sucesso.

🎫 Ticket:
{thread.mention}

💫 Em breve alguém da equipe irá atendê-lo.
""",
            ephemeral=True
        )


# =========================
# PAINEL (BLOX WORLD STYLE)
# =========================

@bot.command()
async def painel(ctx):

    view = discord.ui.LayoutView()
    container = discord.ui.Container()

    container.add_item(
        discord.ui.TextDisplay("# 🌙 MOON SOCIETY")
    )

    container.add_item(
        discord.ui.TextDisplay("""
Seja bem-vindo(a) a central de tickets 🌙

> Escolha uma opção abaixo:

⚒️ Denúncia  
❓ Dúvidas  
⭐ Parceria  

Não crie tickets sem motivo válido.
""")
    )

    container.add_item(discord.ui.Separator())

    row = discord.ui.ActionRow()
    row.add_item(TicketSelect())

    container.add_item(row)

    view.add_item(container)

    await ctx.send(view=view)


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
