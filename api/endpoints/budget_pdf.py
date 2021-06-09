from api.logic.clean_data import get_clean_data
import pandas as pd
from fastapi import APIRouter, BackgroundTasks, UploadFile, File
from fastapi.responses import FileResponse

from api.logic.Controller import last_month_pdf, remove_folder, last_month_excel
from api.logic.clean_data import get_clean_data
router = APIRouter()


@router.get('/')
def HelloWorld():
    return {'Hello': 'World'}


@router.post("/monthly-budget")
def monthly_budget(background_tasks: BackgroundTasks, file: UploadFile = File(...)):#-> how can i return file type ? 
    '''
    Returns a pdf that visualizes expenses
    '''
    pdf_path, dir_path = last_month_pdf(file.file)#this could be optimized

    #Background tasks runs AFTER returning the response
    background_tasks.add_task(remove_folder, dir_path)
    return FileResponse(path = pdf_path, filename = 'budget_report.pdf', media_type = 'pdf')

@router.post('/monthly-excel')
async def monthly_excel(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    '''
    Returns an excel that visualizes expenses
    '''
    excel_path, dir_path = last_month_excel(file.file)

    #Background tasks runs AFTER returning the response
    background_tasks.add_task(remove_folder, dir_path)
    return FileResponse(path = excel_path, filename = 'budget_excel.xlsx', media_type = 'xlsx')