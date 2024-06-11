import warnings
import pickle
import numpy as np
import pandas as pd
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
    name = State()
    weight = State()
    len1 = State()
    len2 = State()
    len3 = State()
    height = State()
    width = State()


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

Введите данные рыбы:
    """
    )
    await state.set_state(Form.name)


@form_router.message(Form.name)
async def get_values(message: Message, state: FSMContext) -> None:
    data = str(message.text).split()

    new_data = {
        'Species': data[0],
        'Length1': float(data[1]),
        'Length2': float(data[2]),
        'Length3': float(data[3]),
        'Height': float(data[4]),
        'Width': float(data[5])
    }

    await message.answer(get_values_ml(new_data))
    await state.set_state(Form.weight)


warnings.filterwarnings('ignore')


def get_values_ml(data):
    # Загрузка модели, StandardScaler и списка столбцов
    with open('model.pkl', 'rb') as f:
        lasso_loaded = pickle.load(f)

    with open('scaler.pkl', 'rb') as f:
        st_loaded = pickle.load(f)

    with open('columns.pkl', 'rb') as f:
        columns = pickle.load(f)

    # Пример новой строки данных
    # data = {
    #     'Species': 'Bream',
    #     'Length1': 23.2,
    #     'Length2': 25.4,
    #     'Length3': 30.0,
    #     'Height': 11.52,
    #     'Width': 4.02
    # }

    # Создание DataFrame из новой строки данных
    new_df = pd.DataFrame([data])

    # Закодировать категориальные переменные так же, как в обучающей выборке
    new_df_label = pd.get_dummies(new_df, columns=['Species'])

    # Убедитесь, что в новой строке есть все столбцы, которые есть в обучающей выборке
    for col in columns:
        if col not in new_df_label.columns:
            new_df_label[col] = 0

    # Убедитесь, что порядок столбцов совпадает
    new_df_label = new_df_label[columns]

    # Стандартизация новой строки данных
    new_df_std = st_loaded.transform(new_df_label)

    # Прогноз с использованием загруженной модели
    new_pred = lasso_loaded.predict(new_df_std)

    # Преобразование предсказания обратно из логарифмической шкалы
    new_pred_exp = np.exp(new_pred) - 1

    return f"Предсказанный вес: {new_pred_exp[0]}"
