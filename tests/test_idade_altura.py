from sombra_cacau.idade_altura import altura_por_idade


def test_altura_cresce_com_a_idade():
    """A altura estimada deve aumentar (ou no mínimo não diminuir) conforme a idade avança."""
    altura_jovem = altura_por_idade(1)
    altura_adulta = altura_por_idade(8)
    assert altura_adulta > altura_jovem


def test_altura_nunca_ultrapassa_o_maximo_da_curva():
    """A curva logística nunca deve ultrapassar a altura máxima definida (5.0 m)."""
    altura_muito_velha = altura_por_idade(50)
    assert altura_muito_velha <= 5.0