
# from aiogram.methods import send_message 
# from aiogram import methods
import config
import DBController
import utils
from aiogram import Router, F
from aiogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ReplyKeyboardMarkup,  KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.fsm.context import FSMContext
from states import Reg, Administration, Bor
from BOTIINT import bot
import datetime




counter_processes = 0
counter_items = 0 
router = Router()
my_url = "t.me/TstTmcBot"



@router.message(Command("start"))
async def start_handler(msg: Message):
    inline_button1 = InlineKeyboardButton(text="Вперед",  callback_data='reg')
    kb = InlineKeyboardMarkup(inline_keyboard=[[inline_button1]])
    await msg.answer( text="Зарегистрироваться", reply_markup = kb )



@router.callback_query(F.data == "reg")
async def callback_reg_handler(callback : CallbackQuery, state : FSMContext):
    if ( DBController.check_user_reg_by_user_id(callback.from_user.id) == False):
        await callback.message.answer("Напишитие свою фамилию и имя через пробел")
        await state.set_state(Reg.fullname)
    else:
        await callback.message.answer("Вы уже зарегистрированы")
        kb = utils.create_menu_keyboard()
        await callback.message.answer(text="Выбрать действие",reply_markup = kb )




@router.message(Reg.fullname)
async def second_step_reg(msg : Message, state: FSMContext):
    await state.update_data(fullname = msg.text)
    await state.set_state(Reg.password)
    await msg.answer("Введите пароль")




@router.callback_query(F.data == "duty")
async def callback_counter_duty(callback : CallbackQuery):
    pass
    await callback.message.answer(text  = "Ваше количество долгов равно " + str(DBController.get_count_duty(callback.from_user.id)))



@router.message(Reg.password)
async def third_step_reg(msg : Message, state: FSMContext):
    await state.update_data(password = msg.text)
    data = await state.get_data()
    access_state = ""
    if (data["password"]  == config.ADMIN_PASSWORD):
        access_state = "admin"
    elif(data["password"] == config.USER_PASSWORD):
        access_state = "common_user"
    else:
        await state.set_state(Reg.password)
        await msg.answer("Вы не правильно ввели пароль, попробуйте еще раз")
        return
    print(data["fullname"])
    DBController.add_new_user(msg.from_user.id, msg.from_user.username, data["fullname"].split(' ')[0], data["fullname"].split()[1],access_state)
    await msg.answer("Вы зарегистрированы")
    await state.clear()
    kb = utils.create_menu_keyboard()
    await msg.answer(text="Выбрать действие",reply_markup = kb )
        





@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def join_to_group_handler(event  : ChatMemberUpdated): 
    inline_button1 = InlineKeyboardButton(text="Регистрация", url = my_url)
    kb = InlineKeyboardMarkup(inline_keyboard=[[inline_button1]])
    await event.answer(text = "Перейдите в меня и зарегистрируйтесь", reply_markup = kb )





@router.message(Command("menu"))
async def menu_handler(msg: Message):
    kb = utils.create_menu_keyboard()
    await msg.answer(text="Выбрать действие",reply_markup = kb )






@router.callback_query(F.data == "adm")
async def callback_admin(callback : CallbackQuery):
    if (DBController.is_admin(callback.from_user.id) == False):
        await callback.message.answer("У вас нету доступа к этому действию")
        return
    button1 = InlineKeyboardButton(text = "Список пользователей", callback_data="list")
    button2  = InlineKeyboardButton(text = "Изменение прав доступа", callback_data = "change_access")
    button3 = InlineKeyboardButton(text = "Вернуться в главное меню",  callback_data="menu_again")
    lst = [[button1,button2], [button3]]
    kb = InlineKeyboardMarkup(inline_keyboard= lst)
    await callback.message.edit_text(text = "Выбрать действие", reply_markup = kb)





@router.callback_query(F.data == "menu_again")
async def callback_again_menu(callback : CallbackQuery):
    kb = utils.create_menu_keyboard()
    await callback.message.edit_text(text="Выбрать действие",reply_markup = kb)




@router.callback_query(F.data == "bor")
async def callback_borrow(callback : CallbackQuery, state : FSMContext):
    await callback.message.answer("Введите идентификатор ТМЦ. Чтобы пропустить шаг: введите 'Пропустить'.")
    await state.set_state(Bor.indef)
    


