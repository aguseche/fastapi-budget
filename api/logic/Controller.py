import pathlib
from typing import Tuple
import numpy as np

import pandas as pd

from api.logic.clean_data import get_clean_data, get_month_df, group_df, prepare_df
from api.logic.data_visualization import create_barchart
from api.logic.pdf_generator import create_analytics_report
from api.logic.manage_files import create_folder, delete_folder, get_pdf_path

different_groups = ['User', 'Type'] #should i import this from a config file ?
color = '#4e94bb'

def last_month_pdf(file)-> Tuple[pathlib.PosixPath,pathlib.PosixPath]:
    '''
    Creates all the charts needed, then generates the PDF report
    '''
    path = create_folder()
    df = get_clean_data(file)
    last_month_df = get_month_df(df)#get data from last month
    plot_charts(last_month_df, path)
    plot_3month_charts(df, path)
    create_analytics_report(path)
    #returns two paths, 1st for the PDF file and 2nd for the folder (in order to remove it later)
    return get_pdf_path(path), path 



def last_month_excel(file):
    path = create_folder()
    df = get_month_df(get_clean_data(file))#get data from last month
    df = df.sort_values(['User', 'Description'], ascending=[True, True])
    excel_path = path / 'Tabla.xlsx'
    df.to_excel(excel_path, index = False)
    return excel_path, path

def plot_charts(df: pd.DataFrame, path: pathlib.PosixPath) -> None:
    #Create two barcharts grouped by Type and by User
    for group in different_groups:
        grouped_df = group_df(df, group)
        create_barchart(grouped_df, path, grouped_df.columns[1], color = color)

    #Create barcharts per user 
    df_aux = group_df(df, 'User', 'Type')
    dif_types = df_aux['Type'].unique()
    for i, name in enumerate(df_aux['User'].unique()): #i is used to save the chart file
        df_sub = df_aux[df_aux.User == name]
        df_sub = prepare_df(df_sub, dif_types)
        create_barchart(df_sub, path, 'Type', f"{name}'s budget", i, color = color)

def plot_3month_charts(df: pd.DataFrame, path: pathlib.PosixPath) -> None:
    dif_months = np.array(df['Month_year'].unique())
    dif_months.sort()
    dif_months = dif_months[-3:]

    for group in different_groups:
        create_barchart(df, path, group, title = f"{group} 3 month analysis",hue="Month_year", hue_order=dif_months)
    
    dif_types = df['Type'].unique()
    for i, name in enumerate(df['User'].unique()): #i is used to save the chart
        df_sub = df[df.User == name].drop(columns='Description')
        create_barchart(df_sub, path, 'Type', f"{name}'s budget", i,hue="Month_year", hue_order=dif_months)

def remove_folder(path: pathlib.PosixPath) -> None:
    '''s
    Deletes the folder used in the endpoint (its used as a BackgroudTask)
    '''
    delete_folder(path)