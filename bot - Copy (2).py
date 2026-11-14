import discord
from discord import app_commands

class StickerBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        #syncs the commands globally so they work across your account
        await self.tree.sync()

client = StickerBot()

STICKERS = {
    "cat1": "https://file.garden/ZmE9PiOgiFXI9Y4Y/weixintietu/cat1.png",
    "lm-ao": "https://file.garden/ZmE9PiOgiFXI9Y4Y/weixintietu/lm-ao.png",
    "what": "https://file.garden/ZmE9PiOgiFXI9Y4Y/weixintietu/what.png",
    "chipmunk": "https://file.garden/ZmE9PiOgiFXI9Y4Y/weixintietu/chipmunk.png",
    "cat-blush": "https://file.garden/ZmE9PiOgiFXI9Y4Y/weixintietu/cat-blush.png",
    "T-T": "https://file.garden/ZmE9PiOgiFXI9Y4Y/weixintietu/T-T.png",
    "he": "https://file.garden/ZmE9PiOgiFXI9Y4Y/weixintietu/he.png",
    "beer": "https://file.garden/ZmE9PiOgiFXI9Y4Y/weixintietu/beer.png",
    "tsingtao": "https://file.garden/ZmE9PiOgiFXI9Y4Y/weixintietu/tsingtao.jpeg",
}

# autocomplete function for /weixin
async def sticker_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    choices = [
        app_commands.Choice(name=name, value=name)
        for name in STICKERS.keys() if current.lower() in name.lower()
    ]
    return choices[:25]

@client.tree.command(name="weixin", description="播送微信或line的貼圖")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(name="貼圖名字 (e.g., cat1)")
@app_commands.autocomplete(name=sticker_autocomplete)
async def weixin(interaction: discord.Interaction, name: str):
    sticker_name = name.lower().strip()
    
    if sticker_name in STICKERS:
        image_url = STICKERS[sticker_name]
        await interaction.response.send_message(image_url)
    else:
        await interaction.response.send_message(
            f"貼圖 '{name}' 不存在. 使用 `/stickers` 查看完整列表.", 
            ephemeral=True
        )

@client.tree.command(name="stickers", description="查看所有可用的微信貼圖")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def stickers_directory(interaction: discord.Interaction):
    sticker_list = ", ".join([f"`{name}`" for name in STICKERS.keys()])
    
    directory_message = (
        "**可用的微信貼圖:**\n"
        f"{sticker_list}\n\n"
        "使用 `/weixin [name]` 來發送一個!"
    )
    
    await interaction.response.send_message(directory_message, ephemeral=True)

@client.event
async def on_ready():
    print(f'登入成功 {client.user}!')
    print('全域指令同步中. 這可能需要一個小時才能在所有地方出現.')

client.run('SECRET_TOKEN')