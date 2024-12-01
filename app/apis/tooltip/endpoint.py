from fastapi import APIRouter, Depends, status

from app.apis.tooltip.service import TOOLTIPService

router = APIRouter()

tooptip_service_instance = TOOLTIPService()

def get_tooltip_service():
    return tooptip_service_instance

@router.post("/tooltip", status_code=status.HTTP_200_OK, description="tooltip function")
async def tooltip(data: dict,
                  tooltip_service: TOOLTIPService = Depends(get_tooltip_service)):
    term = data.get("term")
    context = data.get("context", "")
    if not term:
        return {"error": "Term is required"}
    
    tooltip_info = tooltip_service.run_tooltip_process(term, context)
    return {"term": term, "tooltip": tooltip_info}
