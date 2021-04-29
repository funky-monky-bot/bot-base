import logging
from os import getenv
from traceback import format_exception
from datetime import datetime

import discord
from discord.ext import commands

from bot import Bot


ERRORS_TO_IGNORE = (
    commands.CommandNotFound,
    commands.CheckFailure,
    commands.DisabledCommand,
)  # These errors will be ignored by the handler when raised by commands


class ErrorCog(commands.Cog, name="Error Handling"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandError):
        if isinstance(exc, ERRORS_TO_IGNORE):
            return
        if isinstance(exc, commands.CommandInvokeError):  # Bug found in code
            # Generate additional error text:
            additional_error_text = (
                f"Exception Raised!\n"
                f"Command: {ctx.command.qualified_name}\n"
                f"Exception Text: {exc.original.__class__.__name__}: {exc.original}\n"
                f"Raised by user: `{ctx.author}`    `{ctx.author.id}`\n"
                f"Timestamp: {datetime.now().isoformat()}\n"
            )

            # Generate paginated exception with traceback
            paginator = commands.Paginator(prefix="```py")
            for line in format_exception(type(exc), exc, exc.__traceback__):
                paginator.add_line(line[:-1])  # The newline at the end is removed

            async def send_formatted_exc(destination: discord.abc.Messageable) -> None:
                await destination.send(additional_error_text)
                for page in paginator.pages:
                    await destination.send(page)

            if await self.bot.is_owner(ctx.author):  # If owner, DM traceback as well
                await ctx.send(
                    "An error occurred. Since you're an owner, "
                    "I'm DMing you the traceback."
                )
                await send_formatted_exc(ctx.author)

            channel = self.bot.get_channel(int(getenv("ERROR_CHANNEL_ID")))
            if channel is None:
                await ctx.send(
                    "An error appeared in the command, "
                    "but this bot has not had an error channel properly configured. "
                    "Please contact the bot owner to fix this."
                )

            await ctx.send(
                "An error appeared in the command, attempting to report it now, thanks!"
            )
            try:
                await send_formatted_exc(channel)
            except discord.Forbidden:
                logging.error(
                    "Failed to report following exception, "
                    "cannot send messages to error channel."
                )

            logging.error(
                f"Exception raised in command {ctx.command.qualified_name}: "
                f"{exc.original.__class__.__name__}: {exc.original}. "
                "See error channel for full traceback"
            )
            return

        await ctx.send(exc)


def setup(bot: Bot) -> None:
    bot.add_cog(ErrorCog(bot))
