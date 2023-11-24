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


def get_fixer_api_key() -> str:
    """Get Fixer API key from env vars.

    See FIXER_API_KEY in Spacefile.

    Returns:
        Fixer API key.
    """
    return environ['FIXER_API_KEY']


def get_repo_template_name() -> str:
    """Get name of current reports template document.

    Returns:
        Reports template document name.
    """
    return environ['REPORT_TEMPLATE']
