import pathlib
from typing import Optional, Tuple
import numpy as np 

import pandas as pd

from api.logic.clean_data import get_clean_data, get_month_df, group_df
from api.logic.manage_files import create_folder, delete_folder, get_pdf_path

from api.logic.generators.excel_generator import monthly_excel
from api.logic.generators.pdf_generator import create_analytics_report
from config import DIFFERENT_GROUPS
color = '#4e94bb'

from api.logic.clases import Chart

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
    plot_3month_charts(df, path)
    
    
    #Create Report
    create_analytics_report(path=path, users=df['User'].unique())

    return get_pdf_path(path), path

def plot_simple_charts(df: pd.DataFrame, path: pathlib.PosixPath) -> None:
    #Create two barcharts grouped by Type and by User
    for group in DIFFERENT_GROUPS:
        grouped_df = group_df(df, group)
        Chart(df=grouped_df, path=path).plot_chart()
    #Create barcharts per user 
    df_aux = df.groupby(['Month_year','User','Type'], as_index= False)['Price'].sum() #shouldnt be here
    for user in df_aux['User'].unique():
        df_sub = df_aux[df_aux['User']==user]
        Chart(df=df_sub, path=path, user=user).plot_chart()

def plot_3month_charts(df: pd.DataFrame, path: pathlib.PosixPath) -> None:
    for group in DIFFERENT_GROUPS:
        grouped_df = group_df(df, group)
        Chart(df=grouped_df, path=path).plot_chart()
    for user in df['User'].unique():
        df_sub = df[df.User == user].drop(columns=['Description','User'])
        Chart(df=df_sub, path=path, user=user).plot_chart()

def month_excel(file):
    path = create_folder()
    excel_path = monthly_excel(path, file)
    return excel_path, path

def remove_folder(path: pathlib.PosixPath) -> None:
    '''
    Deletes the folder used in the endpoint (its used as a BackgroudTask)
    '''
    delete_folder(path)


