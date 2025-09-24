from openpyxl import Workbook
from openpyxl.styles import NamedStyle
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import os

from src.models.medical_hystory import MedicalHistory
from src.models.cax_code import CaxCode
from src.models.doctor import Doctor
from src.models.nurse import Nurse

async def export_medical_histories_to_excel(session: AsyncSession, directory: str = "exports") -> str:
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

    date_style = NamedStyle(name="date", number_format="DD.MM.YYYY")

    for row in rows:
        ws.append(list(row))

    for row in ws.iter_rows(min_row=2, max_col=12):
        row[2].style = date_style
        row[10].style = date_style
        row[11].style = date_style

    column_widths = {
        'A': 15,
        'B': 30,
        'C': 15,
        'D': 40,
        'E': 40,
        'F': 15,
        'G': 30,
        'H': 30,
        'I': 15,
        'J': 30,
        'K': 15,
        'L': 15
    }

    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    wb.save(file_path)
    return file_path
