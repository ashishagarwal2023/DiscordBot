import os, random
import datetime
from typing import Optional
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client) 

mobs = ["Jellyfish", "Starfish", "Sponge", "Shell", "Crab", "Bubble", "Leech"]
petals = ["Bubble", "Air", "Sand", "Claw", "Jelly", "Lightning", "Fangs", "Faster", "Magnet", "Shell", "Pearl", "Sponge", "Starfish", "Salt"]

def cooldown_for_everyone_but_me(interaction: discord.Interaction) -> Optional[app_commands.Cooldown]:
    if interaction.user.id == 349495483183529985:
        return None
    return app_commands.Cooldown(1, 10.0)


@tree.command(name="fish", description="Go fishing to earn coins!")
@app_commands.checks.dynamic_cooldown(cooldown_for_everyone_but_me)
async def fish_command(interaction):
  petal = random.choice(petals).lower()
  emb = discord.Embed(description=f"You are currently fishing", color=discord.Color.yellow())
  await interaction.response.send_message(embed=emb)
  success = random.choices([True, False], weights=[0.8, 0.2])[0]
  if success:
    emb = discord.Embed(description=f"You went fishing and caught a {petal}!", color=discord.Color.green())
  else:
    emb = discord.Embed(description=f"A jellyfish electrocuted you to death.", color=discord.Color.red())
  await interaction.edit_original_response(embed=emb)

@fish_command.error
async def fish_on_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
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
