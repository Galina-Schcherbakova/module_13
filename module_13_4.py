from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


API_TOKEN = '7789653976:AAHvzizuR1Tgnbp62o5UcBL2wF66mggpMCc'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    await message.reply("Чтобы начать, введите 'Calories'.")


@dp.message_handler(lambda message: message.text == 'Calories')
async def set_age(message: types.Message):
    await UserState.age.set()
    await message.reply("Введите свой возраст:")


@dp.message_handler(state=UserState.age)

async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.reply("Введите свой рост:")


@dp.message_handler(state=UserState.growth)

async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.reply("Введите свой вес:")


@dp.message_handler(state=UserState.weight)

async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))

    bmr = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.reply(f"Ваша норма калорий: {bmr:.2f} калорий в день.")

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
