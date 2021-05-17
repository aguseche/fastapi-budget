from config import data_path
import pandas as pd
#from pandas.core.frame import DataFrame

#Might be used for multiple paths / files in the future
def load_relevant_data():
    return pd.read_csv(data_path, header=None)

def get_clean_data():
    
    df = load_relevant_data()
    #Drop unnecessary columns and rows
    df.drop(df.columns[[1,2]], axis = 1, inplace = True) 
    df = df.iloc[1:]

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

    #rephrase date 
    df['Date'] = df['Date'].str.replace('[', '', regex=True)

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
    df['Type'] = df['Type'].apply(lambda x: x[:-1] if x[-1] == 's' else x)
    return df

def get_lastmonth_df(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Retrieves a DataFrame with last month values only ('Month_Year' column)
    '''
    return df.loc[df['Month_year'] == df['Month_year'].max()] #devuelvo df con solo las que sean del ultimo mes

def group_df(df: pd.DataFrame, group2: str, group1: str = 'Month_year') -> pd.DataFrame:
    '''
    Retreives a dataframe grouped by 'Month_year' column and a second one specified in group2
    Dataframe has values Group2 and Price
    '''
    return df.groupby([group1,group2], as_index= False)['Price'].sum()
