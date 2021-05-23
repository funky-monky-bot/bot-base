from os import getenv
import re

from discord.ext import commands


FALSEY_VALUES = ["false", "f", "", "no"]


class MentionConverter(commands.Converter):
    """
    Converts to either a Role, Member, @everyone or @here mention.

    This is checked in the following order:

    1. Check if text is simply "@everyone" or "everyone"
    2. Check if text is simply "@here" or "here"
    3. Check if text can be converted to Role object using RoleConverter and get the
    mention string if so
    4. Check if text can be converted to Member or User object using MemberConverter
    and get the mention string if so
    """

    async def convert(self, ctx: commands.Context, argument: str):
        if re.match(r"@?everyone", argument.lower()):
            return "@everyone"
        if re.match(r"@?here", argument.lower()):
            return "@here"

        try:
            converter = commands.RoleConverter()
            role = await converter.convert(ctx, argument)
            return role.mention
        except (commands.NoPrivateMessage, commands.BadArgument):
            pass

        try:
            converter = commands.MemberConverter()
            user = await converter.convert(ctx, argument)
            return user.mention
        except commands.BadArgument:
            pass

        raise commands.BadArgument(f'mention for "{argument}" could not be created')


def getenv_list(key: str) -> list:
    """
    Returns the environment variable associated with the key specified
    split into a list by the semicolon (";") delimiter.

    Does not split on semicolons escaped with a backslash ("\").
    In order to treat a backslash as just a single backslash, double-escape it ("\\").

    It's worth noting that all backslashes are treated as escape characters by this
    function, such that any character coming after a non-double-escaped backslash is
    treated as an escaped character, and the backslash is removed.
    To avoid this, simply double-escape any backslash you want to be literal, otherwise
    it makes the next character literal instead.

    This function is made as a utility for https://github.com/funky-monky-bot/bot
    with heavy inspiration from this stackoverflow answer:
    https://stackoverflow.com/a/21882672
    """
    result = []
    current = []
    s_iter = iter(getenv(key))
    for char in s_iter:
        if char == "\\":
            try:
                current.append(next(s_iter))
            except StopIteration:
                current.append("\\")
        elif char == ";":
            result.append("".join(current))
            current = []
        else:
            current.append(char)
    result.append("".join(current))
    return result


def getenv_bool(key: str) -> bool:
    return getenv(key).lower() not in FALSEY_VALUES
