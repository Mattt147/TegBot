from aiogram.fsm.state import StatesGroup, State


class Reg(StatesGroup):
    fullname = State()
    password = State()


class Administration(StatesGroup):

    username = State()
    new_access = State()


class Bor(StatesGroup):
    indef = State()
    photo =  State()
    description = State()
    date = State()

class Accept(StatesGroup):
    date = State()