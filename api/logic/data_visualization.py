from typing import Optional

import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import GRAPHS_COLOR
from api.logic.clean_data import get_diferent_months
#Error solved but dont know what this does 
import matplotlib
matplotlib.use('Agg')
#-----------------------------------#
#Matplotlib parameters
plt.style.use('ggplot')
#-----------------------------------#

###### VIEJO ######
#Create Graphs
def create_barchart(df:pd.DataFrame, path: pathlib.PosixPath, column: str, 
                    title: Optional[str] = None, index:Optional[int] = None,
                    hue: Optional[str] = None, hue_order: Optional[str] = None,
                    color: Optional[str] = None,
                    ) -> None:
    filename = get_filename(column, index, hue)
    title = get_title(title, column)

    ax = sns.barplot(x=column, y='Price', data=df, estimator=sum, ci=None, color = color, hue=hue, hue_order=hue_order)
    plt.xticks(rotation=0)
    plt.ylabel('$ Money ')
    plt.xlabel(f'{column}s')
    plt.title(title)

    if not hue:
        for p in ax.patches:
            ax.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.2, p.get_height()+80))

    plt.savefig(path / filename)
    plt.close()#used bc sometimes graphs crashed without it

def get_title(title: Optional[str] = None, column: Optional[str] = None) -> str:
    if title:
        return title
    return f'Bugdet per {column.lower()}s'

def get_filename(name:str, index:int = None, hue: Optional[str] = None) -> str:
    #index can be 0 because it comes from an enumerate
    if hue:
        if index or index == 0:
            return f'user{index}-monthsbarchart.png'
        return name + '-monthsbarchart.png'
    if index or index == 0:
        return f'user{index}-barchart.png'
    return name + '-barchart.png'

###### NUEVO ######
def plot_simple_chart(df: pd.DataFrame, path: pathlib.PosixPath)->None:
    column = df.columns[1]
    filename = path / column

    ax = sns.barplot(x=column, y='Price', data=df, estimator=sum, ci=None, color = GRAPHS_COLOR)
    plt.xticks(rotation=0)
    plt.ylabel('$ Money ')
    plt.xlabel(f'{column}s')
    plt.title(f'Bugdet per {column.lower()}s')
    
    for p in ax.patches:
            ax.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.2, p.get_height()+80))
    
    plt.savefig(filename)
    plt.close()

def plot_multipleusers_simple_chart(df: pd.DataFrame, path: pathlib.PosixPath, user: str)->None:
    column = 'Type'
    filename = path / user

    ax = sns.barplot(x=column, y='Price', data=df, estimator=sum, ci=None, color = GRAPHS_COLOR)
    plt.xticks(rotation=0)
    plt.ylabel('$ Money ')
    plt.xlabel(f'{column}s')
    plt.title(f"{user}'s budget")
    
    for p in ax.patches:
            ax.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.2, p.get_height()+80))
    
    plt.savefig(filename)
    plt.close()

def plot_comparative_charts(df: pd.DataFrame, path: pathlib.PosixPath)->None:
    column = df.columns[1]
    hue="Month_year"
    hue_order= get_diferent_months(df=df)
    name = column + '-3months'
    filename = path / name

    ax = sns.barplot(x=column, y='Price', data=df, estimator=sum, ci=None, hue=hue, hue_order=hue_order)
    plt.xticks(rotation=0)
    plt.ylabel('$ Money ')
    plt.xlabel(f'{column}s')
    plt.title(f'{column} 3 month analysis')

    plt.savefig(filename)
    plt.close()

def plot_multipleusers_comparative_charts(df: pd.DataFrame, path: pathlib.PosixPath,  user: str)->None:
    column = df.columns[1]
    hue="Month_year"
    hue_order= get_diferent_months(df=df)
    name = user + '-3months'
    filename = path / name

    ax = sns.barplot(x=column, y='Price', data=df, estimator=sum, ci=None, hue=hue, hue_order=hue_order)
    plt.xticks(rotation=0)
    plt.ylabel('$ Money ')
    plt.xlabel(f'{column}s')
    plt.title(f'{column} 3 month analysis')

    plt.savefig(filename)
    plt.close()