from .status import Status

async def setup(bot):
    await bot.add_cog(Status(bot))
