from aiogram import F, Router
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, BufferedInputFile, \
    InputFile, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

form_router = Router()


class Form(StatesGroup):
    state_1 = State()
    state_2 = State()


@form_router.message(Command(commands=['start']))
async def start(message: Message, state: FSMContext) -> None:
    await message.answer(
        """
Привет! Я ваш помощник по предсказанию веса рыбы. Просто введите параметры вашей рыбы, и я скажу вам её приблизительный вес. Вот что мне нужно:

Вес - вес рыбы в граммах
Длина 1- вертикальная длина в сантиметрах
Длина 2 - диагональная длина в сантиметрах
Длина 3 - поперечная длина в сантиметрах
Высота - высота рыбы в сантиметрах
Ширина - диагональная ширина в сантиметрах
Вводите данные, и я помогу вам узнать вес вашей рыбы!
    """
    )
    await state.set_state(Form.state_2)


@form_router.message(Form.state_2)
async def get_values(message: Message, state: FSMContext) -> None:
    await message.answer(message.text)
