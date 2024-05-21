from discord.ext import commands

class EmptyCog(commands.GroupCog, group_name='emptytest'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="hello")
  async def hello_command(self, interaction):
    await interaction.response.send_message("Hello!")

async def setup(bot: commands.Bot):
  await bot.add_cog(EmptyCog(bot))
