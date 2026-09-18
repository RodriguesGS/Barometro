from datetime import date, timedelta


def add_years(day: date, years: int) -> date:

    try:
        return day.replace(year=day.year + years)
    except ValueError:
        return day.replace(year=day.year + years, day=28)


def split_period(start: date, end: date, years: int = 10) -> list[tuple[date, date]]:

    windows = []
    cursor = start

    while cursor <= end:
        window_end = min(add_years(cursor, years) - timedelta(days=1), end)

        windows.append((cursor, window_end))
        cursor = window_end + timedelta(days=1)

    return windows
