from aiogram.fsm.state import StatesGroup, State

class SendingPost(StatesGroup):
    GET_POST = State()