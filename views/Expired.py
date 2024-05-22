import discord

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
