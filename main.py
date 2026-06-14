import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# CONFIG
# =========================

TICKET_CHANNEL_ID = 1498477718499492069
STAFF_ROLE_ID = 1498522857356132465
OWNER_ID = 1496941098009100519

ticket_creator = {}


# =========================
# SELECT MENU
# =========================

class TicketSelect(discord.ui.Select):

    def __init__(self):
        options = [
            discord.SelectOption(label="Denúncias", emoji="⚒️"),
            discord.SelectOption(label="Dúvidas", emoji="❓"),
            discord.SelectOption(label="Parceria", emoji="⭐"),
        ]

        super().__init__(
            placeholder="Escolha o motivo do ticket...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        if interaction.channel.id != TICKET_CHANNEL_ID:
            return await interaction.response.send_message(
                "Use o canal oficial de tickets.",
                ephemeral=True
            )

        tipo = self.values[0]
        user = interaction.user
        guild = interaction.guild

        staff_role = guild.get_role(STAFF_ROLE_ID)
        owner = await bot.fetch_user(OWNER_ID)

        # =========================
        # CRIA THREAD
        # =========================

        thread = await interaction.channel.create_thread(
            name=f"{tipo} ✦ {user.name} ✦ {user.id}",
            type=discord.ChannelType.private_thread
        )

        ticket_creator[thread.id] = user.id

        await thread.add_user(user)

        # =========================
        # PERMISSÕES
        # =========================

        if tipo in ["Denúncias", "Dúvidas"]:
            await thread.send(f"{staff_role.mention}")

        elif tipo == "Parceria":
            await thread.add_user(owner)
            await thread.send(f"{owner.mention}")

        # =========================
        # MENSAGENS DO TICKET
        # =========================

        if tipo == "Denúncias":
            msg = (
                "🤠 | Alguém da equipe staff logo virá atender.\n"
                "Por favor, tenha cordialidade e respeito pelos nossos staffs.\n\n"
                "Tenha os seguintes itens em mãos:\n"
                "- Prints do ocorrido\n"
                "- Nome do infrator (ou ID)"
            )

        elif tipo == "Dúvidas":
            msg = (
                "😃 | Alguém da equipe staff virá atender.\n"
                "Tenha cordialidade e respeito.\n"
                "Explique sua dúvida com clareza."
            )

        else:
            msg = (
                "😄 | O dono do servidor logo virá.\n\n"
                "Tenha paciência e lembre-se:\n"
                "- mínimo 700 membros\n"
                "- público ativo\n"
                "- sem NSFW ou +18"
            )

        await thread.send(msg, view=TicketControls())

        await interaction.response.send_message(
            f"Ticket criado: {thread.mention}",
            ephemeral=True
        )


# =========================
# PAINEL
# =========================

class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


# =========================
# CONTROLES DO TICKET
# =========================

class TicketControls(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(label="Assumir", style=discord.ButtonStyle.gray)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.channel.send(
            f"🎯 Ticket assumido por {interaction.user.mention}"
        )

        try:
            await interaction.user.send(
                f"Você assumiu o ticket: {interaction.channel.name}"
            )
        except:
            pass

        await interaction.response.send_message("Ticket assumido!", ephemeral=True)


    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

        thread = interaction.channel
        user_id = ticket_creator.get(thread.id)

        await thread.send("🔒 Ticket fechado.")

        try:
            user = await bot.fetch_user(user_id)

            await user.send(
                f"Seu ticket foi fechado: {thread.name}",
                view=ReopenView(thread.id)
            )
        except:
            pass

        await thread.edit(archived=True, locked=True)

        await interaction.response.send_message("Fechado!", ephemeral=True)


# =========================
# REABRIR TICKET
# =========================

class ReopenView(discord.ui.View):

    def __init__(self, thread_id):
        super().__init__(timeout=None)
        self.thread_id = thread_id


    @discord.ui.button(label="Reabrir Ticket", style=discord.ButtonStyle.green)
    async def reopen(self, interaction: discord.Interaction, button: discord.ui.Button):

        thread = await bot.fetch_channel(self.thread_id)

        await thread.edit(archived=False, locked=False)

        await thread.send(f"🔓 Ticket reaberto por {interaction.user.mention}")

        await interaction.response.send_message(
            "Ticket reaberto com sucesso!",
            ephemeral=True
        )


# =========================
# COMANDO PAINEL
# =========================

@bot.command()
async def ticket(ctx):

    embed = discord.Embed(
        title="# MOON SOCIETY #",
        description=
        "Seja bem-vindo(a) a central de tickets.\n\n"
        "Use pra fazer denúncias e fazer perguntas sobre o servidor.\n"
        "Por favor, não crie tickets caso não for um dos motivos abaixo:\n"
        "- Fazer denúncias ;\n"
        "- Tirar dúvidas;\n"
        "- Fazer parceria.\n\n"
        "Caso não for nenhum desses motivos, **NÃO** abra o ticket, pois, você será sujeito a uma punição.",
        color=discord.Color.blurple()
    )

    await ctx.send(embed=embed, view=TicketPanel())


# =========================
# BOT ONLINE
# =========================

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")


bot.run(os.getenv("DISCORD_TOKEN"))
