import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

emojis = {
    "Super": "<:Super:1204172880787668995>",
    "Ultra": "<:Ultra:1204172874110345308>",
    "Mythic": "<:Mythic:1204172872990457926>",
    "Legendary": "<:Legendary:1204172875314233425>",
    "Epic": "<:Epic:1204172881706229761>",
    "Rare": "<:Rare:1204172878065696828>",
    "Unusual": "<:Unusual:1204172879566999653>",
    "Common": "<:Common:1204172876589043754>"
}

inventory = ["5 Super Bone", "3 Ultra Stinger", "1 Mythic Stinger", "1 Ultra Third Eye", "1 Legendary Third Eye", "1 Epic Third Eye", "1 Rare Third Eye", "1 Unusual Third Eye", "1 Common Third Eye", "1 Ultra Corn", "3 Super Talisman of Evasion", "8 Ultra Poo", "19 Ultra Wing", "5 Ultra Beetle Egg", "1 Mythic Yggdrasil", "4 Ultra Mark"]

def generate_inv_desc(inv):
  inv_desc = ""
  for item in inv:
    item_parts = item.split(" ")
    count = int(item_parts[0])
    rarity = item_parts[1] if len(item_parts) > 1 else ""
    petal_name = " ".join(item_parts[2:]) if len(item_parts) > 2 else item_parts[1]
    count_show = f"` {count}`"
    if count > 9:
       count_show = f"`{count}`"
    inv_desc += f"{emojis.get(rarity, '')} {count_show} {rarity} {petal_name}\n"
  return inv_desc

def generate_pages(inv, length):
  pages = []
  inv_lines = inv.strip().split("\n")
  num_pages = len(inv_lines) // length + (len(inv_lines) % length > 0)
  for i in range(num_pages):
    start = i * length
    end = start + length
    page_items = inv_lines[start:end]
    pages.append("\n".join(page_items))
  return pages

class InventoryView(discord.ui.View):
   def __init__(self, inv):
       super().__init__(timeout=60)
       self.inv = inv
       self.page_contents = generate_pages(self.inv, 10)

       self.page = 0 
       self.current_page_contents  = self.page_contents[self.page]
       

   @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
   async def previous_callback(self, interaction, button):
       if self.page == 0:
          await interaction.response.send_message("You are already at the first page.", ephemeral=True)
          return
       self.page -= 1 if self.page > 0 else 0
       self.current_page_contents = self.page_contents[self.page]
       
       emb = discord.Embed(title=f"{interaction.user.name}'s Inventory", description=self.current_page_contents, color=discord.Color.blue())
       emb.set_footer(text=f"Page {self.page + 1} of {len(self.page_contents)}")
       await interaction.response.edit_message(embed=emb)

   @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
   async def next_callback(self, interaction, button):
       if len(self.page_contents) > self.page + 1:
          self.page += 1
       else:
          await interaction.response.send_message("You have reached the end of the inventory.", ephemeral=True)
          return
       self.current_page_contents = self.page_contents[self.page]

       emb = discord.Embed(title=f"{interaction.user.name}'s Inventory", description=self.current_page_contents, color=discord.Color.blue())
       emb.set_footer(text=f"Page {self.page + 1} of {len(self.page_contents)}")
       await interaction.response.edit_message(embed=emb)
  


@tree.command(name="inventory", description="Check your inventory or view someone's")
async def inventory_command(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    inv = generate_inv_desc(inventory)
    pages = generate_pages(inv, 10)

    emb = discord.Embed(title=f"{user.name}'s Inventory", description=pages[0], color=discord.Color.blue())
    emb.set_footer(text=f"Page 1 of {len(pages)}")
    await interaction.response.send_message(embed=emb, view=InventoryView(inv))
    # emb = discord.Embed(description=)
    


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)
