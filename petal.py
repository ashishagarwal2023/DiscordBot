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

petals = [
    {
        "name": "Air",
        "emoji": '<:air:1204771365400354897>',
        "desc": "It's literally nothing.",
        "reload": 0,
        "rarities": [
            {
                "rarity": "common",
                "extra radius": 8
            },
            {
                "rarity": "unusual",
                "extra radius": 16
            },
            {
                "rarity": "rare",
                "extra radius": 24
            },
            {
                "rarity": "epic",
                "extra radius": 32
            },
            {
                "rarity": "legendary",
                "extra radius": 40
            },
            {
                "rarity": "mythic",
                "extra radius": 48
            },
            {
                "rarity": "ultra",
                "extra radius": 56
            },
            {
                "rarity": "super",
                "extra radius": 64
            },
        ]
    },
    {
        "name": "Amulet",
        "emoji": '<:florrAmulet:1222714614127661147>',
        "desc": "Converts a percentage of overheal into shields.",
        "reload": 2,
        "rarities": [
            {
                "rarity": "common",
                "health": 10,
                "overheal": "5%"
            },
            {
                "rarity": "unusual",
                "health": 30,
                "overheal": "10%"
            },
            {
                "rarity": "rare",
                "health": 90,
                "overheal": "15%"
            },
            {
                "rarity": "epic",
                "health": 270,
                "overheal": "20%"
            },
            {
                "rarity": "legendary",
                "health": 810,
                "overheal": "25%"
            },
            {
                "rarity": "mythic",
                "health": 2430,
                "overheal": "30%"
            },
            {
                "rarity": "ultra",
                "health": 7290,
                "overheal": "35%"
            },
            {
                "rarity": "super",
                "health": 21870,
                "overheal": "40%"
            },
        ]
    },
    {
        "name": "Ankh",
        "emoji": '<:ankh:1204770936126177351>',
        "desc": "An ancient relic. When destroyed, will teleport the flower back to where it was destroyed.",
        "reload": [
            "256 + 0.5",
            "128 + 0.5",
            "64 + 0.5",
            "32 + 0.5",
            "16 + 0.5",
            "8 + 0.5",
            "4 + 0.5",
            "2 + 0.5",
        ],
        "rarities": [
            {
                "rarity": "common",
                "health": 10,
            },
            {
                "rarity": "unusual",
                "health": 30,
            },
            {
                "rarity": "rare",
                "health": 90,
            },
            {
                "rarity": "epic",
                "health": 270,
            },
            {
                "rarity": "legendary",
                "health": 810,
            },
            {
                "rarity": "mythic",
                "health": 2430,
            },
            {
                "rarity": "ultra",
                "health": 7290,
            },
            {
                "rarity": "super",
                "health": 21870,
            },
        ]
    },
    {
        "name": "Antennae",
        "emoji": '<:antennae:1204752606837215272>',
        "desc": "Allows your flower to sense foes further away.",
        "reload": [None, None, 0, 0, 0, 0, 0, 0],
        "rarities": [
            {
                "rarity": "rare",
                "extra vision": 25
            },
            {
                "rarity": "epic",
                "extra vision": 33.3
            },
            {
                "rarity": "legendary",
                "extra vision": 42.9
            },
            {
                "rarity": "mythic",
                "extra vision": 100
            },
            {
                "rarity": "ultra",
                "extra vision": 185.7
            },
            {
                "rarity": "super",
                "extra vision": 400
            },
        ]
    },
    {
        "name": "Basic",
        "emoji": '<:basic:1204188019129851954>',
        "desc": "A nice petal, not too strong but not too weak.",
        "reload": 2.5,
        "rarities": [
            {
                "rarity": "common",
                "health": 10,
                "damage": 10
            },
            {
                "rarity": "unusual",
                "health": 30,
                "damage": 30
            },
            {
                "rarity": "rare",
                "health": 90,
                "damage": 90
            },
            {
                "rarity": "epic",
                "health": 270,
                "damage": 270
            },
            {
                "rarity": "legendary",
                "health": 810,
                "damage": 810
            },
            {
                "rarity": "mythic",
                "health": 2430,
                "damage": 2430
            },
            {
                "rarity": "ultra",
                "health": 7290,
                "damage": 7290
            },
            {
                "rarity": "super",
                "health": 21870,
                "damage": 21870
            },
        ]
    }
]

