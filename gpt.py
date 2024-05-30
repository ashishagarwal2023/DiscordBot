import os, time
import datetime
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)  


@tree.command(name="ask", description="Ask AI something")
@app_commands.checks.cooldown(1, 2, key=lambda i: (i.guild.id, i.user.id))
async def hunt_command(interaction, question: str):
  emb = discord.Embed(description=f"Generating AI response. Please wait.", color=discord.Color.blue())
  await interaction.response.send_message(embed=emb)
  emb = discord.Embed(description=f"Response generated successfully.", color=discord.Color.blue())
  emb.add_field(name="Question", value=question)
  emb.add_field(name="Response", value="Testing things to not go wrong") 
  await interaction.edit_original_response(embed=emb)

@hunt_command.error
async def hunt_on_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
   if isinstance(error, app_commands.CommandOnCooldown):
      emb = discord.Embed(
         description=f"This command has a cooldown. Retry <t:{datetime.datetime.now().timestamp() + error.retry_after:.0f}:R>", 
         color=discord.Color.magenta())
      emb.set_footer(text="Premium users get 10s cooldown. You currently have 30s cooldown.")
      await interaction.response.send_message(embeds=[emb], ephemeral=True)
   


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)
