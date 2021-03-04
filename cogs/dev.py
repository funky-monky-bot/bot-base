import logging
import os
from os import getenv
from dotenv import dotenv_values

import discord
from discord.ext import commands

from bot import Bot


class DevCog(commands.Cog, name="Developer Tools"):
    """
    Tools for use exclusively by developers/bot owners.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="envreload", aliases=["env_reload", "ereload", "er"])
    async def env_reload(self, ctx: commands.Context):
        """
        Reloads environment variables as well as reloading some non-cog things that use
        environment variables such as prefixes. (currently only prefixes)
        """
        self.bot.configure_env()
        self.bot.process_prefixes()
        logging.debug(f"Env just reloaded by user {ctx.author}")
        await ctx.send("Env Reloaded!")

    @commands.command("brokencommand", aliases=["broken_command", "bc"])
    async def broken_command(self, ctx: commands.Context):
        """
        Raises a base Exception in order to trigger a CommandInvokeError for testing
        the error handler
        """
        raise Exception("Broken command run")


def setup(bot: Bot) -> None:
    bot.add_cog(DevCog(bot))
