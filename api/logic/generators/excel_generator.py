from typing import Optional

import pandas as pd

from api.logic.clean_data import get_clean_data, get_month_df

FILENAME = 'Tabla.xlsx'


def monthly_excel(path, file):
    excel_path = path / FILENAME

    df = get_clean_data(file)
    month_df = get_month_df(df)#get data from last month
    month_df = month_df.sort_values(['User', 'Description'], ascending=[True, True])
    month_df.to_excel(excel_path, index = False)
    return excel_path