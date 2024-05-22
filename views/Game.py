from lib.win import win
import discord
from .Expired import ExpiredGame

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
