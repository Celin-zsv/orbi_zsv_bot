"""
Аналог urls
"""
from fastapi import APIRouter

from app.api.endpoints import forms_router  # импорт роутеров

main_router = APIRouter()  # главный роутер
main_router.include_router(forms_router, prefix="/form", tags=["forms"])
