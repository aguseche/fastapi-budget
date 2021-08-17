from fastapi import APIRouter

from api.endpoints import budget_pdf
from api.endpoints import budget_excel


api_router = APIRouter()
api_router.include_router(budget_pdf.router)
api_router.include_router(budget_excel.router)
