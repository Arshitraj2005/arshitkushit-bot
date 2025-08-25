import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Load music cog
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

# Load cogs
async def setup():
    await bot.load_extension("cogs.music")

bot.loop.create_task(setup())
bot.run(TOKEN)
