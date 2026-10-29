from datetime import date
from nasa_neo.calendar import week_to_date_range

def test_week_1_starts_in_previous_year():
    # ISO week 1 of 2025 starts Mon Dec 30, 2024
    start, end = week_to_date_range(1, 2025)
    assert start == date(2024, 12, 30)
    assert end == date(2025, 1, 5)

def test_week_1_of_2026():
    # ISO week 1 of 2026 starts Mon Dec 29 2025
    start, end = week_to_date_range(1, 2026)
    assert start == date(2025, 12, 29)
    assert end == date(2026, 1, 4)

def test_week_mid_year():
    start, end = week_to_date_range(10, 2026)
    assert start == date(2026, 3, 2)
    assert end == date(2026, 3, 8)

def test_week_52_year_end():
    start, end = week_to_date_range(52, 2026)
    assert start == date(2026, 12, 21)
    assert end == date(2026, 12, 27)
