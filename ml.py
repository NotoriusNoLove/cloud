import pandas as pd
import numpy as np
import pickle


def get_values_ml(data):
    # Загрузка модели, StandardScaler и списка столбцов
    with open('model.pkl', 'rb') as f:
        lasso_loaded = pickle.load(f)

    with open('scaler.pkl', 'rb') as f:
        st_loaded = pickle.load(f)

    with open('columns.pkl', 'rb') as f:
        columns = pickle.load(f)

    # Пример новой строки данных
    data = {
        'Species': 'Bream',
        'Length1': 23.2,
        'Length2': 25.4,
        'Length3': 30.0,
        'Height': 11.52,
        'Width': 4.02
    }

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


print(get_values_ml('11'))