def get_petal(petal_name):
  """
  Retrieve the properties of a given petal from the petals list.

  Args:
    petal_name (str): The name of the petal to retrieve.

  Returns:
    dict: A dictionary containing the properties of the petal, including name, emoji, desc, and reload.

  """
  for petal in petals:
    if petal["name"].lower() == petal_name.lower():
      name = petal["name"]
      emoji = petal["emoji"]
      desc = petal["desc"]
      reload = petal["reload"]
      # reload is usually a number but in case of some petals it is an array of numbers
      # turn the number into a list always
      if isinstance(reload, int) or isinstance(reload, float) or isinstance(reload, str):
        reload = [reload] * 8

      rarities = petal["rarities"]
      return {
        "name": name,
        "emoji": emoji,
        "desc": desc,
        "reload": reload,
        "rarities": rarities
      }
    
  return None

@tree.command(name="petal", description="Buy or sell your petals!")
async def petal_info(interaction: discord.Interaction, petal_name: str):
    petal = get_petal(petal_name)
    if petal == None:
       emb = discord.Embed(title="Petal not found", description="The petal you are looking for does not exist.", color=discord.Color.red())
    else:
        title = f"{petal['emoji']} {petal['name']}"

        
    props_all = [
        {"id": "health", "name": "Health", "type": int, "unit": "HP"},
        {"id": "damage", "name": "Damage", "type": int, "unit": "DMG"},
        {"id": "extra radius", "name": "Extra Radius", "type": int, "unit": "Extra Radius"},
        {"id": "overheal", "name": "Overheal", "type": str, "unit": "Overheal"},
        {"id": "extra vision", "name": "Extra Vision", "type": (int, float), "unit": "Extra Vision"},
    ]
    
    props = ""
    
    for prop in props_all:
        prop_id = prop["id"]
        prop_name = prop["name"]
        prop_type = prop["type"]
        prop_unit = prop["unit"]
        
        if prop_id in petal['rarities'][0] and isinstance(petal['rarities'][0][prop_id], prop_type):
            prop_values = ""
            for petal_rarity in petal['rarities']:
                if isinstance(petal_rarity[prop_id], prop_type):
                    prop_values += f"**{rarity[petal_rarity['rarity'].title()]} {petal_rarity['rarity'].title()}**: {petal_rarity[prop_id]} {prop_unit}\n"
                else:
                    prop_values += f"**{rarity[petal_rarity['rarity'].title()]} {petal_rarity['rarity'].title()}**: N/A {prop_unit}\n"
            props += f"**{prop_name}:**\n{prop_values}\n\n"
    

        reload = ""
        if petal['reload'][0] != None:
          reload += f"**{rarity['Common']} Common**: {petal['reload'][0]}s\n"
        if petal['reload'][1] != None:
          reload += f"**{rarity['Unusual']} Unusual**: {petal['reload'][1]}s\n"
        if petal['reload'][2] != None:
          reload += f"**{rarity['Rare']} Rare**: {petal['reload'][2]}s\n"
        if petal['reload'][3] != None:
          reload += f"**{rarity['Epic']} Epic**: {petal['reload'][3]}s\n"
        if petal['reload'][4] != None:
          reload += f"**{rarity['Legendary']} Legendary**: {petal['reload'][4]}s\n"
        if petal['reload'][5] != None:
           reload += f"**{rarity['Mythic']} Mythic**: {petal['reload'][5]}s\n"
        if petal['reload'][6] != None:
           reload += f"**{rarity['Ultra']} Ultra**: {petal['reload'][6]}s\n"
        if petal['reload'][7] != None:
           reload += f"**{rarity['Super']} Super**: {petal['reload'][7]}s\n"

        desc = f"*{petal['desc']}*\n\n{props}**Reload:**\n{reload}"
        emb = discord.Embed(
           title=title, 
           description=desc, 
           color=discord.Color.green())
    await interaction.response.send_message(embed=emb)

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


if __name__ == '__main__':
    client.run(TOKEN)
