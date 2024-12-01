from fastapi import APIRouter

from app.apis.summary import endpoint as summary
from app.apis.vis_summary import endpoint as vis_summary
from app.apis.keyword import endpoint as keyword_router
from app.apis.tooltip import endpoint as tooltip_router
from app.apis.navigation import endpoint as navigation_router

api_router = APIRouter()

api_router.include_router(summary.router, prefix="/summary", tags=["summary"])
api_router.include_router(vis_summary.router, prefix="/vissummary", tags=["vissummary"])

api_router.include_router(keyword_router.router, prefix="/keyword", tags=["keyword"])
api_router.include_router(tooltip_router.router, prefix="/tooltip", tags=["Tooltips"])
api_router.include_router(navigation_router.router, prefix="/navigation", tags=["navigation"])