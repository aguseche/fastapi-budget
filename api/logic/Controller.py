import pathlib
from typing import Optional, Tuple
import numpy as np 

import pandas as pd

from api.logic.clean_data import get_clean_data, get_month_df, group_df, prepare_df
from api.logic.data_visualization import create_barchart, plot_multipleusers_simple_chart, plot_simple_chart, plot_comparative_charts, plot_multipleusers_comparative_charts
from api.logic.manage_files import create_folder, delete_folder, get_pdf_path

from api.logic.generators.excel_generator import monthly_excel
from api.logic.generators.pdf_generator import create_analytics_report
from config import DIFFERENT_GROUPS
color = '#4e94bb'

def month_pdf(file)-> Tuple[pathlib.PosixPath,pathlib.PosixPath]:
#returns two paths, 1st for the PDF file and 2nd for the folder (in order to remove it later)
    '''
    Creates all the charts needed, then generates the PDF report
    '''
    #Manage Files
    path = create_folder()
    #Get Clean Data
    df = get_clean_data(file)
    last_month_df = get_month_df(df)#get data from last month
    #Create Graphs
    plot_simple_charts(last_month_df, path)
    plot_3month_charts_new(df, path)#revisar
    #Create Report
    create_analytics_report(path=path, users=df['User'].unique())

    return get_pdf_path(path), path


def plot_simple_charts(df: pd.DataFrame, path: pathlib.PosixPath) -> None:
    #Create two barcharts grouped by Type and by User
    for group in DIFFERENT_GROUPS: # importar de config 
        grouped_df = group_df(df, group)
        plot_simple_chart(df=grouped_df, path=path)
    #Create barcharts per user 
    df_aux = group_df(df, 'User', 'Type')
    dif_types = df_aux['Type'].unique()
    for user in df_aux['User'].unique():
        df_sub = df_aux[df_aux.User == user]
        df_sub = prepare_df(df_sub, dif_types)
        plot_multipleusers_simple_chart(df=df_sub, path=path, user=user)

def plot_3month_charts_new(df: pd.DataFrame, path: pathlib.PosixPath) -> None:
    for group in DIFFERENT_GROUPS:
        grouped_df = group_df(df, group)
        plot_comparative_charts(df=grouped_df, path=path)
    
    for user in df['User'].unique():
        df_sub = df[df.User == user].drop(columns='Description')
        plot_multipleusers_comparative_charts(df=df_sub, path=path, user=user)

# def plot_3month_charts(df: pd.DataFrame, path: pathlib.PosixPath) -> None:
#     dif_months = np.array(df['Month_year'].unique())
#     dif_months.sort()
#     dif_months = dif_months[-3:]

#     for group in DIFFERENT_GROUPS:
#         create_barchart(df, path, group, title = f"{group} 3 month analysis",hue="Month_year", hue_order=dif_months)
    
#     dif_types = df['Type'].unique()
#     for i, name in enumerate(df['User'].unique()): #i is used to save the chart
#         df_sub = df[df.User == name].drop(columns='Description')
#         create_barchart(df_sub, path, 'Type', f"{name}'s budget", i,hue="Month_year", hue_order=dif_months)


def month_excel(file, month:Optional[int]):
    path = create_folder()
    excel_path = monthly_excel(path, file, month)
    return excel_path, path

def remove_folder(path: pathlib.PosixPath) -> None:
    '''
    Deletes the folder used in the endpoint (its used as a BackgroudTask)
    '''
    delete_folder(path)


