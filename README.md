# FUNKY MONKY

> OOOO AAAA OOOO AAAA

This repo is for a fully-functioning but purpose-neutral discord bot, designed to be extended. It is written in [discord.py](https://github.com/Rapptz/discord.py/). This bot is used as a base for all public bots made by Funky Monky Development.

It is distributed under the [GNU Affero General Public License v3.0 (GNU AGPLv3)](LICENSE) (see [below](#license))

### See also

- The [discord.py documentation](https://discordpy.readthedocs.io/)
- The [pipenv documentation](https://pipenv.pypa.io/) (used to handle the dependencies of the project)
- The [jishaku documentation](https://jishaku.readthedocs.io/) (a library used by the bot mainly as an extension for debug and diagnostic purposes)

## Installation for self-hosting

**Be sure to read [about the license](#license)**

### Configuration System

The bot makes use of two (technically optional) configuration files: `shared.env` and `secret.env`. Both of these files' values are simply treated as environment variables and added to the bot's environment during runtime. Moreover, you can override any configuration value simply by specifying an environment variable in your system of the exact same name. It is worth noting that there is a command included in the bot (only usable by bot owners, of course) that allows the reloading of the env files. In this case (and when the bot is initially started), the following order of precedence is taken: First, the variables in secret.env are added. Next, the variables in shared.env are added (overwriting those from secret.env). Finally, the actual environment variables in the system environment when the bot was run are added (overwriting those from both shared.env and secret.env).

### Step-by-Step installation

This guide assumes you have python 3.8 (and git) installed and this repository cloned. It also assumes that all commands you run are run within your cloned copy of this repository

1. Install pipenv with pip (if not already installed):

```bash
pip install pipenv
```

2. Install the project dependencies with pipenv

```bash
pipenv install
```

3. That's it, **provided you aren't expanding the bot**. Now run the bot with

```bash
pipenv run python main.py
```

#### If you're looking to fork/expand/change the source code of the bot

1. Install the dev dependencies too!

```bash
pipenv install --dev
```

2. Make sure to install the pre-commit hooks (pre-commit should be installed as part of the dev dependencies)!

```bash
pre-commit install
```

3. Be absolutely sure to check out [CONTRIBUTING.md **(coming soon)**](CONTRIBUTING.md) and the [License section](#license) below

## License

This bot is licensed under the GNU Affero General Public License v3.0 (GNU AGPLv3). For full legalese see the [license file](LICENSE), or alternatively see the [tl;drLegal page](<https://tldrlegal.com/license/gnu-affero-general-public-license-v3-(agpl-3.0)>)

The important thing to note is that if you are self-hosting the software and making absolutely no changes to the source code (editing the .env files is obviously fine), you are legally safe. However, **if you change the bot's source code, you must open-source your version under the same license. In this case, you must also state all changes you have made publicly.** For more information, read up about the license through one of the aforementioned sources.
