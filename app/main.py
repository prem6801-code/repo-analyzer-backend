from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="GitHub Repo Analyzer", description="A FastAPI application to analyze GitHub repositories.", version="1.0.0")
app.include_router(router,prefix="/repo-analyzer", tags=["Repo Analyzer"])

@app.get("/repo-analyzer")
async def root():
    return {"message": "Welcome to the GitHub Repo Analyzer API!"}