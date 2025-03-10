from aiogram.fsm.state import StatesGroup, State


class Reg(StatesGroup):
    fullname = State()
    password = State()


class Administration(StatesGroup):

    username = State()
    new_access = State()
    