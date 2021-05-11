import pathlib
from typing import Tuple

from api.logic.clean_data import get_clean_data, get_lastmonth_grouped_df
from api.logic.data_visualization import create_barchart
from api.logic.pdf_generator import create_analytics_report
from api.logic.manage_files import create_folder, delete_folder, get_pdf_path

different_groups = ['Type', 'User']

def last_month_pdf()-> Tuple[pathlib.PosixPath,pathlib.PosixPath]:
    #create folder
    df = get_clean_data()
    path = create_folder()
    for group in different_groups:
        create_barchart(get_lastmonth_grouped_df(df, group), path)

    create_analytics_report(path)
    return get_pdf_path(path), path

def remove_folder(path: pathlib.PosixPath):
    delete_folder(path)

