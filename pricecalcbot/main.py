"""Entry point of application.

Telegram Bot and FastAPI instances are created and
services and dependencies initialized there.
"""


from pricecalcbot.api.factory import init_app

app = init_app()
