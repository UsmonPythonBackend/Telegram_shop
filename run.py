import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from app import keyboards as kb
from aiogram.fsm.context import FSMContext
from app.middlewares import TestMiddleware

from app.database.models import async_main
import app.database.requests as rq

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.message.outer_middleware(TestMiddleware())

class Register(StatesGroup):
    name = State()
    age = State()
    number = State()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в магазин гаджетов!', reply_markup=kb.main)



@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи')


@dp.message(F.text == 'Категория')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=kb.catalog)


@dp.callback_query(F.data == 'phone')
async def phone(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию', show_alert=True)
    await callback.message.answer('Вы выбрали категорию телефоны')


@dp.callback_query(F.data == 'computer')
async def computer(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию', show_alert=True)
    await callback.message.answer('Вы выбрали категорию компьютеры')

@dp.callback_query(F.data == 'accessories')
async def accessories(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию', show_alert=True)
    await callback.message.answer('Вы выбрали категорию аксессуары')


@dp.message(Command('register'))
async def register(message: Message, state:FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')


@dp.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')

@dp.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer('Введите ваш номер телефона', reply_markup=kb.get_number)


@dp.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст:{data["age"]}\nНомер: {data["number"]}')
    await state.clear()



async def main():
    await async_main()
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')