@router.message(Bor.indef)
async def id_step_new_ma(msg : Message, state: FSMContext):
    print(msg.text)
    if (msg.text.lower() != "пропустить"):
        await state.update_data(indef = msg.text)
    else:
        await state.update_data(indef = "---")
    await state.set_state(Bor.photo)
    await msg.answer("Введите фотографию ТМЦ.'.")



@router.message(Bor.photo)
async def photo_step(msg : Message, state : FSMContext):
    if (len(msg.photo) ==0):
        msg.answer("Нужно фото без всяких записей")
    photo = msg.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    save_path = "images/" + str(1) + '.jpg'
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())
    await state.update_data( photo = save_path)
    await state.set_state(Bor.description)
    await msg.answer("Введите описание ТМЦ. Чтобы пропустить шаг: введите 'Пропустить'.")



@router.message(Bor.description)
async def step_descrp(msg : Message, state: FSMContext):
    if (msg.text.lower() != "пропустить"):
        await state.update_data(description = msg.text)
    else:
        await state.update_data(description = "---")
    await state.set_state(Bor.date)
    await msg.answer("Введите дату возврата ТМЦ.(дд.мм.гггг)")

@router.message(Bor.date)
async def id_step_date(msg : Message, state: FSMContext):
    witness = DBController.get_witness()
    await state.update_data(date = msg.text)
    data = await state.get_data()
    DBController.add_new_item(data["indef"], data["description"], data["photo"])
    DBController.add_new_process(DBController.get_witness(), msg.from_user.username, 1, data["date"])
    await state.clear()
    string_result, path_photo = DBController.get_process_string(1)
    photo = open(path_photo, "rb")
    await bot.send_message(DBController.get_id_by_username(witness), string_result)
    await bot.send_photo(DBController.get_id_by_username(witness) , photo)
    photo.close()
  



@router.callback_query(F.data == "list")
async def callback_admin(callback : CallbackQuery):
    lst = DBController.getListOfUsers()
    string_users = ""
    for i in range(0, len(lst)):
        string_users+= "{} {} ({}). Количество долгов - {}\n".format( lst[i][1], lst[i][2],lst[i][0],  str(lst[i][3]))
    await callback.message.answer(text = string_users)
    kb = utils.create_menu_keyboard()
    await callback.message.answer(text="Выбрать действие",reply_markup = kb )





@router.callback_query(F.data == "change_access")
async def allback_again_menu(callback : CallbackQuery,state : FSMContext):
    await callback.message.answer(text= "Напишитие username человека, у которого хотите поменять доступ(@....)")
    await state.set_state(Administration.username)






@router.message(Administration.username)
async def second_step_reg(msg : Message, state: FSMContext):
    if (msg.text.startswith('@') == False):
        await msg.answer(text = "Username должен начинаться с @. Попробуйте ещe раз")
        return
    if (DBController.check_user_reg_by_username(msg.text) == False):
        await msg.answer(text ="Такой username не зарегистрирован. Попробуйте еще раз")
        return
    await state.update_data(username = msg.text)
    await state.set_state(Administration.new_access)
    button1 = KeyboardButton(text = "admin")
    button2 = KeyboardButton(text = "common_user")
    button3 = KeyboardButton(text = " witness")
    lst = [[button1,button2,button3]]
    kb = ReplyKeyboardMarkup(keyboard=lst)
    await msg.answer(text = "Введите новый доступ(admin(администратор), common_user(стандартный пользователь), witness(заверитель))", reply_markup= kb)




@router.message(Administration.new_access)
async def new_access(msg : Message, state: FSMContext):
    await state.update_data(new_access = msg.text)
    data = await state.get_data()
    DBController.change_access(data["username"], data["new_access"])
    await state.clear()
    kb = utils.create_menu_keyboard()
    await msg.answer(text = "Вы успешно изменили доступ", reply_markup= ReplyKeyboardRemove())
    await msg.answer(text="Выбрать действие",reply_markup = kb )



# @router.message()
# async def start_handler(msg: Message):
#     msg.answer("Я вас не понимаю. еще раз")