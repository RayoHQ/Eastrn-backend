from fastapi import APIRouter

from app.apis.summary import endpoint as summary

api_router = APIRouter()

api_router.include_router(summary.router, prefix="/summary", tags=["summary"])
