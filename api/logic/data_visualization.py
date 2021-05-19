from typing import Optional

import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Error solved but dont know what this does 
import matplotlib
matplotlib.use('Agg')
#-----------------------------------#
#Matplotlib parameters
plt.style.use('ggplot')
#-----------------------------------#

def create_barchart(df:pd.DataFrame, path: pathlib.PosixPath, column: str, 
                    title: Optional[str] = None, index:Optional[int] = None) -> None:
    filename = get_filename(column, index)
    title = get_title(title, column)

    ax = sns.barplot(x=column, y='Price', data=df, estimator=sum, ci=None, color = '#4e94bb')
    plt.xticks(rotation=0)
    plt.ylabel('$ Money ')
    plt.xlabel(f'{column}s')
    plt.title(title)

    for p in ax.patches:
        ax.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.2, p.get_height()+80))

    plt.savefig(path / filename)
    plt.close()#used bc sometimes graphs crashed without it

def get_title(title: Optional[str] = None, column: Optional[str] = None) -> str:
    if title:
        return title
    return f'Bugdet per {column.lower()}s'

def get_filename(name:str, index:int = None) -> str:
    #index can be 0 because it comes from an enumerate
    if index or index == 0:
        return f'user{index}-barchart.png'
    return name + '-barchart.png'
