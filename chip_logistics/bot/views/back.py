"""Back button keyboard."""


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from chip_logistics.bot.callbacks.back import BackCallback
from chip_logistics.bot.texts.back import BACK_BTN

back_btn = InlineKeyboardButton(
    text=BACK_BTN,
    callback_data=BackCallback().pack(),
)

back_btns = [[back_btn]]


back_kb = InlineKeyboardMarkup(inline_keyboard=back_btns)
