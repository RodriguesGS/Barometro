from datetime import date

from barometro.periods import split_period


def test_period_shorter_than_window():

    windows = split_period(date(2026, 1, 1), date(2026, 1, 31))

    assert windows == [(date(2026, 1, 1), date(2026, 1, 31))]


def test_period_equal_to_window():

    windows = split_period(date(2015, 1, 1), date(2024, 12, 31))

    assert windows == [(date(2015, 1, 1), date(2024, 12, 31))]


def test_period_with_many_windows():

    windows = split_period(date(2000, 1, 1), date(2026, 9, 15))

    assert windows == [
        (date(2000, 1, 1), date(2009, 12, 31)),
        (date(2010, 1, 1), date(2019, 12, 31)),
        (date(2020, 1, 1), date(2026, 9, 15)),
    ]


def test_start_on_february_29():

    windows = split_period(date(2016, 2, 29), date(2030, 12, 31))

    assert windows == [
        (date(2016, 2, 29), date(2026, 2, 27)),
        (date(2026, 2, 28), date(2030, 12, 31)),
    ]
