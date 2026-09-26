import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class UtilsCog(commands.Cog):
    """Utility commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Event listener per messaggi"""
        if message.author == self.bot.user:
            return
        
        if message.content.startswith('!'):
            logger.info(f"Comando ricevuto da {message.author}: {message.content}")

async def setup(bot):
    await bot.add_cog(UtilsCog(bot))
