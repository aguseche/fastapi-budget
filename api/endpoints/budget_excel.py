from typing import Optional
from fastapi import APIRouter, BackgroundTasks, UploadFile, File
from fastapi.responses import FileResponse

from api.logic.Controller import remove_folder, month_excel
router = APIRouter()

@router.post('/monthly-excel')
async def monthly_excel(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    '''
    Returns an excel that visualizes expenses
    '''
    excel_path, dir_path = month_excel(file.file)

    #Background tasks runs AFTER returning the response
    background_tasks.add_task(remove_folder, dir_path)
    return FileResponse(path = excel_path, filename = 'budget_excel.xlsx', media_type = 'xlsx')