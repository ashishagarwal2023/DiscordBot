import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="update")
async def send_update(interaction: discord.Interaction):
    await interaction.response.send_message("Join Supercord Support! https://discord.gg/xAWH3zaSFz")
    pings = "<@&1079999231420543057> <@&1088586326674251898> <@&1135358454849081366>"
    emb = discord.Embed(title="Announcement", description="We have a **new server** for support-related tasks. Join us to apply for staff, appeal NoAccess/NoSpawns and general support.\n\nBecome a <@&1230574511632547901> or <@&1083268143037829191> to get priority support and direct chat with the staff.\n\nJoin and invite your friends: [Supercord Support](https://discord.gg/xAWH3zaSFz)", color=discord.Color.green())
    emb2 = discord.Embed(title="Staff Applications are open!", description="We're looking for staff currently. Join the above server to find out more and how you can apply!", color=discord.Color.yellow())
    await interaction.followup.send(content=pings, embeds=[emb, emb2])


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

if __name__ == '__main__':
    client.run(TOKEN)