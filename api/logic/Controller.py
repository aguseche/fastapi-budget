import pathlib
from typing import Tuple

import pandas as pd

from api.logic.clean_data import get_clean_data, get_lastmonth_df, group_df, prepare_df
from api.logic.data_visualization import create_barchart
from api.logic.pdf_generator import create_analytics_report
from api.logic.manage_files import create_folder, delete_folder, get_pdf_path

different_groups = ['User', 'Type'] #should i import this from a config file ?

def last_month_pdf()-> Tuple[pathlib.PosixPath,pathlib.PosixPath]:
    '''
    Creates all the charts needed, then generates the PDF report
    '''
    path = create_folder()

    df = get_lastmonth_df(get_clean_data())#get data from last month
    plot_charts(df, path)
    create_analytics_report(path)
    #returns two paths, 1st for the PDF file and 2nd for the folder (in order to remove it later)
    return get_pdf_path(path), path 

def plot_charts(df: pd.DataFrame, path: pathlib.PosixPath) -> None:
    #Create two barcharts grouped by Type and by User
    for group in different_groups:
        grouped_df = group_df(df, group)
        create_barchart(grouped_df, path, grouped_df.columns[1])

    #Create barcharts per user 
    df_aux = group_df(df, 'User', 'Type')
    dif_types = df_aux['Type'].unique()
    for i, name in enumerate(df_aux['User'].unique()): #i is used to save the chart
        df_sub = df_aux[df_aux.User == name]
        df_sub = prepare_df(df_sub, dif_types)
        create_barchart(df_sub, path, 'Type', f"{name}'s budget", i)


def remove_folder(path: pathlib.PosixPath) -> None:
    '''
    Deletes the folder used in the endpoint (its used as a BackgroudTask)
    '''
    delete_folder(path)