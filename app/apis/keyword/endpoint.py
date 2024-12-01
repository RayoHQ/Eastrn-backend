from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.apis.keyword.service import KEYWORDService

import os

router = APIRouter()

UPLOAD_DIR = "uploaded_files"  # Matches the upload directory in `main.py`

# Instantiate the service
keyword_service_instance = KEYWORDService()

# Dependency to provide the service
def get_keyword_service():
    return keyword_service_instance

# Define a Pydantic model for payload validation
class KeywordSearchRequest(BaseModel):
    pdf_path: str
    keyword: str

@router.post("/", status_code=status.HTTP_200_OK, description="search_keyword function")
async def search_keyword(
    request: KeywordSearchRequest,
    keyword_service: KEYWORDService = Depends(get_keyword_service)
):
    pdf_path = request.pdf_path
    keyword = request.keyword
    
    # Convert public URL to local file path
    if pdf_path.startswith("http://127.0.0.1:8000/uploaded_files/"):
        local_path = pdf_path.replace("http://127.0.0.1:8000/uploaded_files/", UPLOAD_DIR + "/")
    else:
        local_path = pdf_path

    print(f"로컬 패스 : {local_path}")

    # Check if the file exists locally
    if not os.path.exists(local_path):
        return JSONResponse(content={"error": "PDF file not found"}, status_code=404)

    try:
        # Call the asynchronous service function with `await`
        print(f"22로컬 패스 : {local_path}")
        print(f"키워드 : {keyword}")

        results = await keyword_service.run_keyword_process(local_path, keyword)
        return {"keyword": keyword, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
