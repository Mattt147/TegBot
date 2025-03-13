from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile, Message
import os
import DBController
from BOTIINT import bot


def create_menu_keyboard():
    button_borr = InlineKeyboardButton(text ="Заимствовать", callback_data="bor")
    button_adm = InlineKeyboardButton(text ="Администрирование", callback_data="adm")
    button_see_bd = InlineKeyboardButton(text ="Увидеть бд", url = "t.me/TstTmcBot")
    button_duty =  InlineKeyboardButton(text ="Мои долги", callback_data="duty")
    button = InlineKeyboardButton(text = "Отдать долг", callback_data= "duty")
    lst = [[button_borr,button], [button_see_bd, button_duty], [button_adm]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=lst)

    return keyboard



def count_all_process():
    file_path = "logs.txt"
    res = 0
    with open(file_path, 'r') as file:
        res = len(file.readlines())
    
    return res


def count_all_photo():
    lst = os.listdir("images")
    lst2 = os.listdir("log_images")
    return len(lst) + len(lst2)




