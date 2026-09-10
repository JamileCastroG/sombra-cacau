import math
from sombra_cacau.solar import calcular_posicao_solar

def calcular_sombra(altura_arvore, elevacao_solar, azimute_solar):
    """
    Calcula o comprimento da sombra projetada e a direção para onde ela aponta.

    altura_arvore: altura da árvore em metros
    elevacao_solar: ângulo de elevação do sol em graus
    azimute_solar: direção do sol em graus (0=Norte, 90=Leste, 180=Sul, 270=Oeste)
    """
    elevacao_rad = math.radians(elevacao_solar)

    # Se o sol estiver abaixo do horizonte, não há sombra útil
    if elevacao_solar <= 0:
        return None, None

    comprimento_sombra = altura_arvore / math.tan(elevacao_rad)

    # A sombra aponta na direção oposta ao sol
    direcao_sombra = (azimute_solar + 180) % 360

    return comprimento_sombra, direcao_sombra


if __name__ == "__main__":
    lat, lon = -2.42, -48.15
    altura = 4.0  # metros, altura média de um cacaueiro adulto

    elevacao, azimute = calcular_posicao_solar(lat, lon, "2026-09-09 12:00")
    comprimento, direcao = calcular_sombra(altura, elevacao, azimute)

    if comprimento is not None:
        print(f"Comprimento da sombra: {comprimento:.2f} m")
        print(f"Direção da sombra: {direcao:.2f}° (a partir do Norte)")
    else:
        print("Sol abaixo do horizonte — sem sombra.")