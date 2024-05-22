import discord

# client_id = 1241770339998892053

def check_opponent(func):
    async def wrapper(interaction, opponent: discord.Member):
        if opponent.id == interaction.client.user.id:
            await interaction.response.send_message("You cannot challenge me!", ephemeral=True)
        elif opponent.id == interaction.user.id:
            await interaction.response.send_message("You cannot challenge yourself!", ephemeral=True)
        elif opponent.bot:
            await interaction.response.send_message("You cannot challenge a bot!", ephemeral=True)
        else:
            await func(interaction, opponent)
    return wrapper