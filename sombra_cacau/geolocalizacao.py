import requests

def obter_localizacao_por_ip():
    """
    Estima a localização (latitude, longitude) a partir do IP da conexão.
    Baixa precisão (nível de cidade) — usar como fallback quando o GPS
    do navegador não estiver disponível ou for negado pelo usuário.

    Retorna (latitude, longitude) ou (None, None) em caso de falha.
    """
    try:
        resposta = requests.get("https://ipapi.co/json/", timeout=5)
        dados = resposta.json()
        latitude = dados.get("latitude")
        longitude = dados.get("longitude")
        return latitude, longitude
    except Exception:
        return None, None