"""Calculations FSM states."""


from aiogram.fsm.state import State, StatesGroup


class CalculationsState(StatesGroup):
    """States of whole calculations process."""

    wait_customer_name = State()
    wait_article = State()
    wait_article_name = State()
    wait_article_duty_fee_ratio = State()
    wait_item_name = State()
    wait_item_count = State()
    wait_item_unit_weight = State()
    wait_item_price_currency = State()
    wait_item_unit_price = State()
    wait_continuation = State()
    wait_contact_select = State()
    wait_contact_search = State()
    wait_confirmation = State()
