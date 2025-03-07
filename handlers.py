
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
    #if (msg.from_user.username) обработка повторной регистрации
    pass



@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def join_to_group(event  : ChatMemberUpdated): 
    inline_butto1 = InlineKeyboardButton(text="Регистрация", url = my_url, callback_data='reg')
    kb = InlineKeyboardMarkup(inline_keyboard=[[inline_butto1]])
    await event.answer(text = "Перейдите в меня и зарегистрируйтесь", reply_markup = kb )

@router.callback_query(F.data.startswith('reg'))
async def get_send_shtrihcode(call: CallbackQuery):
    await call.message.answer(text = "Давай зарегаемся ")