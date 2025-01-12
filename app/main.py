from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import code_routes

app = FastAPI(title="Code Mentor Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(code_routes.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Code Mentor Bot"} 