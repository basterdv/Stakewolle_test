from fastapi import FastAPI
from app.api.v1.api import api_router # Файл, где собраны все роутеры через include_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs" # Swagger UI
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
