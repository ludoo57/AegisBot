from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.views import ConfirmView
from discord.ui import View, Select, Button
from discord import Interaction, Embed, SelectOption, Colour
import discord

class AegisConfig(commands.Cog):
    """Configuration avancée d’AegisBOT."""

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command(name="config")
    @commands.is_owner()
    async def aegis_config(self, ctx: commands.Context):
        """Ouvre le menu de configuration d’AegisBOT."""
        view = ConfigMainView(self.bot, ctx.author)
        embed = Embed(title="⚙️ Menu de configuration", description="Utilisez les menus ci-dessous pour configurer AegisBOT.", color=Colour.blurple())
        await ctx.send(embed=embed, view=view)

class ConfigMainView(View):
    def __init__(self, bot: Red, author: discord.User):
        super().__init__(timeout=120)
        self.bot = bot
        self.author = author
        self.add_item(ConfigSelect(bot))
        self.add_item(RefreshButton(bot, author))

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user.id == self.author.id

class ConfigSelect(Select):
    def __init__(self, bot: Red):
        self.bot = bot
        options = [
            SelectOption(label="Résumé de la configuration", value="summary", description="Afficher un résumé de la config actuelle."),
            SelectOption(label="Modules (Cogs)", value="modules", description="Afficher et gérer les modules actifs."),
        ]
        super().__init__(placeholder="Choisissez une section à configurer...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "summary":
            embed = Embed(title="📊 Résumé de la configuration", color=Colour.blurple())
            prefixes = await self.bot.get_valid_prefixes()
            embed.add_field(name="Préfixes", value=", ".join(prefixes), inline=False)
            embed.set_footer(text="AegisBOT - Configuration")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "modules":
            all_cogs = set(await self.bot._cog_mgr.available_modules())
            loaded_cogs = set(self.bot.extensions.keys())
            unloaded_cogs = all_cogs - loaded_cogs

            view = ModuleManagerView(self.bot, sorted(loaded_cogs), sorted(unloaded_cogs), interaction.user)
            await interaction.response.send_message("📦 Modules disponibles :", view=view, ephemeral=True)

class ModuleManagerView(View):
    def __init__(self, bot: Red, loaded, unloaded, user):
        super().__init__(timeout=120)
        self.bot = bot
        self.user = user
        if unloaded:
            self.add_item(ModuleLoadSelect(bot, unloaded))
        if loaded:
            self.add_item(ModuleUnloadSelect(bot, loaded))

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user.id == self.user.id

class ModuleLoadSelect(Select):
    def __init__(self, bot: Red, unloaded):
        self.bot = bot
        options = [SelectOption(label=cog, value=cog) for cog in unloaded[:25]]
        super().__init__(placeholder="📥 Charger un module...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: Interaction):
        cog = self.values[0]
        spec = await self.bot._cog_mgr.find_cog(cog)
        if not spec:
            await interaction.response.send_message(f"❌ Impossible de trouver le module `{cog}`.", ephemeral=True)
            return
        try:
            await self.bot.load_extension(spec)
            await self.bot.add_loaded_package(cog)
            await interaction.response.send_message(f"✅ Module `{cog}` chargé avec succès !", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur lors du chargement de `{cog}` : {e}", ephemeral=True)

class ModuleUnloadSelect(Select):
    def __init__(self, bot: Red, loaded):
        self.bot = bot
        options = [SelectOption(label=cog, value=cog) for cog in loaded[:25]]
        super().__init__(placeholder="📤 Décharger un module...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: Interaction):
        cog = self.values[0]
        print(f"Tentative de déchargement du module : {cog}")  # Pour déboguer
        if cog not in self.bot.extensions:
            await interaction.response.send_message(
                f"❌ Le module `{cog}` n’est pas chargé ou n’est pas un module valide.", ephemeral=True
            )
            return
        try:
            await self.bot.unload_extension(cog)
            await self.bot.remove_loaded_package(cog)
            await interaction.response.send_message(f"✅ Module `{cog}` déchargé avec succès !", ephemeral=True)
        except Exception as e:
            import traceback
            await interaction.response.send_message(
                f"❌ Erreur lors du déchargement de `{cog}` : {e}\nDétails : {traceback.format_exc()}", ephemeral=True
            )

class RefreshButton(Button):
    def __init__(self, bot: Red, author: discord.User):
        super().__init__(label="🔄 Rafraîchir", style=discord.ButtonStyle.primary)
        self.bot = bot
        self.author = author

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Tu n'es pas autorisé à utiliser ce menu.", ephemeral=True)
            return
        await interaction.response.send_message("🔁 Menu rafraîchi.", view=ConfigMainView(self.bot, self.author), ephemeral=True)

async def setup(bot):
    await bot.add_cog(AegisConfig(bot))