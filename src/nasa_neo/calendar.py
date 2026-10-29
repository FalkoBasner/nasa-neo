from datetime import date, timedelta


def week_to_date_range(week: int, year: int) -> tuple[date, date]:
    monday = date.fromisocalendar(year, week, 1)
    sunday = monday + timedelta(days=6)
    return monday, sunday
