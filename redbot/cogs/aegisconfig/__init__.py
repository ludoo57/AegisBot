from .config_menu import AegisConfig

async def setup(bot):
    await bot.add_cog(AegisConfig(bot))
