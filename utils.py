from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup



def create_menu_keyboard():
    button_borr = InlineKeyboardButton(text ="Взаимствовать", callback_data="borr")
    button_adm = InlineKeyboardButton(text ="Администрирование", callback_data="adm")
    button_see_bd = InlineKeyboardButton(text ="Увидеть бд", url = "t.me/TstTmcBot")
    button_duty =  InlineKeyboardButton(text ="Мои долги", callback_data="duty")
    lst = [[button_borr, button_adm], [button_see_bd, button_duty]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=lst)

    return keyboard


def create_borrow_string():
    pass
