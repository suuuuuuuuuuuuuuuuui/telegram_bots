from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sawe_login_passworld_bot.bot_db import *
import os


bot = Bot('5507867442:AAE_hv9ZSvgK7Xas1LGOKDz5F60oMEcZe78')
dp = Dispatcher(bot, storage=MemoryStorage())
admin_id = 5474341798


users = {}


class FSMAdmin(StatesGroup):
    show_info = State()
    get_login = State()
    get_password = State()
    accept = State()
    get_info = State()


@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Ввод отменен', reply_markup=user_start_kb)
    await FSMAdmin.show_info.set()


@dp.message_handler(Text(equals=['добавить аккаунт', 'получить информацию'], ignore_case=True))
@dp.message_handler(commands='start')
async def start_mess(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=user_start_kb)
        await FSMAdmin.show_info.set()
    else:
        await bot.send_message(message.from_user.id, 'Вы не имеете права для работы с этим ботом')


@dp.message_handler(state=FSMAdmin.show_info)
async def send_info(message: types.Message, state: FSMContext):
    if message.text == 'получить информацию':
        await sql_read_info(message=message)
        await state .finish()
    else:
     await bot.send_message(message.from_user.id, 'Введите логин', reply_markup=cancel_button)
     await FSMAdmin.get_login.set()


@dp.message_handler(state=FSMAdmin.get_login)
async def get_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    await FSMAdmin.get_password.set()
    await bot.send_message(message.from_user.id, 'Введите пароль', reply_markup=cancel_button)


@dp.message_handler(state=FSMAdmin.get_password)
async def get_password(message: types.Message, state: FSMContext):
    global login, password
    async with state.proxy() as data:
        data['password'] = message.text

    login = data.get('login')
    password = data.get('password')
    await bot.send_message(message.from_user.id, f'Убедитесь в правильности введенных данных\n\nЛогин: {login},\n'
                                                 f'пароль: {password}', reply_markup=yes_no_kb)
    await FSMAdmin.accept.set()


@dp.message_handler(state=FSMAdmin.accept)
async def accept(message: types.Message, state: FSMContext):
    global login, password, users
    try:
        await sql_add_account(login=login, password=password)
        await bot.send_message(message.from_user.id,'ваши данные успешно сохранены', reply_markup=user_start_kb)
        await state.finish()
    except Exception as ex:
        print(repr(ex))
        await bot.send_message(message.from_user.id, 'произошла ошибка, возможно такой логин уже существует',
                               reply_markup=user_start_kb)
        await FSMAdmin.show_info.set()

    # if message.text == 'Да':
    #     users[login] = password
    #     print(users)
    #     await state.finish()
    # else:
    #     await bot.send_message(message.from_user.id, 'Ввод отменен, выберете действие', reply_markup=user_start_kb)
    #     await FSMAdmin.show_info.set()


"""***************************   BUTTONS   *******************************"""
user_start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('добавить аккаунт'))\
    .add(KeyboardButton('получить информацию'))

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Отмена'))

choice_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('добавить'))\
    .add(cancel_button)


yes_no_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Да'))\
    .add(KeyboardButton('нет'))


if __name__ == '__main__':
    print('bot polling started')
    sql_start()
    executor.start_polling(dp, skip_updates=True)
