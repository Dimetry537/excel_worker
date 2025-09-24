from openpyxl import Workbook
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date
import os

from src.models.medical_hystory import MedicalHistory
from src.models.cax_code import CaxCode
from src.models.doctor import Doctor
from src.models.nurse import Nurse


def prepare_value(v):
    if v is None:
        return ""
    if isinstance(v, date) and not isinstance(v, datetime):
        return datetime.combine(v, datetime.min.time())
    return v


async def export_medical_histories_to_excel(
    session: AsyncSession, directory: str = "exports"
) -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(directory, f"medical_histories_{timestamp}.xlsx")

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
            MedicalHistory.discharge_date,
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
        "Название ЦАХ",
        "Код ЦАХ",
        "Дата поступления",
        "Дата выписки",
    ]
    ws.append(headers)

    for row in rows:
        ws.append([prepare_value(v) for v in row])

    # Форматирование дат
    for row in ws.iter_rows(min_row=2, max_col=12):
        birth_date_cell = row[2]   # колонка C (дата рождения)
        admission_cell = row[10]  # колонка K (дата поступления)
        discharge_cell = row[11]  # колонка L (дата выписки)

        if isinstance(birth_date_cell.value, (datetime, date)):
            birth_date_cell.number_format = "DD.MM.YYYY"
        if isinstance(admission_cell.value, (datetime, date)):
            admission_cell.number_format = "DD.MM.YYYY"
        if isinstance(discharge_cell.value, (datetime, date)):
            discharge_cell.number_format = "DD.MM.YYYY"

    # Ширина колонок
    column_widths = {
        "A": 15,
        "B": 30,
        "C": 15,
        "D": 40,
        "E": 40,
        "F": 15,
        "G": 30,
        "H": 30,
        "I": 30,
        "J": 15,
        "K": 15,
        "L": 15,
    }
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    wb.save(file_path)
    return file_path
