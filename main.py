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
CATEGORY_ID = 1498477718499492064
STAFF_ROLE_ID = 1498522857356132465
OWNER_ID = 1496941098009100519

ticket_creator = {}


# =========================
# SELECT MENU
# =========================

class TicketSelect(discord.ui.Select):

    def __init__(self):
        options = [
            discord.SelectOption(label="Denúncia", emoji="🤠"),
            discord.SelectOption(label="Dúvidas", emoji="😃"),
            discord.SelectOption(label="Parceria", emoji="😄"),
        ]

        super().__init__(
            placeholder="Escolha o tipo de ticket...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        if interaction.channel.id != TICKET_CHANNEL_ID:
            return await interaction.response.send_message(
                "Use o painel oficial de tickets no canal correto.",
                ephemeral=True
            )

        tipo = self.values[0]
        user = interaction.user
        guild = interaction.guild

        staff_role = guild.get_role(STAFF_ROLE_ID)
        owner = await bot.fetch_user(OWNER_ID)

        thread = await interaction.channel.create_thread(
            name=f"{tipo} ✦ {user.name} ✦ {user.id}",
            type=discord.ChannelType.private_thread
        )

        ticket_creator[thread.id] = user.id

        await thread.add_user(user)

        # STAFF / OWNER
        if tipo in ["Denúncia", "Dúvidas"]:
            await thread.send(f"{staff_role.mention}")

        elif tipo == "Parceria":
            await thread.add_user(owner)
            await thread.send(f"{owner.mention}")

        # MENSAGENS
        embed = discord.Embed(
            title=f"🎫 Ticket de {tipo}",
            color=discord.Color.blurple()
        )

        if tipo == "Denúncia":
            embed.description = (
                "🤠 | Staff irá atender em breve.\n\n"
                "Tenha respeito e cordialidade.\n\n"
                "**Itens:**\n"
                "- Prints\n"
                "- ID ou nome do infrator"
            )

        elif tipo == "Dúvidas":
            embed.description = (
                "😃 | Staff irá te atender em breve.\n"
                "Explique sua dúvida com clareza."
            )

        else:
            embed.description = (
                "😄 | Dono irá analisar sua parceria.\n\n"
                "**Requisitos:**\n"
                "- 700+ membros\n"
                "- público ativo\n"
                "- sem NSFW"
            )

        await thread.send(embed=embed, view=TicketControls())

        await interaction.response.send_message(
            f"🎫 Ticket criado: {thread.mention}",
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
# CONTROLES
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
                f"Seu ticket `{thread.name}` foi fechado.\nDeseja reabrir?",
                view=ReopenView(thread.id)
            )
        except:
            pass

        await thread.edit(archived=True, locked=True)

        await interaction.response.send_message("Ticket fechado!", ephemeral=True)


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
        description=(
            "Bem-vindo à central de tickets.\n\n"
            "Use apenas para:\n"
            "- Denúncia\n"
            "- Dúvidas\n"
            "- Parceria\n\n"
            "Escolha abaixo o tipo de atendimento."
        ),
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
