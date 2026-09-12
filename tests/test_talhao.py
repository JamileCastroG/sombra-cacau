from sombra_cacau.talhao import gerar_grade_arvores, simular_talhao


def test_grade_arvores_gera_numero_esperado():
    """
    Um talhão de 20x20m com espaçamento 4x4m deve gerar 5 linhas e
    5 colunas de árvores (20/4 = 5), totalizando 25 árvores.
    """
    posicoes = gerar_grade_arvores(20, 20, 4, 4)
    assert len(posicoes) == 25


def test_simular_talhao_percentual_dentro_do_intervalo_valido():
    """
    O percentual de sombreamento nunca deve ser negativo nem
    ultrapassar 100%, mesmo em talhões muito adensados.
    """
    resultado = simular_talhao(
        largura_talhao=20, comprimento_talhao=20,
        espacamento_linhas=2, espacamento_plantas=2,
        altura=4.0, raio_copa=2.5,
        elevacao_solar=45, azimute_solar=100
    )
    assert 0 <= resultado["percentual"] <= 100


def test_simular_talhao_area_sombreada_nao_ultrapassa_area_do_talhao():
    """
    Mesmo com sobreposição de sombras entre árvores, a área sombreada
    total (após a união geométrica) não pode ser maior que a área
    do próprio talhão.
    """
    resultado = simular_talhao(
        largura_talhao=15, comprimento_talhao=15,
        espacamento_linhas=3, espacamento_plantas=3,
        altura=5.0, raio_copa=3.0,
        elevacao_solar=20, azimute_solar=100
    )
    assert resultado["area_sombreada"] <= resultado["area_talhao"] * 1.01  # margem por aproximação numérica


def test_simular_talhao_sem_sombra_a_noite():
    """
    Com o sol abaixo do horizonte, não deve haver área sombreada.
    """
    resultado = simular_talhao(
        largura_talhao=10, comprimento_talhao=10,
        espacamento_linhas=3, espacamento_plantas=3,
        altura=4.0, raio_copa=2.5,
        elevacao_solar=-5, azimute_solar=100
    )
    assert resultado["area_sombreada"] == 0
    assert resultado["percentual"] == 0