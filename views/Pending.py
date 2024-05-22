import discord
from .Game import GameView
from .Expired import ExpiredPending

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
            emb = discord.Embed(title="Challenge Confirmed", description=f"Challenge accepted! {self.challenger.mention}, it's your turn!", color=discord.Color.green())
            self.finished = True
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