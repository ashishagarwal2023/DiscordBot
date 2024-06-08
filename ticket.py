import asyncio
import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

CATEGORY_ID = 1248283757346164882
BLACKLISTED_ID = 1248306051921739927
SUPPORT_ID = 1248305869947670579

TICK_EMOJI = "<:tick:1247281066889318401>"
X_EMOJI = "❌"
LOCK_EMOJI = "🔒"
CREATE_EMOJI = "📩"

class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Close", style=discord.ButtonStyle.secondary, emoji=LOCK_EMOJI)
    async def close_ticket(self, interaction: discord.Interaction, button):
        interaction.response.defer(ephemeral=True)
        message = interaction.message

        for member in message.channel.members:
            if discord.utils.get(member.roles, id=SUPPORT_ID) is None:
                await message.channel.set_permissions(member, view_channel=False)

        emb = discord.Embed(description=f"Ticket closed by {interaction.user.mention}", color=discord.Color.yellow())
        await message.channel.send(embed=emb, view=ClosedTicket())
        await interaction.response.send_message(ephemeral=True, content="Successfully closed ticket")

class ClosedTicket(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label="Delete?", style=discord.ButtonStyle.red)
  async def delete_ticket(self, interaction: discord.Interaction, button):
    await interaction.message.channel.delete()

class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.secondary, emoji=CREATE_EMOJI)
    async def create_ticket(self, interaction: discord.Interaction, button):
        if interaction.user.roles.count(discord.utils.get(interaction.guild.roles, id=BLACKLISTED_ID)) == 1:
            await interaction.response.send_message("You are blacklisted from creating tickets.", ephemeral=True)
            return
        category = discord.utils.get(interaction.guild.categories, id=CATEGORY_ID)
        ticket = f"ticket-{interaction.user.name.lower()}"
        if category:
            # creating channel
            await interaction.response.send_message("*:hourglass: Creating ticket channel...*", ephemeral=True)
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    embed_links=True,
                    attach_files=True,
                    add_reactions=True,
                    use_external_emojis=True,
                    use_external_stickers=True,
                    mention_everyone=True,
                    read_message_history=True,
                    use_application_commands=True,
                ),
                discord.utils.get(interaction.guild.roles, id=SUPPORT_ID): discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    embed_links=True,
                    attach_files=True,
                    add_reactions=True,
                    use_external_emojis=True,
                    use_external_stickers=True,
                    mention_everyone=True,
                    read_message_history=True,
                    use_application_commands=True,
                )
            }
            channel = await category.create_text_channel(
                ticket,
                overwrites=overwrites,
                topic=f"Ticket OP: {interaction.user.id}"
            )

            # created channel
            await (await interaction.original_response()).edit(content=f"*✔ Ticket created: {channel.mention}*")

            # now in channel
            await channel.send(f"{interaction.user.mention}")
            
            await channel.send("You have 5 minutes to **type your issue**, please be quick or the ticket will be auto-closed.")
            
            emb = discord.Embed(description="Support will be with you shortly.\n1. To close this ticket send `$close`\n2. Name your ticket with `$rename <description>`", color=discord.Color.green())
            emb.set_footer(icon_url="https://cdn.discordapp.com/icons/1079971830384828497/13187ab394935d83c4ba995bcbbe3e18.webp?size=1024&format=webp&width=0&height=204", text="Supercord Support")
            await channel.send(embed=emb, view=TicketCloseView())
            

            def check_ticket_creator(m):
                return m.author == interaction.user and m.channel == channel

            try:
                # wait for first message from op
                message = await client.wait_for('message', check=check_ticket_creator, timeout=300)
                # ping staff
                role = discord.utils.get(interaction.guild.roles, id=SUPPORT_ID)
                await message.channel.send(f"<:tick:1247281066889318401> Thank you very much! Please wait for our staff to respond to you, while you do, please read <#1079976824873943052>\n<:tick:1247281066889318401> At any given moment, we have over 30+ tickets open, so please **avoid pinging our staff**, I already did once, {role.mention}")
            except asyncio.TimeoutError:
                # ticket expired (5min)
                await channel.send(f"Sorry, {interaction.user.mention}, you took too long to respond. Please create a new ticket if you still need assistance. I'm closing this ticket for now.")
                emb = discord.Embed(description="Ticket closed", color=discord.Color.yellow())
                await channel.send(embed=emb)
                await channel.delete()
        else:
            # category not found
            await interaction.response.send_message("Category not found.", ephemeral=True)  # Ephemeral message

