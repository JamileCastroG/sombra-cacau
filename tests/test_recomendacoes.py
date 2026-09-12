from sombra_cacau.recomendacoes import classificar_sombreamento, recomendar_especies_saf


def test_classificar_sombreamento_abaixo_do_ideal():
    status, mensagem = classificar_sombreamento(15)
    assert status == "abaixo"


def test_classificar_sombreamento_dentro_do_ideal():
    status, mensagem = classificar_sombreamento(35)
    assert status == "ideal"


def test_classificar_sombreamento_acima_do_ideal():
    status, mensagem = classificar_sombreamento(70)
    assert status == "acima"


def test_classificar_sombreamento_limites_da_faixa():
    """Os valores exatamente nos limites (25% e 50%) devem contar como 'ideal'."""
    status_min, _ = classificar_sombreamento(25)
    status_max, _ = classificar_sombreamento(50)
    assert status_min == "ideal"
    assert status_max == "ideal"


def test_recomendar_especies_implantacao():
    recomendacao = recomendar_especies_saf(1)
    assert "Implantação" in recomendacao["estagio"]


def test_recomendar_especies_crescimento():
    recomendacao = recomendar_especies_saf(3)
    assert "Crescimento" in recomendacao["estagio"]


def test_recomendar_especies_adulto():
    recomendacao = recomendar_especies_saf(8)
    assert "Adulto" in recomendacao["estagio"]