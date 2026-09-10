import pandas as pd
from pvlib import solarposition
from timezonefinder import TimezoneFinder

_localizador_fuso = TimezoneFinder()

def calcular_posicao_solar(latitude, longitude, data_hora):
    """
    Calcula a posição do sol (azimute e elevação) para um local e horário.

    latitude, longitude: em graus decimais
    data_hora: string no formato 'YYYY-MM-DD HH:MM', horário local do ponto informado
    """
    fuso = _localizador_fuso.timezone_at(lat=latitude, lng=longitude)
    if fuso is None:
        fuso = "UTC"  # fallback raro (ex.: coordenada em pleno oceano)

    timestamp = pd.Timestamp(data_hora, tz=fuso)
    posicao = solarposition.get_solarposition(timestamp, latitude, longitude)

    elevacao = posicao['elevation'].iloc[0]
    azimute = posicao['azimuth'].iloc[0]

    return elevacao, azimute


if __name__ == "__main__":
    lat, lon = -2.42, -48.15
    elevacao, azimute = calcular_posicao_solar(lat, lon, "2026-09-09 12:00")
    print(f"Elevação solar: {elevacao:.2f}°")
    print(f"Azimute solar: {azimute:.2f}°")