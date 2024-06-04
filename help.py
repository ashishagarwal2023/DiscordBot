import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="help", description="Helpful information")
async def help_command(interaction: discord.Interaction):
    desc = "Use the `.help <command/category>` for more information.\n\n"
    desc += "**Coins (Supercoins)**\n"
    desc += "By reporting ultras or supers, playing minigames and particpating in events, you can get coins to purchase items from our shop such as roles, XP and roles! Current rates: 15-30 coins per ultra, 250-500 per super. *Supercoins is the supercord's currency.*\n"
    desc += "> `.bet <dice bet> <supercoins>`: Bet on a dice roll, if you win, you get your supercoins trippled.\n> `/shop`: view the shop\n> `/coins`: check your balance\n> `/rps <player> [wager]`: play rock paper scissors game with someone, optionally with a wager of supercoins\n\n"
    desc += "**Leveling**\n"
    desc += "You earn levels by collecting XP. XP can be collected by chatting or bought from shop.\n> `.lvl`: know your level\n> `.lb`: get the level leaderboard\n> `.rz`: get the leaderboard excluding patrons, boosters and anyone that is not a commander\n\n"
    desc += "**Premium**\n> `.claim`: claim your daily 200-300 supercoins\n> `.next_claim_time`: know the next time when you can claim your next daily supercoins\n\n"
    desc += "**Spawns**\n> `.n <mob>`: report a NA/US server super\n> `.e <mob>`: report a EU server super\n> `.a <mob>`: report a AS server super\n> `.s <mob> <server>`: report a super for the given server\n> `.who <mob> <server>`: know who last reported the provided super mob in provided server\n> `.when <mob>`: predict a super mob spawn\n> `.test <mob>`: test a mob\n> `.reps`: see how many reports of super mobs you did\n> `.accuracy <mob>`: view report accuracy for a mob\n\n"
    desc += "**Utillity**\n> `.dps <flags>`: calculate single target dps\n> `.ping`: Pong!\n> `.drops`: get the expected number of drops for a number of mobs\n> `.opt`: optimize a build\n> `/craftingchance <amount> [from_rarity]`: get the chance of crafting a certain rarity item"
    emb = discord.Embed(title="Supercord Bot Help", description=desc, color=discord.Color.green())
    emb.set_thumbnail(url="https://cdn.discordapp.com/avatars/1132362368979050546/6a905f28ed0c9640efb25483b30c9e0b.webp?size=1024&format=webp&width=0&height=256")
    await interaction.response.send_message(embed=emb)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)
