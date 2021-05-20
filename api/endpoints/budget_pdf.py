from api.logic.clean_data import get_clean_data
import pandas as pd
from fastapi import APIRouter, BackgroundTasks, UploadFile, File
from fastapi.responses import FileResponse

from api.logic.Controller import last_month_pdf, remove_folder
router = APIRouter()


@router.get('/')
def HelloWorld():
    return {'Hello': 'World'}


@router.get("/monthly-budget")
def monthly_budget(background_tasks: BackgroundTasks):#-> how can i return file type ? 
    '''
    Returns a pdf that visualizes expenses
    '''
    pdf_path, dir_path = last_month_pdf()#this could be optimized

    #Background tasks runs AFTER returning the response
    background_tasks.add_task(remove_folder, dir_path)
    return FileResponse(path = pdf_path, filename = 'budget_report.pdf', media_type = 'pdf')

@router.post('/csv')
async def parsecsv(file: UploadFile = File(...)):
    dataframe = pd.DataFrame(file.file)
    dataframe.to_csv('dffastapi.csv', header = None)
    print(dataframe)
    return dataframe