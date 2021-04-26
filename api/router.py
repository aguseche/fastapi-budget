from fastapi import APIRouter

from api.endpoints import budget_pdf

api_router = APIRouter()
api_router.include_router(budget_pdf.router)