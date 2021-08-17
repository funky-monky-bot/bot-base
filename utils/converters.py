import re

from discord.ext import commands


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
