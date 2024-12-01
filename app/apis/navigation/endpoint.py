from fastapi import APIRouter, Depends, status

from app.apis.navigation.service import NAVIGATIONService

router = APIRouter()

navigation_sercice_instance = NAVIGATIONService()

def get_navigation_service():
    return navigation_servicce_instance

@router.get("/{page_number}", status_code=status.HTTP_200_OK, description="navigation function")
async def navigate(pdf_path: str, 
             page_number: int,
             navigation_service: NAVIGATIONService = Depends(get_navigation_service)):
    
    response = navigation_service.get_page_preview(pdf_path, page_number)
    return response
