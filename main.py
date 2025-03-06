from fastapi import FastAPI
import os

from api.endpoints import router as assessment_router
from config.settings import settings

app = FastAPI(title="O-1A Visa Assessment API")
app.include_router(assessment_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():

    # Set Together API key from environment variable
    os.environ["TOGETHER_API_KEY"] = settings.together_api_key
    
    # Initialize RAG system
    from pathlib import Path
    
    # Create knowledge directory if it doesn't exist
    knowledge_dir = Path(settings.knowledge_dir)
    knowledge_dir.mkdir(exist_ok=True)
    
    print(f"Application started with knowledge directory: {knowledge_dir}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)