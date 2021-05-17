from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse

from api.logic.Controller import last_month_pdf, remove_folder
router = APIRouter()


@router.get("/")
def index():
    return {"Hello": "World"}

@router.get("/monthly-budget")
def monthly_budget(background_tasks: BackgroundTasks):#-> how can i return file type ? 
    '''
    Returns a pdf that visualizes your expenses
    '''
    pdf_path, dir_path = last_month_pdf()#this could be optimized

    #Background tasks runs AFTER returning the response
    background_tasks.add_task(remove_folder, dir_path)
    return FileResponse(path = pdf_path, filename = 'budget_report.pdf', media_type = 'pdf')