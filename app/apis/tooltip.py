from fastapi import APIRouter
from app.services.tooltip_service import get_tooltip_from_hyperbolic

router = APIRouter()

@router.post("/tooltip")
def tooltip(data: dict):
    term = data.get("term")
    context = data.get("context", "")
    if not term:
        return {"error": "Term is required"}
    
    tooltip_info = get_tooltip_from_hyperbolic(term, context)
    return {"term": term, "tooltip": tooltip_info}
