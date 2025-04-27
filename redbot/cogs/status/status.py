import discord
import platform
import time
from redbot.core import commands
from redbot import __version__ as red_version
from datetime import timedelta

class Status(commands.Cog):
    """Afficher le statut général du bot."""

    def __init__(self, bot):
        self.bot = bot
        self.launch_time = time.time()

    @commands.hybrid_command(name="status", with_app_command=True)
    async def status(self, ctx: commands.Context):
        """Affiche l'état du bot (latence, uptime, version...)"""
        uptime = str(timedelta(seconds=int(time.time() - self.launch_time)))
        ping = round(self.bot.latency * 1000)
        python_version = platform.python_version()
        total_cogs = len(self.bot.cogs)
        total_commands = len(self.bot.commands)

        embed = discord.Embed(
            title="📊 Statut du Bot",
            color=discord.Color.green()
        )
        embed.add_field(name="🟢 État", value="En ligne", inline=True)
        embed.add_field(name="📡 Latence", value=f"{ping}ms", inline=True)
        embed.add_field(name="⏱ Uptime", value=uptime, inline=True)
        embed.add_field(name="🧠 AegisBOT", value=red_version, inline=True)
        embed.add_field(name="🐍 Python", value=python_version, inline=True)
        embed.add_field(name="🧩 Cogs chargés", value=str(total_cogs), inline=True)
        embed.add_field(name="⚙️ Commandes", value=str(total_commands), inline=True)
        embed.set_footer(text="AegisBOT")

        await ctx.send(embed=embed)
