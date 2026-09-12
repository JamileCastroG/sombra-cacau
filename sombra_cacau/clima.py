import requests

NOMES_MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

CHAVES_MES_API = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                  "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def obter_radiacao_solar_mensal(latitude, longitude):
    """
    Consulta a API pública NASA POWER (climatologia de longo prazo, sem
    necessidade de chave de acesso) e retorna a radiação solar média
    mensal para o ponto informado:

    - allsky: radiação real média histórica (considerando nebulosidade)
    - clrsky: radiação teórica de céu limpo (sem nuvens)

    Ambas em MJ/m²/dia. Retorna None em caso de falha na consulta.
    """
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    parametros = {
        "parameters": "ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "format": "JSON"
    }

    try:
        resposta = requests.get(url, params=parametros, timeout=15)
        resposta.raise_for_status()
        dados = resposta.json()

        allsky_bruto = dados["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
        clrsky_bruto = dados["properties"]["parameter"]["CLRSKY_SFC_SW_DWN"]

        allsky = [allsky_bruto[chave] for chave in CHAVES_MES_API]
        clrsky = [clrsky_bruto[chave] for chave in CHAVES_MES_API]

        indice_ceu_claro = [
            (a / c) if c > 0 else None for a, c in zip(allsky, clrsky)
        ]

        return {
            "meses": NOMES_MESES,
            "allsky": allsky,
            "clrsky": clrsky,
            "indice_ceu_claro": indice_ceu_claro
        }
    except Exception:
        return None