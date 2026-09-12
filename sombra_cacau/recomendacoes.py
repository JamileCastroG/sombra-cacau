SOMBREAMENTO_MINIMO_IDEAL = 25
SOMBREAMENTO_MAXIMO_IDEAL = 50


def classificar_sombreamento(percentual):
    """
    Classifica o percentual de cobertura de dossel de um talhão de cacau
    em relação à faixa geralmente considerada adequada para a cultura
    (aproximadamente 25% a 50%, variando com variedade, idade da planta
    e manejo). Retorna (status, mensagem).

    IMPORTANTE: `percentual` deve ser a cobertura de dossel estática
    (ver calcular_cobertura_dossel em talhao.py), não a sombra projetada
    em um horário específico — esta última varia fortemente ao longo do
    dia (curta ao meio-dia solar, alongada perto do nascer/pôr do sol) e
    não é comparável diretamente à faixa de referência da literatura.

    ATENÇÃO: valores de referência gerais — vale confirmar/ajustar com
    literatura agronômica específica para a variedade e sistema de
    cultivo usados no seu trabalho.
    """
    if percentual < SOMBREAMENTO_MINIMO_IDEAL:
        return "abaixo", (
            f"Sombreamento de {percentual:.1f}% está abaixo da faixa geralmente "
            f"recomendada ({SOMBREAMENTO_MINIMO_IDEAL}-{SOMBREAMENTO_MAXIMO_IDEAL}%). "
            "Pode indicar risco de estresse térmico/hídrico nas plantas."
        )
    elif percentual <= SOMBREAMENTO_MAXIMO_IDEAL:
        return "ideal", (
            f"Sombreamento de {percentual:.1f}% está dentro da faixa geralmente "
            f"recomendada ({SOMBREAMENTO_MINIMO_IDEAL}-{SOMBREAMENTO_MAXIMO_IDEAL}%) para cacauicultura."
        )
    else:
        return "acima", (
            f"Sombreamento de {percentual:.1f}% está acima da faixa geralmente "
            f"recomendada ({SOMBREAMENTO_MINIMO_IDEAL}-{SOMBREAMENTO_MAXIMO_IDEAL}%). "
            "Pode reduzir fotossíntese e produtividade — considere raleamento do sombreamento."
        )


def recomendar_especies_saf(idade_anos):
    """
    Sugere espécies de sombreamento associadas ao cacaueiro em sistema
    agroflorestal (SAF), de acordo com o estágio de desenvolvimento da
    lavoura. Baseado em práticas gerais de SAFs com cacau na Amazônia —
    recomenda-se validar/ajustar com literatura específica e com as
    condições reais do talhão (solo, variedade, arranjo já existente).
    """
    if idade_anos <= 2:
        return {
            "estagio": "Implantação (0-2 anos)",
            "especies": ["Banana / bananeira-da-terra (sombra provisória, rápida)"],
            "observacao": (
                "Nessa fase o cacaueiro ainda é pequeno e precisa de sombra rápida; "
                "a banana cumpre esse papel enquanto a sombra permanente se estabelece."
            )
        }
    elif idade_anos <= 5:
        return {
            "estagio": "Crescimento (2-5 anos)",
            "especies": [
                "Banana (mantida, sombra ainda parcial)",
                "Ingá (leguminosa, fixação de nitrogênio, sombra permanente em formação)",
                "Pupunha (sombra permanente, também produtiva)"
            ],
            "observacao": (
                "Fase de transição: a sombra permanente começa a assumir o papel da "
                "sombra provisória, que pode começar a ser reduzida gradualmente."
            )
        }
    else:
        return {
            "estagio": "Adulto (5+ anos)",
            "especies": [
                "Ingá (sombra permanente já estabelecida)",
                "Castanheira-do-pará (sombra alta, valor econômico adicional)",
                "Açaí (estrato médio, produtivo)"
            ],
            "observacao": (
                "A banana normalmente já pode ser retirada nessa fase — a sombra "
                "permanente das espécies maiores deve estar estabelecida."
            )
        }