from aiogram.utils import executor
from aiogram import Bot,Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, callback_query
import random
from aioparser.parser import run_tasks

bot = Bot('5507867442:AAE_hv9ZSvgK7Xas1LGOKDz5F60oMEcZe78')
dp = Dispatcher(bot)

list_of_jokes = []


@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    await bot.send_message(message.from_user.id, 'привет могу рассказать анекдот', reply_markup=user_kb)


@dp.callback_query_handler(text='joke_button')
async def get_joke(callback_query: types.CallbackQuery):
    global list_of_jokes
    if len(list_of_jokes) == 0:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'в базе нет анекдотов', reply_markup=update_base_kb)
    else:
        await bot.answer_callback_query(callback_query.id)
        msg = random.choice(list_of_jokes)
        await bot.send_message(callback_query.from_user.id,  f'<b>{msg}</b>', parse_mode=types.ParseMode.HTML,
                               reply_markup=user_kb)


@dp.callback_query_handler(text='update_button')
async def update_base(callback_query: types.CallbackQuery):
    global list_of_jokes
    try:
        list_of_jokes = await run_tasks()
        await bot.answer_callback_query(callback_query.id, 'база данных успешно обновлена', show_alert=True)

    except Exception as ex:
        await bot.send_message(callback_query.from_user.id, repr(ex), reply_markup=update_base_kb)

"""******************   BUTTONS  ****************"""
user_kb = InlineKeyboardMarkup(resize_keyboard=True)\
    .add(InlineKeyboardButton('получить анекдот', callback_data='joke_button'))

update_base_kb = InlineKeyboardMarkup(resize_keyboard=True)\
    .add(InlineKeyboardButton('обновить базу анекдотов', callback_data='update_button'))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)