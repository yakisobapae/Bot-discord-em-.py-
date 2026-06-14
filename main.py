import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# CONFIG
# =========================

TICKET_CHANNEL_ID = 1498477718499492069
LOG_CHANNEL_ID = 1498477718499492069  # pode trocar depois
STAFF_ROLE_ID = 1498522857356132465
OWNER_ID = 1496941098009100519

tickets = {}


# =========================
# COMPONENTS V2 PAINEL
# =========================

def panel_v2():
    return {
        "type": 17,
        "accent_color": 0x2b2d31,
        "components": [

            {
                "type": 10,
                "content": """# MOON SOCIETY #
Seja bem-vindo(a) a central de tickets.

Use pra:
- Denúncias
- Dúvidas
- Parcerias

Não abra tickets sem motivo válido."""
            },

            {
                "type": 1,
                "components": [
                    {
                        "type": 3,
                        "custom_id": "ticket_select",
                        "placeholder": "Escolha o tipo de ticket...",
                        "options": [
                            {"label": "Denúncias", "value": "Denúncias", "emoji": {"name": "⚒️"}},
                            {"label": "Dúvidas", "value": "Dúvidas", "emoji": {"name": "❓"}},
                            {"label": "Parceria", "value": "Parceria", "emoji": {"name": "⭐"}}
                        ]
                    }
                ]
            }
        ]
    }


# =========================
# BOTÕES V2 (TICKET)
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
# INTERAÇÕES
# =========================

@bot.event
async def on_interaction(interaction: discord.Interaction):

    if interaction.type != discord.InteractionType.component:
        return

    data = interaction.data
    cid = data.get("custom_id")


    # =========================
    # SELECT
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

        tickets[thread.id] = user.id

        await thread.add_user(user)

        if tipo in ["Denúncias", "Dúvidas"]:
            await thread.send(f"{staff.mention}")
        else:
            await thread.add_user(owner)
            await thread.send(f"{owner.mention}")

        await thread.send(
            f"🎫 Ticket de {tipo} criado.",
            components=ticket_controls()
        )

        await interaction.response.send_message(
            f"Ticket criado: {thread.mention}",
            ephemeral=True
        )


    # =========================
    # ASSUMIR TICKET
    # =========================

    elif cid == "claim_ticket":

        await interaction.channel.send(
            f"``🎯 Ticket assumido por {interaction.user.mention}``"
        )

        await interaction.response.send_message("Assumido!", ephemeral=True)


    # =========================
    # FECHAR TICKET
    # =========================

    elif cid == "close_ticket":

        thread = interaction.channel
        user_id = tickets.get(thread.id)

        await thread.send("🔒 Ticket fechado.")

        try:
            user = await bot.fetch_user(user_id)

            await user.send(
                f"Seu ticket foi fechado: {thread.name}",
                components=[
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "style": 3,
                                "label": "Reabrir Ticket",
                                "custom_id": f"reopen_{thread.id}"
                            }
                        ]
                    }
                ]
            )
        except:
            pass

        await thread.edit(archived=True, locked=True)

        await interaction.response.send_message("Fechado!", ephemeral=True)


    # =========================
    # REABRIR TICKET
    # =========================

    elif cid.startswith("reopen_"):

        thread_id = int(cid.split("_")[1])

        thread = await bot.fetch_channel(thread_id)

        await thread.edit(archived=False, locked=False)

        await thread.send(f"🔓 Ticket reaberto por {interaction.user.mention}")

        await interaction.response.send_message("Reaberto!", ephemeral=True)


# =========================
# COMANDO PAINEL
# =========================

@bot.command()
async def ticket(ctx):

    await ctx.send(
        components=[panel_v2()]
    )


# =========================
# START
# =========================

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")


bot.run(os.getenv("DISCORD_TOKEN"))
