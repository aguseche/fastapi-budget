import pathlib
from typing import Tuple

import pandas as pd

from api.logic.clean_data import get_clean_data, get_lastmonth_df, group_df, prepare_df
from api.logic.data_visualization import create_barchart
from api.logic.pdf_generator import create_analytics_report
from api.logic.manage_files import create_folder, delete_folder, get_pdf_path

different_groups = ['User', 'Type']

def last_month_pdf()-> Tuple[pathlib.PosixPath,pathlib.PosixPath]:
    path = create_folder()
    df = get_lastmonth_df(get_clean_data())

    plot_charts(df, path)
    create_analytics_report(path)
    return get_pdf_path(path), path

def remove_folder(path: pathlib.PosixPath):
    delete_folder(path)

def plot_charts(df: pd.DataFrame, path: pathlib.PosixPath):
    for group in different_groups:
        grouped_df = group_df(df, group)
        create_barchart(grouped_df, path, grouped_df.columns[1])

    df_aux = group_df(df, 'User', 'Type')
    dif_types = df_aux['Type'].unique()
    for i, name in enumerate(df_aux['User'].unique()): #enumerate for the plt.savefig()
        df_sub = df_aux[df_aux.User == name]
        df_sub = prepare_df(df_sub, dif_types)
        create_barchart(df_sub, path, 'Type', f"{name}'s budget", i)

    


