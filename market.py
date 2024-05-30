import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)  

rarity = {
    "Super": "<:Super:1204172880787668995>",
    "Ultra": "<:Ultra:1204172874110345308>",
    "Mythic": "<:Mythic:1204172872990457926>",
    "Legendary": "<:Legendary:1204172875314233425>",
    "Epic": "<:Epic:1204172881706229761>",
    "Rare": "<:Rare:1204172878065696828>",
    "Unusual": "<:Unusual:1204172879566999653>",
    "Common": "<:Common:1204172876589043754>"
}

auctions = [
    # [seller user id, petal emoji id, petal, rarity, price, id (to buy or manage item)]
    [1153023901203447940, 1204172906544762931, "Claw", "super", 500, 0], 
    [1153023901203447940, 1204203078576898068, "Poo", "ultra", 400, 1], 
    [1153023901203447940, 1204172873057570887, "Jelly", "mythic", 500, 2], 
    [1153023901203447940, 1204187998401462292, "Bone", "ultra", 400, 3], 
    [1153023901203447940, 1204172895182520470, "Stinger", "super", 500, 4], 
    [1153023901203447940, 1204188010392985640, "Starfish", "mythic", 400, 5], 
    [1153023901203447940, 1204172893320384562, "Pollen", "common", 500, 6], 
    [1153023901203447940, 1204188017074634873, "Wing", "ultra", 400, 7], 
    [1153023901203447940, 1204172895765659739, "Talisman of Evasion", "rare", 500, 8], 
    [1153023901203447940, 1204188022187368488, "Powder", "mythic", 400, 9], 
    [1153023901203447940, 1204172906544762931, "Claw", "epic", 500, 10], 
    [1153023901203447940, 1204172910617428078, "Yucca", "unusual", 400, 11], 
    [1153023901203447940, 1204188008375648326, "Light", "mythic", 500, 12], 
    [1153023901203447940, 1204172902522556416, "Bubble", "rare", 400, 13], 
    [1153023901203447940, 1204187989618458706, "Shell", "rare", 500, 14], 
    [1153023901203447940, 1204193501877764187, "Pincer", "epic", 400, 15], 
    [1153023901203447940, 1204187986946949161, "Leaf", "super", 500, 16], 
    [1153023901203447940, 1204187983314550924, "Yggdrasil", "ultra", 400, 17]
]
# auctions = []

def get_item_by_id(id):
    for auction in auctions:
        if auction[5] == id:
            return auction
    return None

def generate_auction_msg():
    if auctions == []:
        return "No auctions available. You may sell your item or check back later to buy something."
    msg = ""
    for auction in auctions:
        seller = auction[0]
        item_emoji = auction[1]
        item_name = auction[2]
        item_rarity = auction[3].title()
        item_rarity_emoji = rarity[item_rarity]
        item_price = auction[4]
        item_id = auction[5]
        msg += f"{item_rarity_emoji} <:_:{item_emoji}> {item_rarity} {item_name} by <@{seller}> for {item_price} <:Supercoin:1200278703805050981> | ID: {item_id}\n"
    return msg

def generate_pages(auctions, lpp=10):
    pages = []
    auction_lines = auctions.strip().split("\n")
    num_pages = len(auction_lines) // lpp + (len(auction_lines) % lpp > 0)
    for i in range(num_pages):
      start = i * lpp
      end = start + lpp
      page_items = auction_lines[start:end]
      pages.append("\n".join(page_items))
    return pages

class BuyingView(discord.ui.View):
    def __init__(self, item):
       super().__init__(timeout=60)

       self.item = item

    @discord.ui.button(label="Buy", style=discord.ButtonStyle.primary)
    async def buy_callback(self, interaction, button):
        emb = discord.Embed(description=f"You have successfully bought a {rarity[self.item[3].title()]} <:_:{self.item[1]}> {self.item[3].title()} {self.item[2]} for {self.item[4]} <:Supercoin:1200278703805050981>.", color=discord.Colour.green())
        await interaction.response.edit_message(embed=emb, view=None)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_callback(self, interaction, button):
        emb = discord.Embed(description="You have cancelled the purchase.", color=discord.Colour.secondary())
        await interaction.response.edit_message(embed=emb, view=None)

