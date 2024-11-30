from fastapi import APIRouter
from app.apis.keyword import router as keyword_router
from app.apis.navigation import router as navigation_router
from app.apis.tooltip import router as tooltip_router

api_router = APIRouter()

api_router.include_router(keyword_router, prefix="/keyword", tags=["keyword"])
api_router.include_router(navigation_router, prefix="/navigation", tags=["Page Navigation"])
api_router.include_router(tooltip_router, prefix="/tooltip", tags=["Tooltips"])
