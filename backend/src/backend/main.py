from fastapi import FastAPI, HTTPException
from backend.api.endpoints import router

app = FastAPI(title="RAG Virtual Assistant")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "RAG Virtual Assistant API is running."}