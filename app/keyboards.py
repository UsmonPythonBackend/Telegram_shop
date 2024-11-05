from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Категория')],
                                     [KeyboardButton(text='Корзина')],
                                     [KeyboardButton(text='Контакты'),
                                      KeyboardButton(text='О нас')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Телефоны', callback_data='phone')],
    [InlineKeyboardButton(text='Компьютеры', callback_data='computer')],
    [InlineKeyboardButton(text='Аксессуары', callback_data='accessories')]])


get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True)]],
                                 resize_keyboard=True)