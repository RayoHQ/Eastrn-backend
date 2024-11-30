from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.apis.api_router import api_router
from app.core.config import settings
import logging
import os
import shutil

# Initialize app
app = FastAPI(title=settings.APP_NAME, version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Restrict to frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Routers
app.include_router(api_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Interaction Backend!"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Upload directory
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Static file serving
app.mount("/uploaded_files", StaticFiles(directory=UPLOAD_DIR), name="uploaded_files")

# File upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return the public URL of the uploaded file
        public_url = f"http://127.0.0.1:8000/uploaded_files/{file.filename}"    
        return {"file_path": public_url}
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(content={"message": "Resource not found"}, status_code=404)

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(content={"message": "Internal server error"}, status_code=500)
