"""Articles menu states."""


from aiogram.fsm.state import State, StatesGroup


class CreateArticleState(StatesGroup):
    """FSM of article creation."""

    wait_name = State()
    wait_duty_fee_ratio = State()
    wait_confirmation = State()
