from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.db.config import settings
from src.api.doctor import router as doctor_router
from src.api.nurse import router as nurse_router
from src.api.cax_codes import router as cax_code_router
from src.api.medical_history import router as medical_history_router
from src.api.discharge_date import router as discharge_date_router
from src.api.oracle_get_generator import router as oracle_router
from src.api.tasks import router as tasks_router
from src.api.operations import router as operations_router
from src.api.patient import router as patient_router
from src.api.medical_history_report import router as medical_history_report_router
from src.api.users import router as users_router
from src.api.roles import router as roles_router
from src.api.auth import router as auth_router

app = FastAPI(title="Excel-Worker")


origins = [f"http://{settings.cors_host}:{settings.cors_port}"]

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
app.include_router(patient_router)
app.include_router(medical_history_router)
app.include_router(operations_router)
app.include_router(discharge_date_router)
app.include_router(oracle_router)
app.include_router(tasks_router)
app.include_router(medical_history_report_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(auth_router)

app.mount("/exports", StaticFiles(directory="exports"), name="exports")
