import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

SHOP_PAGES = [
    discord.SelectOption(label="Miscellaneous", value="misc", description="Miscellaneous things like optimizers", emoji="<:bur:1107810155397136394>"),
    discord.SelectOption(label="Roles", value="roles", description="Roles and trial roles", emoji="<:GodofSpawnsIcon:1172586580477743144>"),
    discord.SelectOption(label="Experience", value="xp", description="Buy experience to level up!", emoji="<:clover:1112488290545827870>"),
]

items = {
    "misc": [
        {
            "name": "Optimizer",
            "description": "One-time use of optimizer to optimize your build!",
            "price": 1000,
            "emoji": "<:bur:1107810155397136394>",
            "value": "optimizer"
        }
    ],
    "roles": [
        {
            "name": "Platinum",
            "description": "Said to be the rarest role",
            "price": 100000,
            "emoji": "<:florrTroll:1082737694288912464>",
            "value": "platinum"
        },
        {
            "name": "Patreon 1d Trial",
            "description": "Patreon 1 day tier-3 trial!",
            "price": 100000,
            "emoji": "<:superior_patron:1243475995189837824>",
            "value": "patreon1daytrial"
        }
    ],
    "xp": [
        {
            "name": "5k XP",
            "description": "Withdraw 5k of experience instantly!",
            "price": 1000,
            "emoji": "<:florrUpvote:1083863165995069492>",
            "value": "5kxp"
        },{
            "name": "25k XP",
            "description": "Withdraw 25k of experience instantly!",
            "price": 4000,
            "emoji": "<:florrUpvote:1083863165995069492>",
            "value": "25kxp"   
        }        
    ]
}

ITEMS = {}
for category, items_list in items.items():
  options = []
  for item in items_list:
    label = f"{item['name']}: {item['price']} Supercoins"
    value = item['value']
    description = item['description']
    emoji = item['emoji']
    option = discord.SelectOption(label=label, value=value, description=description, emoji=emoji)
    options.append(option)
  ITEMS[category] = options

def find_info(value):
      item_info = None
      for category, items_list in items.items():
        for item in items_list:
          if item['value'] == value:
            item_info = item
            break
        if item_info is not None:
          break

      return item_info

class BuyingView(discord.ui.View):
   def __init__(self, value):
      super().__init__(timeout=30)
      self.value = value

   @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
   async def cancel_callback(self, interaction, button):
      await interaction.response.edit_message(embed=discord.Embed(title="Super Shop", description="You have cancelled the purchase.", color=discord.Color.red()), view=None)
   
   @discord.ui.button(label="Buy", style=discord.ButtonStyle.green)
   async def buy_item_callback(self, interaction, button):
      info = find_info(self.value)
      name = info["name"]
      price = info["price"]
      if False: # handle balace check
        emb = discord.Embed(title="Super Shop", description=f"Successfully bought {name} for {price} <:Supercoin:1200278703805050981>.", color=discord.Color.green())
        emb.set_footer(text=f"{price} supercoins have been debited from your account.")
        await interaction.response.edit_message(embed=emb, view=None)
      else:
        emb = discord.Embed(title="Super Shop", description=f"You need a minimum of {price} <:Supercoin:1200278703805050981> to buy {name}", color=discord.Color.red())
        await interaction.response.edit_message(embed=emb, view=None)


class ShopView(discord.ui.View):
  def __init__(self, user, options=SHOP_PAGES):
        super().__init__(timeout=30)
        self.main = True
        if options != SHOP_PAGES:
            self.main = False
        self.user = user
        self.options = options
        self.goback = discord.ui.Button(label="Go Back", style=discord.ButtonStyle.secondary)
        self.goback.callback = self.goback_callback
        self.select = discord.ui.Select(
            placeholder='Select a shop category',
            options=self.options,
            max_values=1
        )
        self.select.callback = self.select_option_callback
        if options != SHOP_PAGES:
            self.add_item(self.goback)
        self.add_item(self.select)


  async def select_option_callback(self, interaction: discord.Interaction):
      if interaction.user != self.user:
        await interaction.response.send_message("You are not allowed to interact with this shop. Please do /shop to open the shop!", ephemeral=True)
        return
      selected_value = self.select.values[0]
      if self.main:
        options = ITEMS[selected_value]
        emb = discord.Embed(
            title="Super Shop",
            description="Buy items with your supercoins! You have 45 <:Supercoin:1200278703805050981>.",
            color=discord.Color.green()
        )
        emb.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        await interaction.response.edit_message(embed=emb, view=ShopView(user=interaction.user, options=options))
        return
      info = find_info(selected_value)
      name = info["name"]
      price = info["price"]
      emb = discord.Embed(title="Super Shop", description=f"Are you sure you want to buy {name} for {price} <:Supercoin:1200278703805050981>?", color=discord.Color.yellow())
      await interaction.response.send_message(content=interaction.user.mention, ephemeral=True, embed=emb, view=BuyingView(selected_value))

  async def goback_callback(self, interaction):
      if interaction.user != self.user:
        await interaction.response.send_message("You are not allowed to interact with this shop. Please do /shop to open the shop!", ephemeral=True)
        return
      emb = discord.Embed(title="Super Shop", description="Buy items with your supercoins! You have 45 <:Supercoin:1200278703805050981>.", color=discord.Color.green())
      emb.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
      await interaction.response.edit_message(embed=emb, view=ShopView())


@tree.command(name="shop", description="Buy items with your supercoins!",)
async def shop(interaction: discord.Interaction):
    user = interaction.user
    emb = discord.Embed(title="Super Shop", description="Buy items with your supercoins! You have 45 <:Supercoin:1200278703805050981>.", color=discord.Color.green())
    emb.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
    await interaction.response.send_message(embed=emb, view=ShopView(user=user))

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)