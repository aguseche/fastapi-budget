import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
#Error solved but dont know what this does 
import matplotlib
matplotlib.use('Agg')
#-----------------------------------#
#Matplotlib parameters


def create_barchart(df:pd.DataFrame):
    #define variables
    last_month = df['Month_year'].max()
    x_value = df.columns[1]
    y_value = 'Price'
    label = x_value + 's'
    #plot
    sns.barplot(x=x_value, y=y_value, data=df, estimator=sum, ci=None)
    plt.xticks(rotation=0)
    plt.ylabel('$ Money ')
    plt.xlabel(f'{label}')
    plt.title(f'Bugdet {label.lower()} for {last_month}')
    plt.savefig(x_value)
    plt.close()