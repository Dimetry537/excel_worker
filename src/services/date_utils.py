from datetime import date, timedelta
import holidays

RU_HOLIDAYS = holidays.Russia()

def calculate_discharge_date(admission_date: date, quantity_of_days: int) -> date:
    current_date = admission_date
    days_counted = 0

    while days_counted < quantity_of_days:
        current_date += timedelta(days=1)

        if current_date.weekday() < 5:
            continue
        if current_date in RU_HOLIDAYS:
            continue

        added_days += 1

    return current_date
