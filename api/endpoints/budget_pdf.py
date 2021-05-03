from typing import List
from fastapi import APIRouter
import tempfile
from fastapi.responses import FileResponse

from api.logic.clean_data import get_clean_data, get_lastmonth_grouped_df
from api.logic.data_visualization import create_barchart
from api.logic.pdf_generator import create_analytics_report

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
    with tempfile.TemporaryDirectory(dir = 'response') as tmpdir:
        #this should be a function that graphs every chart
        create_barchart(get_lastmonth_grouped_df(df, 'Type'), tmpdir)
        create_barchart(get_lastmonth_grouped_df(df, 'User'), tmpdir)
        create_analytics_report(tmpdir)
        return FileResponse(path = 'budget_report.pdf', filename = 'budget_report.pdf', media_type = 'pdf')