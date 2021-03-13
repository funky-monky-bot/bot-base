from datetime import datetime

import discord
from discord.ext import commands

from bot import Bot


class MiscCog(commands.Cog, name="Miscellaneous Commands"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """
        Gives the bot websocket latency as well as time taken to send message!
        """
        text = f"Pong!\U0001f3d3\n\nLatency: `{int(self.bot.latency * 1000)}ms`"

        start_time = datetime.now()
        msg = await ctx.send(text)
        await msg.edit(
            content=f"{text}\nTime taken to send this message: "
            f"`{int((datetime.now() - start_time).total_seconds() * 1000)}ms`"
        )


def setup(bot: Bot) -> None:
    bot.add_cog(MiscCog(bot))
