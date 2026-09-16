from datetime import date

import requests

URL_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
HEADERS = {"User-Agent": "barometro/0.1 (github.com/RodriguesGS/barometro)"}


class InvalidPeriod(Exception):
    
class TemporaryError(Exception):
    
class PermanentError(Exception):

def search_last(code: int, quantity: int) -> list[dict[str, str]]:

    url = f"{URL_BASE.format(code=code)}/ultimos/{quantity}"
    response = requests.get(url, params={"formato": "json"}, headers=HEADERS, timeout=30)

    return response.json()


def format_date(data: date) -> str:
    return data.strftime("%d/%m/%Y")

def validate_period(start: date, end: date) -> None:

    if start > end:
        raise InvalidPeriod()


if __name__ == "__main__":
    for i in search_last(code=1, quantity=5):
        print(f"{i['data']}  {i['valor']}")

    print(format_date(date(2026, 1, 31)))
