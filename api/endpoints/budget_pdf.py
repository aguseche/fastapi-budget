from typing import List
from fastapi import APIRouter
#from fastapi.responses import FileResponse FileResponse('report.pdf') 

from api.logic.clean_data import get_clean_data
router = APIRouter()


@router.get("/")
def index():
    return {"Hello": "World"}

@router.get("/monthly-budget")
def monthly_budget():
    '''
    Returns a pdf that visualizes your expenses
    '''
    return get_clean_data()