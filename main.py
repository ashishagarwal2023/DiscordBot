import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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
            emb = discord.Embed(title="Challenge Confirmed", description=f"Challenge accepted! {self.challenger.mention}, it's your turn!", color=discord.Color.green())
            view = GameView(self.opponent, self.challenger)
            await interaction.response.edit_message(embed=emb, content=self.challenger.mention, view=view)
            message = await interaction.original_response()
            view.message = message
            await message.edit(embed=emb, content=self.challenger.mention, view=view)
        else:
            await interaction.response.send_message("This is not your game.", ephemeral=True)
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline_callback(self, interaction, button):
        if interaction.user == self.opponent:
            self.finished = True
            emb = discord.Embed(title="Challenge Declined", description=f"{self.opponent.mention} declined {self.challenger.mention}'s challenge in Rock Paper Scissors.", color=discord.Color.red())
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

# Game View

choices = ["Rock", "Paper", "Scissors"]
emojis = {
    "Rock": "🪨",
    "Paper": "📄",
    "Scissors": "✂️"
}

class GameView(discord.ui.View):
    def __init__(self, opponent, challenger):
        super().__init__(timeout=30)
        self.opponent = opponent
        self.challenger = challenger
        self.chance = challenger
        self.chances = [None, None]
        self.finished = False

    async def on_timeout(self):
        if self.finished:
            return
        emb = discord.Embed(title="Challenge Expired", description=f"This challenge has expired automatically.", color=discord.Color.dark_gray())
        await self.message.edit(view=ExpiredGame(), embed=emb, content="")

    async def end(self, interaction):
        self.finished = True
        result_embed = discord.Embed(title="Rock Paper Scissors Result", color=0x00ff00)
        result_embed.add_field(name=self.challenger.name, value=f"{self.chances[0]} {emojis[self.chances[0]]}")
        result_embed.add_field(name=self.opponent.name, value=f"{self.chances[1]} {emojis[self.chances[1]]}")
        winner = win(self.chances[0], self.chances[1])
        if winner == None:
            result_embed.add_field(name="Result", value="It's a draw!", inline=False)
        elif winner == 1:
            result_embed.add_field(name="Winner", value=f"{self.challenger.mention} wins!", inline=False)
        else:
            result_embed.add_field(name="Winner", value=f"{self.opponent.mention} wins!", inline=False)
        await interaction.response.edit_message(embed=result_embed, content="The game has ended!", view=None)

    async def make_choice(self, interaction, choice, emoji):
        if self.finished:
            await interaction.response.send_message("This game has already ended!", ephemeral=True)
        else:
            if interaction.user == self.chance:
                if self.chance == self.challenger:
                    self.chances[0] = choice
                    self.chance = self.opponent
                else:
                    self.chances[1] = choice
                    self.chance = self.challenger
                    await self.end(interaction)
                    return
                emb = discord.Embed(title="Challenge Confirmed", description=f"{self.opponent.mention}, it's your turn!", color=discord.Color.green())
                await interaction.response.edit_message(content=f"{self.opponent.mention}'s turn!", embed=emb)
            else:
                await interaction.response.send_message("This is not your turn.", ephemeral=True)

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.primary, emoji="🪨")
    async def rock_callback(self, interaction, button):
        await self.make_choice(interaction, "Rock", "🪨")

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.primary, emoji="📄")
    async def paper_callback(self, interaction, button):
        await self.make_choice(interaction, "Paper", "📄")

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.primary, emoji="✂️")
    async def scissor_callback(self, interaction, button):
        await self.make_choice(interaction, "Scissors", "✂️")




# Win check
def win(a, b):
    if a == b:
        return None
    if (a == "Rock" and b == "Scissors") or \
       (a == "Scissors" and b == "Paper") or \
       (a == "Paper" and b == "Rock"):
        return 1
    return 2


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
        
    @discord.ui.button(label="Rock", style=discord.ButtonStyle.gray, emoji="🪨", disabled=True)
    async def rock_callback(self, interaction, button):
        pass

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.gray, emoji="📄", disabled=True)
    async def paper_callback(self, interaction, button):
        pass

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.gray, emoji="✂️", disabled=True)
    async def scissor_callback(self, interaction, button):
        pass

@tree.command(
    name="rps",
    description="Play a game of RPS!",
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
    emb = discord.Embed(title="Pending Confirmation", description=f"{interaction.user.mention} is challenging {opponent.mention} in Rock Paper Scissors!", color=discord.Color.yellow())

    view = PendingView(opponent, interaction.user)
    await interaction.response.send_message(embed=emb, content=opponent.mention, view=view)
    message = await interaction.original_response()
    view.message = message

    await message.edit(embed=emb, content=opponent.mention, view=view)

@tree.command(name="ping", description="Check the bot's latency.",)
async def ping(interaction: discord.Interaction):
    """Pong!"""
    ping_message = f"Ping!"
    if interaction.user.id == 1153023901203447940:
        ping_delay = round(client.latency * 1000)
        ping_message = f"Ping: {ping_delay}ms"
    await interaction.response.send_message(content=ping_message)

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)
