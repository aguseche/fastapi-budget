from typing import Optional
import pandas as pd
import numpy as np
import datetime as dt
from config import data_path

def get_clean_data(file) -> None:
    df = pd.DataFrame(file)

    #delete first row (automatically generated from whatsapp)
    df = df.iloc[1:]
    #decode
    df[0] = df[0].str.decode('utf-8')

    #Separate into 5 different columns and rename
    df = df[0].str.split(' ', n =5, expand=True)
    df.rename(columns={0:'Date', 1:'Time', 2: 'User', 3:'Price', 4:'Type', 5:'Description'}, inplace=True)

    #Set Price type to float64
    #So we make NaN the ones that cant be converted and further use numbers properties with the df
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    #Set NaN rows with Price < 0
    df['Price'] = df['Price'][df['Price'] > 0]  

    #Delete rows where user, price or type are none / nan
    df = df.mask(df.eq('None')).dropna(subset=['User','Price','Type'])

    #Drop time since not needed
    df.drop(['Time'], axis = 1, inplace = True) 

    #rephrase date and description
    df['Date'] = df['Date'].str.replace('[', '', regex=True)
    df = df.replace('\\n',' ', regex=True)
    df = df.replace('\\r',' ', regex=True) 
    df['Type'] = df['Type'].str.rstrip()
    df['Description'] = df['Description'].str.rstrip()

    #Convert type to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors="coerce",dayfirst=True)    
    #Rephrase user
    df['User'] = df['User'].str.replace(':','')

    #Set Type and Description to Lower Case
    df['Type'] = df['Type'].str.lower()
    df['Description'] = df['Description'].str.lower()

    df['Month_year'] = pd.to_datetime(df['Date']).dt.to_period('M')
    # Drop date becouse not used in this version
    df.drop('Date', axis=1, inplace=True)

    #Temporary remove plurals
    df['Type'] = df['Type'].apply(remove_plurals)

    return df

def get_month_df(df: pd.DataFrame, month: Optional[str] = None) -> pd.DataFrame:
    '''
    Retrieves a DataFrame with certain month values only ('Month_Year' column)
    If month not given, retreives last month data
    '''
    #2021-04 str
    if not month:
        month = df['Month_year'].max()
    return df[df['Month_year'] == month]

def group_df(df: pd.DataFrame, group2: str, group1: str = 'Month_year') -> pd.DataFrame:
    '''
    Retreives a dataframe with the sum of Price, grouped by group1 and group2
    '''
    return df.groupby([group1,group2], as_index= False)['Price'].sum()

#This function is used in order to create uniform charts
def prepare_df(df:pd.DataFrame, dif_types:np.ndarray) -> pd.DataFrame:
    '''
    Returns a dataframe with columns Type and Price.
    Type has all the diferent posible types 
    '''
    df_aux = pd.DataFrame(dif_types, columns = ['Type'])
    df_aux['Price'] = 0.0
    #Merge, delete unused column, fillnan with 0 and rename column
    df_aux = df_aux.merge(df, how='left', on='Type').drop(columns='Price_x').fillna(0).rename(columns={'Price_y':'Price'})
    return df_aux

def get_diferent_months(df:pd.DataFrame):
    dif_months = np.array(df['Month_year'].unique())
    dif_months.sort()
    dif_months = dif_months[-3:]
    return dif_months

#Lambda Function
def remove_plurals(x):
    if len(x) >= 2:
        if x[-1] =='s':
            return x[:-1]
    return x