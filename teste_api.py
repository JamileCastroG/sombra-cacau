import requests

url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
parametros = {
    "parameters": "ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN",
    "community": "AG",
    "longitude": -48.15,
    "latitude": -2.42,
    "format": "JSON"
}

resposta = requests.get(url, params=parametros, timeout=15)
print(resposta.status_code)
print(resposta.text[:1000])
