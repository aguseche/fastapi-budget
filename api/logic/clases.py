from dataclasses import dataclass
from typing import Optional

import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import seaborn as sns

from api.logic.clean_data import get_diferent_months
#@dataclass
class Chart:
    #Multiple users
    hue: Optional[str] = None
    hue_order: Optional[str] = None

    color: str = '#4e94bb'
    y: str = 'Price'
    df: pd.DataFrame
    path: pathlib.PosixPath 

    filename: str #1- path/column 2-path/user 3n4- (1-2)+'-3months'
    title: str #1- f'Bugdet per {column.lower()}s' 2- f"{user}'s budget" 3n4- f'{column} 3 month analysis'
    column: str

    def __init__(self,df:pd.DataFrame, path: pathlib.PosixPath, user: Optional[str] = None) -> None:
        self.df = df
        self.path = path
        #title-> ?
        self.column = df.columns[1]
        #Filename
        if user:
            self.filename = path/user
            self.title = f"{user}'s budget"
        else:
            self.filename = path/self.column
            self.title = f'Bugdet per {self.column.lower()}s'
        #Multiple users
        if len(self.df['Month_year'].unique()) >= 2:
            self.hue = 'Month_year'
            self.hue_order = get_diferent_months(df)
            self.filename =str(self.filename) + '-3months'
            self.color = None #por ahi lo re borro a esto pero quedaba mas lindo con un poco de color
            self.title = f'{self.column} 3 month analysis'

    def plot_chart(cls)->None:
        ax = sns.barplot(x=cls.column, y='Price', data=cls.df, estimator=sum, ci=None, hue = cls.hue, hue_order=cls.hue_order)
        plt.xticks(rotation=0)
        plt.ylabel('$ Money ')
        plt.title(cls.title)

        if len(cls.df['Month_year'].unique()) == 1:
            plt.xlabel(f'{cls.column}s')
            for p in ax.patches:
                ax.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.2, p.get_height()+80))


        plt.savefig(cls.filename)
        plt.close()
