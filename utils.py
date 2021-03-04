from os import getenv


FALSEY_VALUES = ["false", "f", "", "no"]


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
    if getenv(key).lower() in FALSEY_VALUES:
        return False
    return True
