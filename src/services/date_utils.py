from datetime import date, timedelta
import holidays

RU_HOLIDAYS = holidays.RU()

def calculate_discharge_date(admission_date: date, quantity_of_days: int) -> date:
    target_date = admission_date + timedelta(days=quantity_of_days)

    while target_date.weekday() >= 5 or target_date in RU_HOLIDAYS:
        target_date += timedelta(days=1)

    return target_date