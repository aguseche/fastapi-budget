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
plt.style.use('ggplot')


def create_barchart(df:pd.DataFrame, path: pathlib.PosixPath, column: str, title: str = None, index:int = None):
    filename = get_filename(column, index)

    #plot
    ax = sns.barplot(x=column, y='Price', data=df, estimator=sum, ci=None, color = '#4e94bb')
    plt.xticks(rotation=0)
    plt.ylabel('$ Money ')
    plt.xlabel(f'{column}s')

    set_title(title, column)

    for p in ax.patches:
        ax.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.2, p.get_height()+80))

    plt.savefig(path / filename)
    #plt.show()
    plt.close()



def set_title(title:str = None, column: str = None):
    if title:
        plt.title(f'{title}')
    else:
        plt.title(f'Bugdet per {column.lower()}s')

def get_filename(name:str, index:int = None):
    if index or index == 0:
        filename = f'user{index}-barchart.png'
    else:
        filename = name + '-barchart.png'
    return filename
