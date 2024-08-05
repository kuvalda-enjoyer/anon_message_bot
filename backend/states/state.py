from aiogram.fsm.state import StatesGroup, State

class SendingPost(StatesGroup):
    START = State()
    GET_POST = State()
    GET_CONFIRM = State()