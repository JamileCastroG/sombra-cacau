from sombra_cacau.solar import calcular_posicao_solar
from sombra_cacau.sombra import calcular_sombra

NOMES_MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def variacao_sazonal(latitude, longitude, altura, ano, hora=12):
    """
    Calcula a posição solar e o comprimento da sombra no dia 15 de cada
    mês do ano informado, no mesmo horário fixo — para visualizar a
    variação sazonal da trajetória solar e da sombra ao longo do ano.
    """
    resultados = []
    for mes in range(1, 13):
        data_hora = f"{ano}-{mes:02d}-15 {hora:02d}:00"
        elevacao, azimute = calcular_posicao_solar(latitude, longitude, data_hora)

        if elevacao > 0:
            comprimento, direcao = calcular_sombra(altura, elevacao, azimute)
        else:
            comprimento, direcao = None, None

        resultados.append({
            "mes": NOMES_MESES[mes - 1],
            "elevacao": elevacao,
            "comprimento_sombra": comprimento
        })

    return resultados