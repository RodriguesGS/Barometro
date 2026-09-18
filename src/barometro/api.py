from datetime import date

import requests

from barometro.periods import add_years

URL_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
HEADERS = {"User-Agent": "barometro/0.1 (github.com/RodriguesGS/barometro)"}


def search_last(code: int, quantity: int) -> list[dict[str, str]]:

    url = f"{URL_BASE.format(code=code)}/ultimos/{quantity}"
    response = requests.get(
        url, params={"formato": "json"}, headers=HEADERS, timeout=30
    )

    response.raise_for_status()

    return response.json()


def format_date(data: date) -> str:
    return data.strftime("%d/%m/%Y")


def validate_period(start: date, end: date) -> None:

    if start > end:
        raise ValueError(
            f"Data inicial {format_date(start)} eh depois da data final {format_date(end)}"
        )

    if end >= add_years(start, 10):
        raise ValueError(
            f"O periodo ultrapassa do limite de 10 anos {format_date(start)} - {format_date(end)}"
        )


def search_period(code: int, start: date, end: date) -> list[dict[str, str]]:
    """
    Busca os valores da série entre duas datas, como vieram da API.

    A API responde 404 quando o período não tem dados. Nesse caso,
    retorna uma lista vazia.
    """

    validate_period(start=start, end=end)

    url = f"{URL_BASE.format(code=code)}"
    params = {
        "formato": "json",
        "dataInicial": format_date(start),
        "dataFinal": format_date(end),
    }

    response = requests.get(url, params=params, headers=HEADERS, timeout=30)

    if response.status_code == 404:
        return []

    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    records = search_period(code=1, start=date(2026, 1, 1), end=date(2026, 1, 31))
    print(f"Teste 1 | dólar em janeiro | {len(records)} registros")

    try:
        search_last(code=999999999, quantity=5)
        print("Teste 2 | não deu erro")
    except requests.HTTPError as err:
        print(f"Teste 2 | HTTPError, status {err.response.status_code}")
    except requests.Timeout:
        print("Teste 2 | Timeout: a API não respondeu em 30 segundos")

    try:
        records = search_period(code=433, start=date(2026, 9, 5), end=date(2026, 9, 10))
        print(f"Teste 3 | IPCA de 05/09 a 10/09 | {len(records)} registros")
    except requests.HTTPError as err:
        print(f"Teste 3 | HTTPError, status {err.response.status_code}")
        print(f"Resposta: {err.response.text[:200]}")
