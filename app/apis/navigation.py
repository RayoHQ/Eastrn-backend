from fastapi import APIRouter
from app.services.navigation_service import get_page_preview

router = APIRouter()

@router.get("/{page_number}")
def navigate(pdf_path: str, page_number: int):
    response = get_page_preview(pdf_path, page_number)
    return response
