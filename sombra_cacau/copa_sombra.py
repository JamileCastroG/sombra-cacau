import math
from sombra_cacau.solar import calcular_posicao_solar
from sombra_cacau.sombra import calcular_sombra

def projetar_sombra_copa(raio_copa, comprimento_sombra, direcao_sombra):
    """
    Retorna o centro da elipse de sombra projetada no solo, em coordenadas
    relativas à base da árvore (x=Leste/Oeste, y=Norte/Sul, em metros).

    raio_copa: raio da copa da árvore, em metros
    comprimento_sombra: distância que o centro da copa se desloca no solo
    direcao_sombra: direção da sombra, em graus a partir do Norte
    """
    direcao_rad = math.radians(direcao_sombra)

    # Deslocamento do centro da copa projetada
    delta_x = comprimento_sombra * math.sin(direcao_rad)  # Leste-Oeste
    delta_y = comprimento_sombra * math.cos(direcao_rad)  # Norte-Sul

    area_sombra = math.pi * (raio_copa ** 2)  # aproximação: área ~ igual à da copa

    return {
        "centro_x": delta_x,
        "centro_y": delta_y,
        "raio_projetado": raio_copa,
        "area_m2": area_sombra
    }


if __name__ == "__main__":
    lat, lon = -2.42, -48.15
    altura = 4.0
    raio_copa = 2.5  # metros, copa de um cacaueiro adulto

    elevacao, azimute = calcular_posicao_solar(lat, lon, "2026-09-09 12:00")
    comprimento, direcao = calcular_sombra(altura, elevacao, azimute)

    resultado = projetar_sombra_copa(raio_copa, comprimento, direcao)

    print(f"Centro da sombra: ({resultado['centro_x']:.2f}, {resultado['centro_y']:.2f}) m da base da árvore")
    print(f"Área de sombra projetada: {resultado['area_m2']:.2f} m²")