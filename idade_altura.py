import math

def altura_por_idade(idade_anos):
    """
    Estima a altura do cacaueiro a partir da idade, usando uma curva
    de crescimento logística (aproximação genérica).

    ATENÇÃO: os parâmetros abaixo são valores de referência aproximados.
    Ajuste-os com base em literatura agronômica específica ou dados de
    campo antes de usar os resultados de forma definitiva.

    idade_anos: idade da árvore em anos
    """
    altura_maxima = 5.0   # m — altura média de cacaueiro adulto manejado
    taxa_crescimento = 0.8
    ponto_inflexao = 2.5   # anos — fase de crescimento mais rápido

    altura = altura_maxima / (1 + math.exp(-taxa_crescimento * (idade_anos - ponto_inflexao)))
    return altura


if __name__ == "__main__":
    for idade in [1, 2, 3, 4, 5, 8]:
        h = altura_por_idade(idade)
        print(f"Idade: {idade} anos -> Altura estimada: {h:.2f} m")