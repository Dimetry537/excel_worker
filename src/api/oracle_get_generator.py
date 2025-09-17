from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.db.oracle_db import get_db
from typing import Optional

router = APIRouter(prefix="/oracle", tags=["Oracle DB"])

@router.get("/oracle-test")
def oracle_test(session: Session = Depends(get_db)):
    result = session.execute(text("SELECT sysdate FROM dual"))
    row = result.fetchone()
    return {"sysdate": str(row[0])}

@router.get("/patient-search")
def search_patient(
    lastname: Optional[str] = Query(None, description="Фамилия пациента (частичное совпадение)"),
    firstname: Optional[str] = Query(None, description="Имя пациента (частичное совпадение)"),
    secondname: Optional[str] = Query(None, description="Отчество пациента (частичное совпадение)"),
    birthdate: Optional[str] = Query(None, description="Дата рождения пациента (ДД.ММ.ГГГГ)"),
    adress: Optional[str] = Query(None, description="Адрес пациента (частичное совпадение)"),
    session: Session = Depends(get_db)
):

    is_empty_query = all(param is None or param.strip() == "" for param in [lastname, firstname, secondname, birthdate, adress])

    query = text("""
        SELECT
            fn_pat_name_by_id(p.keyid) AS FIO,
            TO_CHAR(p.birthdate, 'dd.mm.yyyy') AS BD,
            p_pat.address(p.keyid) AS ADR
        FROM SOLUTION_MED.patient p
        WHERE 
            (:surname IS NULL OR p.LASTNAME LIKE NULLIF(:surname, '') || '%')
            AND (:firstName IS NULL OR p.FIRSTNAME LIKE NULLIF(:firstName, '') || '%')
            AND (:secondName IS NULL OR p.SECONDNAME LIKE NULLIF(:secondName, '') || '%')
            AND (:birthdate IS NULL OR p.birthdate = TO_DATE(NULLIF(:birthdate, ''), 'dd.mm.yyyy'))
            AND (:adress IS NULL OR p_pat.address(p.keyid) LIKE '%' || NULLIF(:adress, '') || '%')
            AND ROWNUM <= 100
        ORDER BY fn_pat_name_by_id(p.keyid)
    """)

    params = {
        "surname": lastname,
        "firstName": firstname,
        "secondName": secondname,
        "birthdate": birthdate,
        "adress": adress,
        "is_empty_query": 1 if is_empty_query else 0
    }

    try:
        result = session.execute(query, params)
        rows = result.fetchall()

        response = [
            {
                "pname": row[0],
                "birthdate": row[1],
                "address": row[2]
            } for row in rows
        ]

        return response if response else {"error": "Пациенты не найдены"}
    except Exception as e:
        return {"error": f"Ошибка базы данных: {str(e)}"}
