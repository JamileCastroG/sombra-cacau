from sombra_cacau.sazonal import variacao_sazonal


def test_variacao_sazonal_retorna_doze_meses():
    resultados = variacao_sazonal(latitude=-2.42, longitude=-48.15, altura=4.0, ano=2026)
    assert len(resultados) == 12


def test_variacao_sazonal_meses_em_ordem():
    resultados = variacao_sazonal(latitude=-2.42, longitude=-48.15, altura=4.0, ano=2026)
    meses_esperados = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    meses_obtidos = [r["mes"] for r in resultados]
    assert meses_obtidos == meses_esperados