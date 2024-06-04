import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class VoteView(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=180)
    button = discord.ui.Button(label="Vote", style=discord.ButtonStyle.url, url="https://top.gg/bot/1132362368979050546")
    self.add_item(button)

@tree.command(name="vote", description="Vote for supercord bot on top.gg and earn supercoins!")
async def help_command(interaction: discord.Interaction):
    your_votes_this_month = 4
    rewards = "100-500 <:Supercoin:1200278703805050981>"
    desc = f"> Your votes this month: {your_votes_this_month}\n> Reward per vote: {rewards}\n\n**Support our bot!**\nSupport supercord and supercord bot by voting for us! You also earn supercoins when you vote for us.\n\nClick the button below to vote for us on top.gg. You can only vote once per each 12 hours!"
    emb = discord.Embed(title="Vote for Supercord Bot", description=desc, color=discord.Color.green())
    emb.set_thumbnail(url="https://cdn.discordapp.com/avatars/1132362368979050546/6a905f28ed0c9640efb25483b30c9e0b.webp?size=1024&format=webp&width=0&height=256")
    await interaction.response.send_message(embed=emb, view=VoteView())


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)
