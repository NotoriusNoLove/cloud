import pandas as pd
import numpy as np
import pickle
import warnings

warnings.filterwarnings('ignore')


def get_values_ml(data):
    with open('model.pkl', 'rb') as f:
        lasso_loaded = pickle.load(f)

    with open('scaler.pkl', 'rb') as f:
        st_loaded = pickle.load(f)

    with open('columns.pkl', 'rb') as f:
        columns = pickle.load(f)

    new_df = pd.DataFrame([data])

    new_df_label = pd.get_dummies(new_df, columns=['Species'])

    for col in columns:
        if col not in new_df_label.columns:
            new_df_label[col] = 0

    new_df_label = new_df_label[columns]

    new_df_std = st_loaded.transform(new_df_label)

    new_pred = lasso_loaded.predict(new_df_std)

    new_pred_exp = np.exp(new_pred) - 1

    return f"Предсказанный вес: {new_pred_exp[0]}"


print(get_values_ml('11'))
