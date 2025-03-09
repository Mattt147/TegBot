
# from aiogram.methods import send_message 
# from aiogram import methods
import utils
from aiogram import Router, F
from aiogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION



router = Router()
my_url = "t.me/TstTmcBot"




@router.message(Command("start"))
async def start_handler(msg: Message):
    inline_button1 = InlineKeyboardButton(text="Вперед",  callback_data='reg')
    kb = InlineKeyboardMarkup(inline_keyboard=[[inline_button1]])
    await msg.answer( text="Начать регистрацию", reply_markup = kb )



@router.callback_query(F.data == "reg")
async def callback_reg_handler(callback : CallbackQuery):
    await callback.message.answer("Как вас зовут")
    



@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def join_to_group_handler(event  : ChatMemberUpdated): 
    inline_button1 = InlineKeyboardButton(text="Регистрация", url = my_url)
    kb = InlineKeyboardMarkup(inline_keyboard=[[inline_button1]])
    await event.answer(text = "Перейдите в меня и зарегистрируйтесь", reply_markup = kb )



@router.message(Command("menu"))
async def menu_handler(msg: Message):
    kb = utils.create_menu_keyboard()
    await msg.answer(text="Выбрать действие",reply_markup = kb )



