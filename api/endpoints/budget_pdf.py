from typing import List
from fastapi import APIRouter
import tempfile

from api.logic.clean_data import get_clean_data, get_lastmonth_grouped_df
from api.logic.data_visualization import create_barchart
from api.logic.pdf_generator import create_pdf
router = APIRouter()


@router.get("/")
def index():
    return {"Hello": "World"}

@router.get("/monthly-budget")
def monthly_budget():
    '''
    Returns a pdf that visualizes your expenses
    '''
    df = get_clean_data()
    #this should be a function that graphs every chart
    create_barchart(get_lastmonth_grouped_df(df, 'Type'))
    create_barchart(get_lastmonth_grouped_df(df, 'User'))
    return 1