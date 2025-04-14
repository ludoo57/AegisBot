import discord
from redbot.core import commands
from redbot.core.bot import Red

class AegisWelcome(commands.Cog):
    """Affiche un menu d’accueil interactif à l’arrivée du bot ou via commande."""

    def __init__(self, bot: Red):
        self.bot = bot

    async def send_tutorial(self, guild: discord.Guild, channel: discord.TextChannel):
        embed = discord.Embed(
            title="🤖 Bienvenue sur AegisBOT !",
            description=(
                "Merci d'utiliser **AegisBOT** dans votre serveur Discord !\n\n"
                "AegisBOT est un bot basé sur Red-DiscordBot, pensé pour vous offrir des outils avancés de modération, vérification, logs, et plus encore.\n\n"
                "Utilisez le menu ci-dessous pour découvrir rapidement les fonctionnalités principales du bot."
            ),
            color=discord.Color.blurple()
        )
        embed.set_footer(text="AegisBOT - propulsé par RedBot")

        view = AegisWelcomeView(self.bot)
        await channel.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = discord.utils.find(
            lambda c: c.permissions_for(guild.me).send_messages,
            guild.text_channels
        )
        if channel:
            await self.send_tutorial(guild, channel)

    @commands.command()
    @commands.guild_only()
    async def aegispanel(self, ctx: commands.Context):
        """Réaffiche le menu d'accueil interactif d'AegisBOT."""
        await self.send_tutorial(ctx.guild, ctx.channel)

class AegisWelcomeView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=120)
        self.bot = bot
        self.add_item(AegisMenuSelect(bot))

class AegisMenuSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Commandes utiles", description="Liste des commandes Redbot/AegisBOT", value="help"),
            discord.SelectOption(label="Modules disponibles", description="Modules actuellement chargés", value="modules"),
            discord.SelectOption(label="Assistance", description="Obtenir de l'aide pour bien démarrer", value="aide")
        ]
        super().__init__(placeholder="Choisissez une catégorie...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "help":
            embed = discord.Embed(
                title="📘 Commandes utiles",
                description=(
                    "- `!help` : Affiche toutes les commandes disponibles\n"
                    "- `!config` : Si disponible, permet d’ouvrir un panneau interactif\n"
                    "- Mentionnez le bot pour obtenir l’aide rapide"
                ),
                color=discord.Color.green()
            )
        elif self.values[0] == "modules":
            embed = discord.Embed(
                title="🧩 Modules chargés (par catégorie)",
                color=discord.Color.teal()
            )
            help_cog = self.bot.get_cog("customHelp")
            categories = getattr(help_cog, "GLOBAL_CATEGORIES", {}) if help_cog else {}
            for key, cat in categories.items():
                cogs_list = cat.cogs
                if not cogs_list:
                    continue
                embed.add_field(
                    name=f"{cat.emoji} {cat.name}",
                    value="\n".join(f"• `{cog}`" for cog in cogs_list),
                    inline=False
                )
        else:
            embed = discord.Embed(
                title="🆘 Assistance",
                description=(
                    "AegisBOT est basé sur Redbot.\n"
                    "Utilisez `!help` ou consultez la documentation de votre fork Redbot.\n\n"
                    "En cas de besoin, contactez l’équipe de modération de votre serveur."
                ),
                color=discord.Color.orange()
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AegisWelcome(bot))