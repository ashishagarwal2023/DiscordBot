import os
import discord
from discord import app_commands
from dotenv import load_dotenv

from views.Pending import PendingView
from lib.check import check_opponent

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name="rps",
    description="Play a game of RPS!",
)
@check_opponent
async def rps_command(interaction, opponent: discord.Member):
    emb = discord.Embed(title="Pending Confirmation", description=f"{interaction.user.mention} is challenging {opponent.mention} in Rock Paper Scissors!", color=discord.Color.yellow())
    await interaction.response.send_message(embed=emb, content=opponent.mention, view=PendingView(opponent, interaction.user))

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

if __name__ == '__main__':
    client.run(TOKEN)