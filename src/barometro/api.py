import json
import urllib.request

URL_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
USER_AGENT = "barometro/0.1 (github.com/RodriguesGS/barometro)"
TIMEOUT = 30
MAX_SEC = 20


def search_last(code: int, quantity: int) -> list[dict[str, str]]:
    if not 1 <= quantity <= MAX_SEC:
        raise ValueError(
            f"Quantidade deve estar entre 1 e {MAX_SEC}, recebido: {quantity}"
        )

    url = URL_BASE.format(code=code) + f"/ultimos/{quantity}?formato=json"
    requisicao = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    with urllib.request.urlopen(requisicao, timeout=TIMEOUT) as resposta:
        return json.load(resposta)


if __name__ == "__main__":
    for registro in search_last(code=1, quantity=5):
        print(f"{registro['data']}  {registro['valor']}")
        