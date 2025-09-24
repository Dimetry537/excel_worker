from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import get_async_session
from src.services.excel_service import export_medical_histories_to_excel
import os

router = APIRouter(prefix="/excel", tags=["excel"])

@router.get("/export")
async def export_to_excel(db: AsyncSession = Depends(get_async_session)):
    try:
        print(f"export_medical_histories_to_excel: {export_medical_histories_to_excel}")
        print(f"db: {db}")
        file_path = await export_medical_histories_to_excel(db)
        
        response = FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        @response.background
        async def cleanup():
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {str(e)}")
                
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании Excel-файла: {str(e)}")
