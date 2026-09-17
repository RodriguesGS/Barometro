from datetime import date

from barometro.periods import split_period


def test_period_shorter_than_window():
    
    windows = split_period(date(2026, 1, 1), date(2026, 1, 31))
    
    assert windows == [(date(2026, 1, 1), date(2026, 1, 31))]
    