from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.doctor import router as doctor_router
from src.api.nurse import router as nurse_router
from src.api.cax_codes import router as cax_code_router
from src.api.medical_history import router as medical_history_router
from src.api.discharge_date import router as discharge_date_router
from src.api.oracle_get_generator import router as oracle_router
from src.api.excel import router as excel_router

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
app.include_router(nurse_router)
app.include_router(cax_code_router)
app.include_router(medical_history_router)
app.include_router(discharge_date_router)
app.include_router(oracle_router)
app.include_router(excel_router)
