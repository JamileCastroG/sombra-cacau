import pandas as pd
from pvlib import solarposition

def calcular_posicao_solar(latitude, longitude, data_hora):
    """
    Calcula a posição do sol (azimute e elevação) para um local e horário.

    latitude, longitude: em graus decimais (ex.: -1.45, -48.48 para Belém)
    data_hora: string no formato 'YYYY-MM-DD HH:MM', horário local
    """
    timestamp = pd.Timestamp(data_hora, tz='America/Belem')
    posicao = solarposition.get_solarposition(timestamp, latitude, longitude)

    elevacao = posicao['elevation'].iloc[0]
    azimute = posicao['azimuth'].iloc[0]

    return elevacao, azimute


if __name__ == "__main__":
    # Teste: Tomé-Açu, meio-dia de um dia qualquer
    lat, lon = -2.42, -48.15
    elevacao, azimute = calcular_posicao_solar(lat, lon, "2026-09-09 12:00")
    print(f"Elevação solar: {elevacao:.2f}°")
    print(f"Azimute solar: {azimute:.2f}°")