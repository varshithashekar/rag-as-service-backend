from fastapi import FastAPI
from backend.api.datasource_routes import router as datasource_router

app = FastAPI(title="RAG Service")

app.include_router(datasource_router)

@app.get("/health")
def health():
    return {"status": "ok"}