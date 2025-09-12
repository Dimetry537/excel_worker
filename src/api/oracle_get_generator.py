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
    lastname: Optional[str] = Query(None, description="Patient last name (partial match)"),
    firstname: Optional[str] = Query(None, description="Patient first name (partial match)"),
    secondname: Optional[str] = Query(None, description="Patient second name (partial match)"),
    birthdate: Optional[str] = Query(None, description="Patient birthdate (DD.MM.YYYY)"),
    num: Optional[str] = Query(None, description="Patient card number (partial match)"),
    session: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            fn_pat_name_by_id(p.keyid) AS FIO,
            TO_CHAR(p.birthdate, 'dd.mm.yyyy') AS BD,
            p_pat.address(p.keyid) AS ADR
        FROM SOLUTION_MED.patient p
        WHERE (:lastname IS NULL OR UPPER(p.lastname) LIKE UPPER(:lastname || '%'))
          AND (:firstname IS NULL OR UPPER(p.firstname) LIKE UPPER(:firstname || '%'))
          AND (:secondname IS NULL OR UPPER(p.secondname) LIKE UPPER(:secondname || '%'))
          AND (:birthdate IS NULL OR TO_CHAR(p.birthdate, 'dd.mm.yyyy') = :birthdate)
          AND (:num IS NULL OR EXISTS (
              SELECT 1 FROM SOLUTION_MED.pat_card pc 
              WHERE pc.id_pat = p.keyid 
                AND UPPER(pc.num) LIKE UPPER(:num || '%')
          ))
    """)

    # Параметры для SQL-запроса
    params = {
        "lastname": lastname,
        "firstname": firstname,
        "secondname": secondname,
        "birthdate": birthdate,
        "num": num
    }

    try:
        result = session.execute(query, params)
        rows = result.fetchall()

        # Форматируем результат в список словарей
        response = [
            {
                "pname": row[0],  # FIO
                "birthdate": row[1],  # BD
                "address": row[2]  # ADR
            } for row in rows
        ]

        return response if response else {"error": "No patients found"}
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}
