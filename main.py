from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.endpoints.v1.router import router as v1_router

app = FastAPI(
    title="Templete API",
    description="Solufit Microservice Network",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(v1_router, prefix="/v1")