from openpyxl import Workbook
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.medical_hystory import MedicalHistory
from src.models.cax_code import CaxCode
from src.models.doctor import Doctor
from src.models.nurse import Nurse

async def export_medical_histories_to_excel(session: AsyncSession, file_path: str):
    stmt = (
        select(
            MedicalHistory.history_number,
            MedicalHistory.full_name,
            MedicalHistory.birth_date,
            MedicalHistory.address,
            MedicalHistory.diagnosis,
            MedicalHistory.icd10_code,
            Doctor.full_name.label("doctor_name"),
            Nurse.full_name.label("nurse_name"),
            CaxCode.cax_name,
            CaxCode.cax_code,
            MedicalHistory.admission_date,
            MedicalHistory.discharge_date
        )
        .join(Doctor, MedicalHistory.doctor_id == Doctor.id, isouter=True)
        .join(Nurse, MedicalHistory.nurse_id == Nurse.id, isouter=True)
        .join(CaxCode, MedicalHistory.cax_code_id == CaxCode.id, isouter=True)
        .where(MedicalHistory.cancelled.is_(None))
    )

    result = await session.execute(stmt)
    rows = result.all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Истории болезней"

    headers = [
        "Номер истории",
        "ФИО пациента",
        "Дата рождения",
        "Адрес",
        "Диагноз",
        "Код МКБ-10",
        "Врач",
        "Медсестра",
        "Код ЦАХ",
        "Название ЦАХ",
        "Дата поступления",
        "Дата выписки"
    ]

    ws.append(headers)

    for row in rows:
        ws.append([list(row)])

    wb.save(file_path)
    return file_path
