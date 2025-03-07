
# from aiogram.methods import send_message 
# from aiogram import methods
from aiogram import Router, F
from aiogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION
router = Router()

my_url = "t.me/TstTmcBot"

# menu_keybord = 



@router.message(Command("start"))
async def start_handler(msg: Message):
    inline_butto1 = InlineKeyboardButton(text="Начать регистрацию",  callback_data='reg')
    kb = InlineKeyboardMarkup(inline_keyboard=[[inline_butto1]])
    await msg.answer(text = "Начать регистрацию", reply_markup = kb )


@router.callback_query(F.data == "reg")
async def callback_reg_handler(callback : CallbackQuery):
    await callback.message.answer("Как вас зовут")

@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def join_to_group_handler(event  : ChatMemberUpdated): 
    inline_butto1 = InlineKeyboardButton(text="Регистрация", url = my_url)
    kb = InlineKeyboardMarkup(inline_keyboard=[[inline_butto1]])
    await event.answer(text = "Перейдите в меня и зарегистрируйтесь", reply_markup = kb )


