import logging
import os
from os import getenv
from dotenv import dotenv_values
import re

import discord
from discord.ext import commands

from utils import getenv_list, getenv_bool


class Bot(commands.Bot):
    # Saved here so that the .env files can be reloaded and not overwrite the actual
    # environment variables set by the user and/or system
    original_environ = os.environ.copy()

    def __init__(self, *args, **kwargs):
        # process_prefixes called to redefine on connect
        self.prefix_re = ""
        self.default_prefix = ""

        super().__init__(*args, **kwargs)

    # Overwrites default owner check to allow for additional owners as supplied in env
    async def is_owner(self, user: discord.User) -> bool:
        if user.id in [int(oid) for oid in getenv_list("OWNER_IDS")]:
            return True

        # Else fall back to the original
        return await super().is_owner(user)

    async def on_connect(self) -> None:
        self.process_prefixes()
        logging.debug("Prefix Regex created")

    async def on_ready(self) -> None:
        logging.info(f"Active and ready on bot {self.user} with ID {self.user.id}")
        await self.change_presence(
            activity=discord.Game(
                f"with my {len(self.users)} monké brethren \U0001F46F"
            )
        )

        # Check for error channel
        channel = self.get_channel(int(getenv("ERROR_CHANNEL_ID")))
        if channel is None:
            logging.warning(
                "Could not find error channel, have you configured it correctly?"
            )

    def process_prefixes(self) -> str:
        # Implemented here so that it can be updated without bot reload by other areas
        # of the bot. The alternative is to get and process the environment variable on
        # every prefix check, which has the potential to greatly increase resource
        # usage. (The prefix check is run for every message the bot sees.)

        prefix_list = getenv_list("COMMAND_PREFIXES")
        formatted_prefixes = "|".join([re.escape(pf.strip()) for pf in prefix_list])

        self.prefix_re = r"({}{}) ?(?=[^ ])".format(
            formatted_prefixes,
            rf"|<@!?{self.user.id}>" if getenv_bool("MENTION_PREFIX") else "",
        )
        # In case no prefixes match, as a valid prefix must be returned
        self.default_prefix = prefix_list[0]

    def configure_env(self):
        """
        Load dotenv files into os.environ, replacing variables previously loaded from
        these files but not replacing values from system env at program start
        """
        os.environ = {
            **dotenv_values("secret.env"),
            **dotenv_values("shared.env"),
            **self.original_environ,
        }
