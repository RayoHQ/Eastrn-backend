from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.keyword_service import search_keywords
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_files"  # Matches the upload directory in `main.py`

# Define a Pydantic model for payload validation
class KeywordSearchRequest(BaseModel):
    pdf_path: str
    keyword: str

@router.post("/")
async def search_keyword(request: KeywordSearchRequest):
    pdf_path = request.pdf_path
    keyword = request.keyword
    
    # Convert public URL to local file path
    if pdf_path.startswith("http://127.0.0.1:8000/uploaded_files/"):
        local_path = pdf_path.replace("http://127.0.0.1:8000/uploaded_files/", UPLOAD_DIR + "/")
    else:
        local_path = pdf_path

    # Check if the file exists locally
    if not os.path.exists(local_path):
        return JSONResponse(content={"error": "PDF file not found"}, status_code=404)

    try:
        # Delegate the keyword search to the service function
        results = search_keywords(local_path, keyword)
        return {"keyword": keyword, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
