from sombra_cacau.solar import calcular_posicao_solar

def test_elevacao_meio_dia_proxima_zenite():
    """
    Perto do Equador, ao meio-dia (próximo aos equinócios), a elevação
    solar deve ser alta (próxima de 90°).
    """
    lat, lon = -2.42, -48.15
    elevacao, azimute = calcular_posicao_solar(lat, lon, "2026-09-09 12:00")

    assert elevacao > 70  # esperado: sol bem alto nesse horário/local
    assert 0 <= azimute <= 360  # azimute deve estar em um intervalo válido


def test_elevacao_noite_e_negativa():
    """
    De madrugada, o sol deve estar abaixo do horizonte (elevação negativa).
    """
    lat, lon = -2.42, -48.15
    elevacao, azimute = calcular_posicao_solar(lat, lon, "2026-09-09 03:00")

    assert elevacao < 0