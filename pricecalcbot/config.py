"""Application configurations.

Configurations are stored in env variables (See Spacefile)
or just specified as variables.

Configurations can bu used as dependencies.
"""


from os import environ


def get_bot_token() -> str:
    """Get bot token from env vars.

    See BOT_TOKEN in Spacefile.

    Returns:
        Telegram-bot token.
    """
    return environ['BOT_TOKEN']


def get_bot_secret() -> str:
    """Get telegram webhook secret from env vars.

    See BOT_SECRET in Spacefile.

    Returns:
        Telegram webhook secret.
    """
    return environ['BOT_SECRET']
