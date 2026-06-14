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
panel_sent = False


# =========================
# PAINEL V2 (SEM EMBED)
# =========================

def panel_v2():
    return {
        "type": 17,
        "accent_color": 0x2b2d31,
        "components": [

            {
                "type": 10,
                "content": """# MOON SOCIETY #
Seja bem-vindo(a) à central de tickets.

Use apenas para:
- Denúncias
- Dúvidas
- Parceria

Não crie tickets sem motivo válido.
"""
            },

            {
                "type": 1,
                "components": [
                    {
                        "type": 3,
                        "custom_id": "ticket_select",
                        "placeholder": "Escolha o tipo de ticket...",
                        "options": [
                            {"label": "Denúncias", "value": "Denúncias", "emoji": {"name": "🤠"}},
                            {"label": "Dúvidas", "value": "Dúvidas", "emoji": {"name": "😃"}},
                            {"label": "Parceria", "value": "Parceria", "emoji": {"name": "😄"}}
                        ]
                    }
                ]
            }
        ]
    }


# =========================
# INTERAÇÕES V2
# =========================

@bot.event
async def on_interaction(interaction: discord.Interaction):

    if interaction.type != discord.InteractionType.component:
        return

    data = interaction.data
    cid = data.get("custom_id")

    # =========================
    # SELECT TICKET
    # =========================

    if cid == "ticket_select":

        tipo = data["values"][0]
        user = interaction.user
        guild = interaction.guild

        staff = guild.get_role(STAFF_ROLE_ID)
        owner = await bot.fetch_user(OWNER_ID)

        thread = await interaction.channel.create_thread(
            name=f"{tipo} ✦ {user.name} ✦ {user.id}",
            type=discord.ChannelType.private_thread
        )

        ticket_creator[thread.id] = user.id

        await thread.add_user(user)

        if tipo in ["Denúncias", "Dúvidas"]:
            await thread.send(f"{staff.mention}")
        else:
            await thread.add_user(owner)
            await thread.send(f"{owner.mention}")

        if tipo == "Denúncias":
            msg = "⚒️ Staff irá atender. Tenha prints e ID."
        elif tipo == "Dúvidas":
            msg = "❓ Staff irá te ajudar em breve."
        else:
            msg = "⭐ Dono irá analisar parceria."

        await thread.send(msg, components=ticket_controls())

        await interaction.response.send_message(
            f"Ticket criado: {thread.mention}",
            ephemeral=True
        )

    # =========================
    # BOTÕES
    # =========================

    elif cid == "claim_ticket":

        await interaction.channel.send(
            f"🎯 Ticket assumido por {interaction.user.mention}"
        )

        await interaction.response.send_message("Assumido!", ephemeral=True)


    elif cid == "close_ticket":

        thread = interaction.channel
        user_id = ticket_creator.get(thread.id)

        await thread.send("🔒 Ticket fechado.")
        await thread.edit(archived=True, locked=True)

        try:
            user = await bot.fetch_user(user_id)
            await user.send("Seu ticket foi fechado. Deseja reabrir?")
        except:
            pass

        await interaction.response.send_message("Fechado!", ephemeral=True)


    elif cid.startswith("reopen_"):

        thread_id = int(cid.split("_")[1])

        thread = await bot.fetch_channel(thread_id)

        await thread.edit(archived=False, locked=False)

        await thread.send(f"🔓 Ticket reaberto por {interaction.user.mention}")

        await interaction.response.send_message("Reaberto!", ephemeral=True)


# =========================
# BOTÕES V2
# =========================

def ticket_controls():

    return [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": 2,
                    "label": "Assumir",
                    "custom_id": "claim_ticket"
                },
                {
                    "type": 2,
                    "style": 4,
                    "label": "Fechar",
                    "custom_id": "close_ticket"
                }
            ]
        }
    ]


# =========================
# AUTO PAINEL
# =========================

@bot.event
async def on_ready():
    global panel_sent

    print(f"Logado como {bot.user}")

    if panel_sent:
        return

    channel = bot.get_channel(TICKET_CHANNEL_ID)

    if channel:
        await channel.send(
            content=None,
            embeds=None,
            components=[panel_v2()],
            flags=32768
        )

    panel_sent = True


# =========================
# START
# =========================

bot.run(os.getenv("DISCORD_TOKEN"))
