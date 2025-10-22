from io import BytesIO
from pathlib import Path
from docxtpl import DocxTemplate
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.medical_history_repository import MedicalHistoryRepository
from src.repository.operation_repository import OperationRepository
from src.repository.doctor_repository import DoctorRepository
from src.repository.nurse_repository import NurseRepository
from src.repository.cax_code_repository import CaxCodeRepository

TEMPLATE_PATH = Path(__file__).parent.parent / 'templates' / 'medical_history_template.docx'

async def generate_medical_history_report(session: AsyncSession, history_id: int) -> BytesIO:
    history_repo = MedicalHistoryRepository(session)
    operation_repo = OperationRepository(session)
    doctor_repo = DoctorRepository(session)
    nurse_repo = NurseRepository(session)
    cax_repo = CaxCodeRepository(session)

    history = await history_repo.get_by_id(history_id)
    if not history:
        raise ValueError("Медицинская история не найдена")

    operations = await operation_repo.get_by_history_id(history_id)
    doctor = await doctor_repo.get_by_id(history.doctor_id)
    nurse = await nurse_repo.get_by_id(history.nurse_id)
    cax = await cax_repo.get_by_id(history.cax_code_id)

    first_operation = operations[0] if operations else None

    if not history.patient:
        raise ValueError("Пациент не найден для этой истории")

    context = {
        'history_number': history.history_number,
        'patient_full_name': history.patient.full_name,
        'birth_date': history.patient.birth_date.strftime('%d.%m.%Y'),
        'patient_adress': history.patient.adress,
        'work_place': history.patient.workplace if history.patient.workplace else 'Не указано',
        'admission_date': history.admission_date.strftime('%d.%m.%Y'),
        'discharge_date': history.discharge_date.strftime('%d.%m.%Y') if history.discharge_date else 'Не указана',
        'diagnosis': history.diagnosis,
        'icd10': history.icd10_code,
        'cax_number': cax.cax_code if cax else 'Не указан',
        'doctor': doctor.full_name if doctor else 'Не указан',
        'nurse': nurse.full_name if nurse else 'Не указан',
        'operation_number': first_operation.id if first_operation else 'Не указан',
        'operation_date': first_operation.created_at.strftime('%d.%m.%Y') if first_operation and first_operation.created_at else 'Не указана',
        'operation_name': first_operation.oper_name if first_operation else 'Не указано',
        'operation_protocol': first_operation.oper_protocol if first_operation else 'Не указано'
    }

    doc = DocxTemplate(TEMPLATE_PATH)
    doc.render(context)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
