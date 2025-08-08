from datetime import date, timedelta
import holidays

RU_HOLIDAYS = holidays.RU()

def calculate_discharge_date(admission_date: date, quantity_of_days: int) -> date:
    max_date = admission_date + timedelta(days=quantity_of_days)

    discharge_date = max_date

    while discharge_date.weekday() >= 5 or discharge_date in RU_HOLIDAYS:
        discharge_date -= timedelta(days=1)

    return discharge_date
