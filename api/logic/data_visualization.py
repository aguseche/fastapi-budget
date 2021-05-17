import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

#Error solved but dont know what this does 
import matplotlib
matplotlib.use('Agg')
#-----------------------------------#
#Matplotlib parameters

#should manage files from manage_files file
def create_barchart(df:pd.DataFrame, path: pathlib.PosixPath):
    #define variables
    last_month = df['Month_year'].max()
    x_value = df.columns[1]
    filename = x_value + '-barchart.png'
    y_value = 'Price'
    label = x_value + 's'
    #plot
    ax = sns.barplot(x=x_value, y=y_value, data=df, estimator=sum, ci=None)
    plt.xticks(rotation=0)
    plt.ylabel('$ Money ')
    plt.xlabel(f'{label}')
    plt.title(f'Bugdet {label.lower()} for {last_month}')

    for p in ax.patches:
        ax.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.2, p.get_height()+80))

    plt.savefig(path / filename)
    plt.close()

