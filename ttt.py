import os
import random
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

x = "X"
o = "O"
b = " "

possible_color = discord.ButtonStyle.primary
opponent_color = discord.ButtonStyle.red
challenger_color = discord.ButtonStyle.green

class TicTacToe(discord.ui.View):
  def __init__(self, opponent, challenger):
     self.opponent = opponent
     self.challenger = challenger
     self.turn = random.choice([self.opponent, self.challenger])
     self.board = [b, b, b, b, b, b, b, b, b]
    
  id = 0
  letter = x
  @discord.ui.button(label=letter, style=possible_color, row=0, custom_id=f"{letter}{id}")
  async def x0_callback(self, interaction, button):
     pass
  
  
  id = 1
  letter = o
  @discord.ui.button(label=letter, style=possible_color, row=0, custom_id=f"{letter}{id}")
  async def o1_callback(self, interaction, button):
     pass
  
  
  id = 2
  letter = x
  @discord.ui.button(label=letter, style=possible_color, row=0, custom_id=f"{letter}{id}")
  async def x2_callback(self, interaction, button):
     pass
  
  
  id = 3
  letter = o
  @discord.ui.button(label=letter, style=possible_color, row=1, custom_id=f"{letter}{id}")
  async def o3_callback(self, interaction, button):
     pass
  
  
  id = 4
  letter = x
  @discord.ui.button(label=letter, style=possible_color, row=1, custom_id=f"{letter}{id}")
  async def x4_callback(self, interaction, button):
     pass
  
  
  id = 5
  letter = o
  @discord.ui.button(label=letter, style=possible_color, row=1, custom_id=f"{letter}{id}")
  async def o5_callback(self, interaction, button):
     pass
  
  
  id = 6
  letter = x
  @discord.ui.button(label=letter, style=possible_color, row=2, custom_id=f"{letter}{id}")
  async def x6_callback(self, interaction, button):
     pass
  
  id = 7
  letter = o
  @discord.ui.button(label=letter, style=possible_color, row=2, custom_id=f"{letter}{id}")
  async def o7_callback(self, interaction, button):
     pass
  
  id = 8
  letter = x
  @discord.ui.button(label=letter, style=possible_color, row=2, custom_id=f"{letter}{id}")
  async def x8_callback(self, interaction, button):
     pass
  
  

# Pending View
class PendingView(discord.ui.View):
    def __init__(self, opponent, challenger):
        super().__init__(timeout=30)
        self.opponent = opponent
        self.challenger = challenger
        self.finished = False

    
    async def on_timeout(self):
        if self.finished:
            return
        emb = discord.Embed(title="Challenge Expired", description=f"This challenge has expired automatically.", color=discord.Color.dark_gray())
        await self.message.edit(view=ExpiredPending(), embed=emb, content="")
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept_callback(self, interaction, button):
        if interaction.user == self.opponent:
            self.finished = True
            await interaction.response.edit_message(content="", view=TicTacToe(self.opponent, self.challenger))
        else:
            await interaction.response.send_message("This is not your game.", ephemeral=True)
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline_callback(self, interaction, button):
        if interaction.user == self.opponent:
            self.finished = True
            emb = discord.Embed(title="Challenge Declined", description=f"{self.opponent.mention} declined {self.challenger.mention}'s challenge in Tic Tac Toe", color=discord.Color.red())
            await interaction.response.edit_message(content=None, view=None, embed=emb)
        else:
            await interaction.response.send_message("This is not your game.", ephemeral=True)
    
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
    async def cancel_callback(self, interaction, button):
        if interaction.user == self.challenger:
            self.finished = True
            emb = discord.Embed(title="Challenge Cancelled", description=f"This challenge has been cancelled by {self.challenger.mention}", color=discord.Color.dark_gray())
            await self.message.edit(view=ExpiredPending(), embed=emb, content="")
            await interaction.response.send_message("Challenge cancelled.", ephemeral=True)
        else:
            await interaction.response.send_message("This is not your game.", ephemeral=True)





# Expired Views
class ExpiredPending(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=1)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.gray, disabled=True)
    async def accept_callback(self, interaction, button):
        pass
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.gray, disabled=True)
    async def decline_callback(self, interaction, button):
        pass
    
    
    @discord.ui.button(label="Cancelled", style=discord.ButtonStyle.red, disabled=True)
    async def cancel_callback(self, interaction, button):
        pass
    
class ExpiredGame(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=1)
        
    @discord.ui.button(label=x, style=discord.ButtonStyle.gray, disabled=True, row=0)
    async def x1(self, interaction, button):
      pass

    @discord.ui.button(label=o, style=discord.ButtonStyle.gray, disabled=True, row=0)
    async def o2(self, interaction, button):
      pass

    @discord.ui.button(label=x, style=discord.ButtonStyle.gray, disabled=True, row=0)
    async def x3(self, interaction, button):
      pass

    @discord.ui.button(label=o, style=discord.ButtonStyle.gray, disabled=True, row=1)
    async def o4(self, interaction, button):
      pass

    @discord.ui.button(label=x, style=discord.ButtonStyle.gray, disabled=True, row=1)
    async def x5(self, interaction, button):
      pass

    @discord.ui.button(label=o, style=discord.ButtonStyle.gray, disabled=True, row=1)
    async def o6(self, interaction, button):
      pass

    @discord.ui.button(label=x, style=discord.ButtonStyle.gray, disabled=True, row=2)
    async def x7(self, interaction, button):
      pass

    @discord.ui.button(label=o, style=discord.ButtonStyle.gray, disabled=True, row=2)
    async def o8(self, interaction, button):
      pass

    @discord.ui.button(label=x, style=discord.ButtonStyle.gray, disabled=True, row=2)
    async def x9(self, interaction, button):
      pass

@tree.command(
    name="ttt",
    description="Play a game of TTT!",
)
async def rps_command(interaction, opponent: discord.Member):
    if opponent.id == interaction.client.user.id:
      await interaction.response.send_message("You cannot challenge me!", ephemeral=True)
      return
    elif opponent.id == interaction.user.id:
      await interaction.response.send_message("You cannot challenge yourself!", ephemeral=True)
      return
    elif opponent.bot:
      await interaction.response.send_message("You cannot challenge a bot!", ephemeral=True)
      return
    emb = discord.Embed(title="Pending Confirmation", description=f"{interaction.user.mention} is challenging {opponent.mention} in Tic Tac Toe!", color=discord.Color.yellow())

    view = PendingView(opponent, interaction.user)
    await interaction.response.send_message(embed=emb, content=opponent.mention, view=view)
    message = await interaction.original_response()
    view.message = message

    await message.edit(embed=emb, content=opponent.mention, view=view)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)
