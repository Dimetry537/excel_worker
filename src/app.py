from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.doctor import router as doctor_router

app = FastAPI(title="Excel-Worker")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(doctor_router)