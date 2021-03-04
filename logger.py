import logging
import logging.config
from os import path, getenv, mkdir, listdir, remove
from datetime import datetime
import re

from colorama import init, Fore, Back, Style

init()

LOGS_DIR = path.join(path.dirname(path.realpath(__file__)), "logs")
COLOURED_LOGGING_FORMATS = {
    logging.DEBUG: f"%(asctime)s - {Fore.GREEN}{Style.DIM}DEBUG:\t  %(message)s"
    f"{Style.RESET_ALL}",
    logging.INFO: f"%(asctime)s - {Fore.CYAN}INFO:\t\t  %(message)s{Style.RESET_ALL}",
    logging.WARNING: f"%(asctime)s - {Fore.YELLOW}WARNING:\t  %(message)s"
    f"{Style.RESET_ALL}",
    logging.ERROR: f"%(asctime)s - {Back.RED}{Fore.CYAN}{Style.BRIGHT}ERROR:\t  "
    f"%(message)s{Style.RESET_ALL}",
    logging.CRITICAL: f"%(asctime)s - {Back.RED}{Style.BRIGHT}CRITICAL:\t  %(message)s"
    f"{Style.RESET_ALL}",
}
UNCOLOURED_LOGGING_FORMATS = {
    logging.DEBUG: "%(asctime)s - DEBUG:\t  %(message)s",
    logging.INFO: "%(asctime)s - INFO:\t\t  %(message)s",
    logging.WARNING: "%(asctime)s - WARNING:\t  %(message)s",
    logging.ERROR: "%(asctime)s - ERROR:\t  %(message)s",
    logging.CRITICAL: "%(asctime)s - CRITICAL:\t  %(message)s",
}


class Formatter(logging.Formatter):
    def __init__(self, coloured: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level_dict = (
            COLOURED_LOGGING_FORMATS if coloured else UNCOLOURED_LOGGING_FORMATS
        )

    def format(self, record: logging.LogRecord):

        # Save original format
        original = self._style._fmt

        # Replace with different format depending on logging level
        self._style._fmt = self.level_dict[record.levelno]

        # Call the original formatter
        result = logging.Formatter.format(self, record)

        # Restore original format
        self._style._fmt = original

        return result


def prepare_logs_dir() -> None:
    if not path.isdir(LOGS_DIR):
        mkdir(LOGS_DIR)
        return

    files = listdir(LOGS_DIR)
    if len(files) == 0:
        return  # If no files in logs dir for whatever reason, return

    # Remove latest.log, as the program is now running again, and it may be replaced.
    latests = filter(lambda fn: fn.startswith("latest.log"), files)
    for l in latests:
        remove(path.join(LOGS_DIR, l))
        files.remove(l)

    max_logs = int(getenv("MAX_LOG_FILES"))

    if len(files) < max_logs or max_logs < 0:
        return  # Return if log limit disabled or under limit

    # Order files and group by datetime in title
    sorted_files = {}
    for fn in files:
        file_dt = datetime.fromisoformat(
            ".".join(re.sub("-(?!.*_)", ":", fn).split(".")[0:2])
        )  # Create datetime object from filename

        # If datetime already in dict, add new filename then continue
        if file_dt in sorted_files.keys():
            sorted_files[file_dt] = [*sorted_files[file_dt], fn]
            continue
        sorted_files[file_dt] = [fn]  # Else, create new with filename

    # Remove oldest logs until under limit
    while len(files) > max_logs:
        to_remove = (
            sorted_files.pop(min(*sorted_files.keys()))
            if len(sorted_files) > 1
            else sorted_files.popitem()[1]
        )
        for fn in to_remove:
            remove(path.join(LOGS_DIR, fn))
            files.remove(fn)


def configure_logging() -> None:
    file_handler_config = {
        "class": "logging.handlers.RotatingFileHandler",
        "maxBytes": 20_000_000,  # 20 MB
        "level": "DEBUG",
        "formatter": "file",
    }

    config = {
        "version": 1,
        "formatters": {"console": {"()": Formatter}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": getenv("CONSOLE_LOG_LEVEL"),
                "formatter": "console",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    }

    # If not disabled, prepare logs dir and log to files too!
    if not int(getenv("MAX_LOG_FILES")) == 0:
        prepare_logs_dir()

        config["formatters"].update({"file": {"()": Formatter, "coloured": False}})
        config["handlers"].update(
            {
                "file": {
                    **file_handler_config,
                    "filename": path.join(
                        LOGS_DIR,
                        f"{str(datetime.now()).replace(':', '-').replace(' ', '_')}.log",
                    ),
                },
                "latest_file": {
                    **file_handler_config,
                    "filename": path.join(LOGS_DIR, "latest.log"),
                },
            }
        )
        config["root"].update({"handlers": ["console", "file", "latest_file"]})

    logging.config.dictConfig(config)

    logging.debug("Log directory organised, old logs deleted and logger set up")
