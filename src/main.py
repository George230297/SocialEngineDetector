from fastapi import FastAPI
from src.core.config import settings
from src.api.v1.endpoints import scan

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include routers
app.include_router(scan.router, prefix=f"{settings.API_V1_STR}/scan", tags=["scan"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Social Engineering Detector API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
