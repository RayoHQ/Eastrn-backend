from fastapi import APIRouter, Depends, status

from app.apis.vis_summary.service import VISSUMMARYService

router = APIRouter()

vis_summary_service_instance = VISSUMMARYService()

def get_vis_summary_service():
    return vis_summary_service_instance

@router.get("", status_code=status.HTTP_200_OK, description="2. Visual Summary function")
async def summary(text: str,
                vis_summary_service: VISSUMMARYService = Depends(get_vis_summary_service)):

    return await vis_summary_service.run_vissummary_process(text=text)