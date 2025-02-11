from aiogram.fsm.state import StatesGroup, State

class SendingPost(StatesGroup):
    WAITING = State()