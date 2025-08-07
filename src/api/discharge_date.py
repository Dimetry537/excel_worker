from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.db.base import get_async_session
from src.models.cax_code import CaxCode
from src.services.date_utils import calculate_discharge_date
from src.schemas.discharge_date import DischargeDateRequest, DischargeDateResponse

router = APIRouter(prefix="/dates", tags=["dates"])


@router.post("/suggest_discharge_date", response_model=DischargeDateResponse)
async def suggest_discharge_date(
    payload: DischargeDateRequest,
    session: AsyncSession = Depends(get_async_session)
):
    cax_code = await session.get(CaxCode, payload.cax_code_id)
    if not cax_code:
        raise HTTPException(status_code=404, detail="ЦАХ не найден")

    discharge_date = calculate_discharge_date(
        payload.admission_date,
        cax_code.quantity_of_days
    )

    return DischargeDateResponse(discharge_date=discharge_date)
