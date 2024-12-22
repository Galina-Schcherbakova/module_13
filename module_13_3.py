import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = ' '

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Вы можете отправить любое сообщение, и я отвечу на него.')

@dp.message_handler(lambda message: True)
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    print("Запуск бота...")
    executor.start_polling(dp, skip_updates=True)
