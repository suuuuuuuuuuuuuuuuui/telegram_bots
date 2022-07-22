from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import os
import aiofiles


bot = Bot('5507867442:AAE_hv9ZSvgK7Xas1LGOKDz5F60oMEcZe78')
dp = Dispatcher(bot)
number = 100
count_of_attempts = 1


@dp.message_handler(commands="start")
async def start_message(message: types.Message):
    if count_of_attempts == 1:
        await bot.send_message(message.from_user.id, f"привет, {message.from_user.full_name}, я загадал число,"
                                                     f" попробуй его угадать")
    else:
        await bot.send_message(message.from_user.id, "введите число")


@dp.message_handler()
async def info(message: types.Message):
    global number, count_of_attempts

    try:
        if int(message.text) == number:
            await message.answer(f"поздравляю! вы угадали! \n кол-во попыток: {count_of_attempts}")

        elif int(message.text) < number:
            await message.answer("ваше число меньше загаданного \nПопробуй ввести число еще раз")
            count_of_attempts += 1
        else:
            await message.answer("ваше число больше загаданного \n Попробуй ввести число еще раз")
            count_of_attempts += 1
    except:
        await bot.send_message(message.from_user.id, f"привет, {message.from_user.full_name}, я загадал число,"
                                                      f" попробуй его угадать")


if __name__ == "__main__":
    print("Бот запущен")
    executor.start_polling(dp)
