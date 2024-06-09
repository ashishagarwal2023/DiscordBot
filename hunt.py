import os, random
import datetime
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)  


@tree.command(name="hunt", description="Hunt to earn coins!")
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild.id, i.user.id))
async def hunt_command(interaction):
  emb = discord.Embed(description=f"You are currently hunting", color=discord.Color.yellow())
  await interaction.response.send_message(embed=emb)
  success = random.choices([True, False], weights=[0.8, 0.2])[0]
  if success:
    coins = random.randint(1, 5)
    emb = discord.Embed(description=f"You were hunting, you found {coins}<:Supercoin:1200278703805050981> !", color=discord.Color.green())
  else:
    loss = random.randint(5, 20)
    emb = discord.Embed(description=f"You went hunting and your coin sack got caught on a cactus spine and {loss}<:Supercoin:1200278703805050981> fell out", color=discord.Color.red())
  coins = random.randint(1, 5)
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
