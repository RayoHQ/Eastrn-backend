from fastapi import APIRouter, Depends, status

from app.apis.summary.service import SUMMARYService

router = APIRouter()

summary_service_instance = SUMMARYService()

def get_summary_service():
    return summary_service_instance

@router.get("", status_code=status.HTTP_200_OK, description="1. Summary function")
async def summary(text: str,
                summary_service: SUMMARYService = Depends(get_summary_service)):

    return await summary_service.run_summary_process(text=text)