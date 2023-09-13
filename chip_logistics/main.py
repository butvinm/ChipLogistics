"""Entry point of application.

Telegram Bot and FastAPI instances are created and
services and dependencies initialized there.
"""


from chip_logistics.api.factory import init_app

app = init_app()
