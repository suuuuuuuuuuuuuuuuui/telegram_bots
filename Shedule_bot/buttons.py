from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('пн'), KeyboardButton('вт'),
                                                        KeyboardButton('ср'),
                                                        KeyboardButton('чт'),
                                                        KeyboardButton('пт'),
                                                        KeyboardButton('сб'),
                                                        KeyboardButton('сегодня'),
                                                        KeyboardButton('завтра'))
