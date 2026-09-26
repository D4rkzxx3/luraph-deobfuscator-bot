import discord
from discord.ext import commands
from discord import app_commands
import aiofiles
import os
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DeobfuscatorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.output_dir = 'output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    @app_commands.command(
        name="deobf",
        description="Deobfusca uno script Luraph v15"
    )
    @app_commands.describe(
        script="Lo script da deobfuscare (file o testo)",
        options="Opzioni: --no-hooks, --max-runs N, --devirt-rounds N"
    )
    async def deobfuscate(self, interaction: discord.Interaction, script: str, options: str = ""):
        """Deobfusca script Luraph v15"""
        await interaction.response.defer()
        
        try:
            logger.info(f"Deobfuscazione richiesta da {interaction.user}")
            
            # Validazione
            if not script or len(script) == 0:
                await interaction.followup.send("❌ Script vuoto", ephemeral=True)
                return
            
            if len(script) > 100000:
                await interaction.followup.send("❌ Script troppo grande (max 100KB)", ephemeral=True)
                return
            
            # Parse options
            opts = self._parse_options(options)
            
            # Salva script temporaneo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            user_id = interaction.user.id
            input_file = os.path.join(self.output_dir, f"input_{user_id}_{timestamp}.lua")
            
            async with aiofiles.open(input_file, 'w', encoding='utf-8') as f:
                await f.write(script)
            
            logger.info(f"Script salvato: {input_file}")
            
            # Simula deobfuscazione (stub per ora)
            result = await self._deobfuscate_luraph(input_file, opts)
            
            if result['success']:
                # Prepara file output
                output_file = os.path.join(self.output_dir, f"output_{user_id}_{timestamp}.deobf.luau")
                async with aiofiles.open(output_file, 'w', encoding='utf-8') as f:
                    await f.write(result['content'])
                
                # Crea embed risposta
                embed = discord.Embed(
                    title="✅ Deobfuscazione Completata",
                    description=f"Script Luraph v15 deobfuscato con successo",
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                embed.add_field(name="📊 Statistiche", value=f"```\nLinee: {len(result['content'].splitlines())}\nBytes: {len(result['content'])}\nOpzioni: {opts}\n```", inline=False)
                embed.add_field(name="📝 Note", value=result['message'], inline=False)
                embed.set_footer(text=f"Richiesto da {interaction.user}")
                
                # Invia file se piccolo
                if len(result['content']) < 5000000:  # 5MB
                    with open(output_file, 'rb') as f:
                        file = discord.File(f, filename=f"deobf_{timestamp}.luau")
                        await interaction.followup.send(embed=embed, file=file)
                else:
                    await interaction.followup.send(embed=embed)
                    await interaction.followup.send("⚠️ File troppo grande per allegare. Salvato nel server.")
            else:
                await interaction.followup.send(
                    f"❌ Errore: {result['error']}",
                    ephemeral=True
                )
        
        except Exception as e:
            logger.error(f"Errore deobfuscazione: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ Errore interno: {str(e)[:100]}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="analyze",
        description="Analizza uno script Luraph v15 senza completa devirtualizzazione"
    )
    @app_commands.describe(
        script="Lo script da analizzare"
    )
    async def analyze(self, interaction: discord.Interaction, script: str):
        """Analizza script Luraph v15"""
        await interaction.response.defer()
        
        try:
            logger.info(f"Analisi richiesta da {interaction.user}")
            
            if not script or len(script) == 0:
                await interaction.followup.send("❌ Script vuoto", ephemeral=True)
                return
            
            # Salva temporaneo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            user_id = interaction.user.id
            input_file = os.path.join(self.output_dir, f"analyze_{user_id}_{timestamp}.lua")
            
            async with aiofiles.open(input_file, 'w', encoding='utf-8') as f:
                await f.write(script)
            
            # Analizza
            result = await self._analyze_luraph(input_file)
            
            if result['success']:
                embed = discord.Embed(
                    title="✅ Analisi Completata",
                    color=discord.Color.blue(),
                    timestamp=datetime.now()
                )
                
                analysis_text = result['analysis']
                # Dividi se troppo lungo
                if len(analysis_text) > 1024:
                    chunks = [analysis_text[i:i+1020] for i in range(0, len(analysis_text), 1020)]
                    for i, chunk in enumerate(chunks[:25]):  # Max 25 fields
                        embed.add_field(name=f"Analisi Parte {i+1}", value=f"```\n{chunk}\n```", inline=False)
                else:
                    embed.add_field(name="📋 Risultato Analisi", value=f"```\n{analysis_text}\n```", inline=False)
                
                embed.set_footer(text=f"Richiesto da {interaction.user}")
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    f"❌ Errore analisi: {result['error']}",
                    ephemeral=True
                )
        
        except Exception as e:
            logger.error(f"Errore analisi: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ Errore interno: {str(e)[:100]}",
                ephemeral=True
            )
    
    async def _deobfuscate_luraph(self, file_path: str, options: dict):
        """Deobfusca script Luraph v15 (stub)"""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            # Validazione header Luraph
            if "Luraph Obfuscator v15" not in content and "return setmetatable({" not in content:
                return {
                    'success': False,
                    'error': 'Script non riconosciuto come Luraph v15'
                }
            
            # Simula deobfuscazione (stub)
            deobf_content = self._simulate_deobf(content, options)
            
            return {
                'success': True,
                'content': deobf_content,
                'message': f"Deobfuscazione completata con opzioni: {options}"
            }
        
        except Exception as e:
            logger.error(f"Errore deobfuscazione: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _analyze_luraph(self, file_path: str):
        """Analizza script Luraph v15"""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            analysis = []
            analysis.append(f"📊 Analisi Script Luraph v15")
            analysis.append(f"Linee: {len(content.splitlines())}")
            analysis.append(f"Bytes: {len(content)}")
            
            # Cerca VM signatures
            if "Luraph Obfuscator v15" in content:
                analysis.append("✅ Header Luraph v15 trovato")
            
            if "setmetatable" in content:
                analysis.append("✅ VM object (setmetatable) trovato")
            
            if "bit32" in content:
                analysis.append("✅ Bit32 operations rilevate")
            
            if "LPH_CRASH" in content:
                analysis.append("⚠️ LPH_CRASH rilevato (anti-tamper)")
            
            if "LPH_ENCSTR" in content:
                analysis.append("⚠️ String encryption rilevata")
            
            if "LPH_ENCFUNC" in content:
                analysis.append("⚠️ Function encryption rilevata")
            
            if "LPH_JIT" in content:
                analysis.append("⚠️ JIT compilation rilevata")
            
            analysis_text = "\n".join(analysis)
            
            return {
                'success': True,
                'analysis': analysis_text
            }
        
        except Exception as e:
            logger.error(f"Errore analisi: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _parse_options(self, options_str: str) -> dict:
        """Parsa opzioni da stringa"""
        opts = {
            'no_hooks': False,
            'max_runs': 1000,
            'devirt_rounds': 5
        }
        
        if '--no-hooks' in options_str:
            opts['no_hooks'] = True
        
        if '--max-runs' in options_str:
            try:
                idx = options_str.index('--max-runs')
                val = options_str[idx:].split()[1]
                opts['max_runs'] = int(val)
            except:
                pass
        
        if '--devirt-rounds' in options_str:
            try:
                idx = options_str.index('--devirt-rounds')
                val = options_str[idx:].split()[1]
                opts['devirt_rounds'] = int(val)
            except:
                pass
        
        return opts
    
    def _simulate_deobf(self, content: str, options: dict) -> str:
        """Simula deobfuscazione (stub per sviluppo)"""
        header = f"-- Deobfuscated by Luraph v15 Deobfuscator Bot\n"
        header += f"-- Options: {options}\n"
        header += f"-- Original size: {len(content)} bytes\n\n"
        
        # Stub: ritorna solo una traccia
        return header + "-- [DEVIRTUALIZATION PLACEHOLDER]\n-- Script deobfuscation in progress...\n"

async def setup(bot):
    await bot.add_cog(DeobfuscatorCog(bot))
