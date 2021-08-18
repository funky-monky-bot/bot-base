from os import getenv, path, listdir
import sys
import logging
import asyncio
import re

from tortoise import Tortoise

import discord
from discord.ext import commands

import models
from logger import configure_logging
from bot import Bot
from utils import getenv_bool


def prefix(bot: Bot, message: discord.Message) -> list:
    if message.type == discord.MessageType.default:
        match = re.match(bot.prefix_re, message.content)
        if match:
            return match.group()
    return bot.default_prefix


async def setup(bot: commands.Bot):
    # Connect to DB
    if getenv_bool("DB_ENABLED"):
        await Tortoise.init(
            db_url=getenv("DB_URL"), modules={"models": [models.__name__]}
        )

    # Load extension cogs
    for filename in listdir(path.join(path.dirname(path.realpath(__file__)), "cogs")):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{filename[0:-3]}")
                logging.debug(f"cog extension {filename[0:-3]} loaded successfully")
            except commands.ExtensionError as e:
                logging.error(e)
    if getenv_bool("JSK_ENABLED"):
        bot.load_extension("jishaku")


def task_done_callback(task: asyncio.Task) -> None:
    if task.exception():
        task.print_stack()


bot = Bot(prefix, case_insensitive=True)

if __name__ == "__main__":
    bot.configure_env()
    configure_logging()

    if not getenv("BOT_TOKEN"):
        logging.critical(
            "You must specify a bot token to connect to discord with (see secret.env.example)"
        )
        sys.exit(1)

    loop = asyncio.get_event_loop()
    logging.info("Initialising...")
    try:
        loop.run_until_complete(setup(bot))  # Setup bot

        # Run bot forever
        start_task = loop.create_task(bot.start(getenv("BOT_TOKEN")))
        start_task.add_done_callback(task_done_callback)

        loop.run_forever()
    except KeyboardInterrupt:
        logging.debug("KeyboardInterrupt")  # Probably raised by Ctrl+C at terminal
    finally:
        logging.debug("Logging out from discord")
        loop.run_until_complete(bot.close())
        logging.info("Logged out from discord")
    loop.run_until_complete(Tortoise.close_connections())
    logging.debug("Shutting down asynchronous generators to close loop")
    loop.run_until_complete(loop.shutdown_asyncgens())
    logging.info("Terminating program")
    sys.exit(0)
