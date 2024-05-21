import discord
from .Game import GameView

class PendingView(discord.ui.View):
    def __init__(self, opponent, challenger):
        super().__init__(timeout=60)
        self.opponent = opponent
        self.challenger = challenger

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept_callback(self, interaction, button):
        if interaction.user == self.opponent:
            emb = discord.Embed(title="Challenge Confirmed", description=f"Challenge accepted! {self.challenger.mention}, it's your turn!", color=discord.Color.green())
            await interaction.response.edit_message(content=self.challenger.mention, embed=emb, view=GameView(self.opponent, self.challenger))
        else:
            await interaction.response.send_message("This is not your game.", ephemeral=True)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline_callback(self, interaction, button):
        if interaction.user == self.opponent:
            emb = discord.Embed(title="Challenge Declined", description=f"{self.opponent.mention} declined {self.challenger.mention}'s challenge in Rock Paper Scissors.", color=discord.Color.red())
            await interaction.response.edit_message(content=None, view=None, embed=emb)
        else:
            await interaction.response.send_message("This is not your game.", ephemeral=True)
