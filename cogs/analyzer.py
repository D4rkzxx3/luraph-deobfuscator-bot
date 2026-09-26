import discord
from discord.ext import commands
from discord import app_commands
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AnalyzerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name="status",
        description="Mostra lo stato del bot"
    )
    async def status(self, interaction: discord.Interaction):
        """Status del bot"""
        embed = discord.Embed(
            title="🤖 Status Bot Luraph Deobfuscator",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="✅ Online",
            value=f"Bot Status: **Online**",
            inline=False
        )
        
        embed.add_field(
            name="📊 Informazioni",
            value=f"Latenza: **{self.bot.latency*1000:.2f}ms**\nUtente: **{self.bot.user}**",
            inline=False
        )
        
        embed.add_field(
            name="⚡ Funzionalità",
            value="✅ Deobfuscazione Luraph v15\n✅ Analisi Script\n✅ VM Analysis\n✅ Output File",
            inline=False
        )
        
        embed.add_field(
            name="📝 Comandi",
            value="- `/deobf` - Deobfusca script\n- `/analyze` - Analizza script\n- `/help` - Mostra aiuto",
            inline=False
        )
        
        embed.set_footer(text=f"Richiesto da {interaction.user}")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(
        name="help",
        description="Mostra i comandi disponibili"
    )
    async def help_cmd(self, interaction: discord.Interaction):
        """Aiuto comandi"""
        embed = discord.Embed(
            title="📖 Aiuto - Luraph Deobfuscator Bot",
            color=discord.Color.blue(),
            description="Comandi disponibili per deobfuscare script Luraph v15",
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="/deobf",
            value="**Descrizione**: Deobfusca uno script Luraph v15\n**Uso**: `/deobf script:<testo> options:<opzioni>`\n**Opzioni**:\n- `--no-hooks` - Salta hook processing\n- `--max-runs N` - Max esecuzioni (default 1000)\n- `--devirt-rounds N` - Devirtualizzazione rounds (default 5)",
            inline=False
        )
        
        embed.add_field(
            name="/analyze",
            value="**Descrizione**: Analizza script senza completa devirtualizzazione\n**Uso**: `/analyze script:<testo>`\n**Output**: Dettagli VM, signatures, encryption methods",
            inline=False
        )
        
        embed.add_field(
            name="/status",
            value="**Descrizione**: Mostra lo stato del bot\n**Uso**: `/status`",
            inline=False
        )
        
        embed.add_field(
            name="/help",
            value="**Descrizione**: Questo messaggio\n**Uso**: `/help`",
            inline=False
        )
        
        embed.add_field(
            name="📚 Luraph v15 Features",
            value="✅ Devirtualization - Bytecode VM → Luau reale\n✅ Control Flow - Preservazione control flow\n✅ Proto Analysis - Analisi funzioni\n✅ Constant Rounds - Decodifica costanti\n✅ String Decryption - Decriptazione stringhe\n✅ JIT Support - Supporto JIT compilation",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Note Importanti",
            value="• Max file: 100 KB\n• Deobfuscazione può richiedere tempo\n• Anti-tamper puede influire su risultati\n• Output salvati per debugging",
            inline=False
        )
        
        embed.set_footer(text=f"Richiesto da {interaction.user}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(AnalyzerCog(bot))
