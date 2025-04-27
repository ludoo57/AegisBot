from .autotuto_on_join import AegisWelcome

async def setup(bot):
    await bot.add_cog(AegisWelcome(bot))