@tree.command(name="ticket-button", description="Sends a button in the current channel to create a ticket.")
async def send_ticket_button_command(interaction: discord.Interaction):
    # ticket button
    await interaction.response.send_message("Button sent!", ephemeral=True)
    emb = discord.Embed(description=f"**Support**\nTo create a ticket react with {CREATE_EMOJI}", color=discord.Color.green())
    emb.set_footer(icon_url="https://cdn.discordapp.com/icons/1079971830384828497/13187ab394935d83c4ba995bcbbe3e18.webp?size=1024&format=webp&width=0&height=204", text="Supercord Support")
    await interaction.channel.send(view=ButtonView(), embed=emb)

@client.event
async def on_message(message: discord.Message):
    fetched_message = await message.channel.fetch_message(message.id)
    content = fetched_message.content

    if content.startswith("$blacklist"):
        if message.author.roles.count(discord.utils.get(message.guild.roles, id=SUPPORT_ID)) == 0:
            await message.add_reaction(X_EMOJI)
            return
        try:
            user = message.mentions[0]
            await user.add_roles(discord.utils.get(message.guild.roles, id=BLACKLISTED_ID))
            await message.add_reaction(TICK_EMOJI)
        except IndexError:
            await message.add_reaction(X_EMOJI)

    elif content.startswith("$unblacklist"):
        if message.author.roles.count(discord.utils.get(message.guild.roles, id=SUPPORT_ID)) == 0:
            await message.add_reaction(X_EMOJI)
            return
        try:
            user = message.mentions[0]
            await user.remove_roles(discord.utils.get(message.guild.roles, id=BLACKLISTED_ID))
            await message.add_reaction(TICK_EMOJI)
        except IndexError:
            await message.add_reaction(X_EMOJI)

    if isinstance(message.channel, discord.TextChannel) and message.channel.category and message.channel.category.id == CATEGORY_ID and not message.author.bot:
        # $close command
        if content == "$close":
            for member in message.channel.members:
                if discord.utils.get(member.roles, id=SUPPORT_ID) is None:
                    await message.channel.set_permissions(member, view_channel=False)

            emb = discord.Embed(description=f"Ticket closed by {message.author.mention}", color=discord.Color.yellow())
            await message.channel.send(embed=emb, view=ClosedTicket())

        # $rename command
        elif content.startswith("$rename"):
            try:
                new_name = content.split("$rename ", 1)[1]
                await message.add_reaction(TICK_EMOJI)
                await message.channel.edit(name=new_name)
            except IndexError:
                await message.add_reaction(X_EMOJI)

        # $add <user> and $remove <user> command
        elif content.startswith("$add"):
            if message.author.roles.count(discord.utils.get(message.guild.roles, id=SUPPORT_ID)) == 0:
                await message.add_reaction(X_EMOJI)
                return
            try:
                user = message.mentions[0]
                await message.add_reaction(TICK_EMOJI)
                await message.channel.set_permissions(user, view_channel=True,send_messages=True,embed_links=True,attach_files=True,add_reactions=True,use_external_emojis=True,use_external_stickers=True,mention_everyone=True,read_message_history=True,use_application_commands=True)
            except IndexError:
                await message.add_reaction(X_EMOJI)

        elif content.startswith("$remove"):
            if message.author.roles.count(discord.utils.get(message.guild.roles, id=SUPPORT_ID)) == 0:
                await message.add_reaction(X_EMOJI)
                return
            try:
                user = message.mentions[0]
                await message.add_reaction(TICK_EMOJI)
                await message.channel.set_permissions(user, view_channel=False)
            except IndexError:
                await message.add_reaction(X_EMOJI)

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

if __name__ == '__main__':
    client.run(TOKEN)
