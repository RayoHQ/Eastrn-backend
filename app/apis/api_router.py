from fastapi import APIRouter

from app.apis.summary import endpoint as summary
from app.apis.vis_summary import endpoint as vis_summary

api_router = APIRouter()

api_router.include_router(summary.router, prefix="/summary", tags=["summary"])
api_router.include_router(vis_summary.router, prefix="/vissummary", tags=["vissummary"])