class BuyModal(discord.ui.Modal, title="Enter ID of item to buy"):
    item_id = discord.ui.TextInput(label='ID')

    async def on_submit(self, interaction: discord.Interaction):
        try:
            item = get_item_by_id(int(self.item_id.value))
        except ValueError:
            emb = discord.Embed(description="Invalid ID provided. Please enter a valid number.", color=discord.Colour.red())
            await interaction.response.send_message(embed=emb, ephemeral=True)
            return

        if item is None:
            emb = discord.Embed(description="No item is available for sale with the given ID.", color=discord.Colour.red())
            await interaction.response.send_message(embed=emb, ephemeral=True)
            return

        emb = discord.Embed(description=f"Are you sure you want to buy a {rarity[item[3].title()]} <:_:{item[1]}> {item[3].title()} {item[2]} from <@{item[0]}> for {item[4]} <:Supercoin:1200278703805050981>?", color=discord.Colour.yellow())
        await interaction.response.send_message(embed=emb, ephemeral=True, view=BuyingView(item))

class MarketView(discord.ui.View):
   def __init__(self, items, author):
       super().__init__(timeout=60)
       self.page_contents = items
       self.author = author

       self.page = 0 
       self.current_page_contents  = self.page_contents[self.page]
       

   @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
   async def previous_callback(self, interaction, button):
       if self.author != interaction.user:
        return # edit it as you wish
       if self.page == 0:
          await interaction.response.send_message("You are already at the first page.", ephemeral=True)
          return
       self.page -= 1 if self.page > 0 else 0
       self.current_page_contents = self.page_contents[self.page]
       
       emb = discord.Embed(title="Market", description=f"Use your <:Supercoin:1200278703805050981> to buy and sell petals from and to other players!\n\n{self.current_page_contents}", color=discord.Color.dark_magenta())
       emb.set_footer(text=f"Page {self.page + 1} of {len(self.page_contents)}")
       await interaction.response.edit_message(embed=emb)

   @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
   async def next_callback(self, interaction, button):
       if self.author != interaction.user:
        return # edit it as you wish
       if len(self.page_contents) > self.page + 1:
          self.page += 1
       else:
          await interaction.response.send_message("You have reached the end of the inventory.", ephemeral=True)
          return
       self.current_page_contents = self.page_contents[self.page]

       emb = discord.Embed(title="Market", description=f"Use your <:Supercoin:1200278703805050981> to buy and sell petals from and to other players!\n\n{self.current_page_contents}", color=discord.Color.dark_magenta())
       emb.set_footer(text=f"Page {self.page + 1} of {len(self.page_contents)}")
       await interaction.response.edit_message(embed=emb)

   @discord.ui.button(label="Buy", style=discord.ButtonStyle.green)
   async def buy_callback(self, interaction: discord.Interaction, button):
       if self.author != interaction.user:
        return # edit it as you wish
       await interaction.response.send_modal(BuyModal())
   
   @discord.ui.button(label="Sell", style=discord.ButtonStyle.primary)
   async def sell_callback(self, interaction, button):
       if self.author != interaction.user:
        return # edit it as you wish
       pass # make a modal like BuyModal and ask user the petal they want to sell "2sclaw" or maybe multiples and the price they want to sell it for
       # then yourself add it to the auctions
  

@tree.command(name="market", description="Buy or sell your petals!")
async def auctions_command(interaction: discord.Interaction):
    author = interaction.user
    items = generate_pages(generate_auction_msg(), 10)
    emb = discord.Embed(title="Market", description=f"Use your <:Supercoin:1200278703805050981> to buy and sell petals from and to other players!\n\n{items[0]}", color=discord.Color.dark_magenta())
    emb.set_footer(text=f"Page 1 of {len(items)}")

    await interaction.response.send_message(embed=emb, view=MarketView(items, author))

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)
