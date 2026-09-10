from sombra_cacau.sombra import calcular_sombra

def test_sombra_maior_com_sol_baixo():
    """
    Com o sol mais baixo no céu, a sombra deve ser mais longa
    do que com o sol mais alto, para a mesma altura de árvore.
    """
    altura = 4.0

    comprimento_sol_alto, _ = calcular_sombra(altura, elevacao_solar=80, azimute_solar=100)
    comprimento_sol_baixo, _ = calcular_sombra(altura, elevacao_solar=20, azimute_solar=100)

    assert comprimento_sol_baixo > comprimento_sol_alto


def test_sem_sombra_com_sol_abaixo_do_horizonte():
    """
    Se o sol está abaixo do horizonte (elevação <= 0), não deve haver sombra.
    """
    comprimento, direcao = calcular_sombra(altura_arvore=4.0, elevacao_solar=-5, azimute_solar=100)

    assert comprimento is None
    assert direcao is None