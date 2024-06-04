import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="about", description="Shows some info and stats about the bot")
async def about_command(interaction: discord.Interaction):
    emb = discord.Embed(title="About Supercord Bot", description="Supercord is the first and largest yet unofficial discord server for the game known as **florr.io**.\n\nThe Supercord bot is the main bot that not just operates supercord, **but also operates Chaoscord and Superiorcord!** Supercord bot provides many free features to everyone including build optimizer, DPS calculator, crafting rate guesser, 60 to 10s super spawn pings and minigames as well as we give premium features to supporters (patrons and boosters) like **premium build optimizer, more winning in minigames and 0s delay (instant) super spawn pings!**\n\n**Links:**\n1. [Patron Link](https://patreon.com/superiorcord)\n2. [Invite your friends](https://discord.gg/super-florr-players-1079971830384828497)\n\n")
    emb.set_author(name="Cryptverse (@cryptverse)", icon_url="https://cdn.discordapp.com/avatars/349495483183529985/a_f8b1ada7d2becaf567a9abc21ac263aa?size=1024")
    emb.set_footer(text="Made with 💖 and Discord.py by Cryptverse", icon_url="https://i.ibb.co/Hddhxs3/discord-py-logo.png")
    servers_count = len(client.guilds)
    emb.add_field(name="Servers", value=f"In {str(servers_count)} servers")
    await interaction.response.send_message(embed=emb)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

if __name__ == '__main__':
    client.run(TOKEN)