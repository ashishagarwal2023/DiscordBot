import random

import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


class BalanceView(discord.ui.View):
   def __init__(self):
      super().__init__(timeout=45)

   @discord.ui.button(label="Help", style=discord.ButtonStyle.secondary)
   async def help_callback(self, interaction, button):
      emb = discord.Embed(title="How to earn supercoins?", description="You can earn supercoins by reporting supers, participating in events, challenges, and giveaways. You can also earn supercoins by chatting in the server and leveling up.", color=discord.Color.blurple())
      emb.add_field(name="Commands to earn coins:", value="`/hunt` - Go on a hunting expedition to find coins\n`/fish <rarity>` - Go fishing to catch coins\n`/rps <player> <wager>` - Play Rock-Paper-Scissors game to win coins\n`.bet <dice> <wager>` - Wager your coins against other players to win 3x coins if you win")
      await interaction.response.send_message(embed=emb)



@tree.command(name="coins", description="Find your supercoins balance or someone other's")
async def coins_command(interaction: discord.Interaction, user: discord.Member = None):
    random_coins = random.randint(0, 3)

    you = False
    if (interaction.user == user) or interaction.user and user == None:
        you = True
    balance_user = user or interaction.user
    title = f"{balance_user.name}'s supercoins"

    if random_coins != 0:
        if you:
          emb = discord.Embed(title=title, description=f"You have {random_coins} supercoins.", color=discord.Color.brand_green())
        else:
          emb = discord.Embed(title=title, description=f"{balance_user.name} has {random_coins} supercoins.", color=discord.Color.brand_green())
    else:
       emb = discord.Embed(title="No supercoins", description=f"{balance_user.name} has no supercoins.", color=discord.Color.brand_red())
    emb.set_footer(text=balance_user.name, icon_url=balance_user.avatar)
    await interaction.response.send_message(embed=emb, view = BalanceView())


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)
