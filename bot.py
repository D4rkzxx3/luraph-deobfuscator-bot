import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Load environment
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN non trovato in .env")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="/",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    logger.info(f"Bot loggato come {bot.user}")
    print(f"\n{'='*50}")
    print(f"✅ Bot Online: {bot.user}")
    print(f"✅ Latenza: {bot.latency*1000:.2f}ms")
    print(f"{'='*50}\n")
    
    try:
        synced = await bot.tree.sync()
        logger.info(f"Sincronizzati {len(synced)} comandi slash")
    except Exception as e:
        logger.error(f"Errore sincronizzazione comandi: {e}")

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Errore comando: {error}")
    await ctx.send(f"❌ Errore: {error}")

@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    logger.error(f"Errore app command: {error}")
    await interaction.response.send_message(f"❌ Errore: {error}", ephemeral=True)

# Load cogs
async def load_cogs():
    cogs_dir = 'cogs'
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
        logger.info(f"Cartella {cogs_dir} creata")
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f"✅ Caricato cog: {filename}")
            except Exception as e:
                logger.error(f"❌ Errore caricamento {filename}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot arrestato dall'utente")
    except Exception as e:
        logger.critical(f"Errore critico: {e}")
