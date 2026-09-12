import math
from shapely.geometry import Point, box
from shapely.ops import unary_union
from shapely.affinity import scale as escalar, rotate as rotacionar, translate as transladar

from sombra_cacau.sombra import calcular_sombra


def gerar_grade_arvores(largura_talhao, comprimento_talhao, espacamento_linhas, espacamento_plantas):
    """
    Gera as posições (x, y), em metros, das árvores em uma grade retangular
    regular. x = Leste-Oeste, y = Norte-Sul. Origem no canto do talhão.
    """
    posicoes = []
    x = espacamento_plantas / 2
    while x < largura_talhao:
        y = espacamento_linhas / 2
        while y < comprimento_talhao:
            posicoes.append((x, y))
            y += espacamento_linhas
        x += espacamento_plantas
    return posicoes


def _elipse_sombra(centro_x, centro_y, raio_copa, comprimento_sombra, direcao_sombra):
    """
    Retorna um polígono (shapely) representando a área de copa + sombra
    projetada de uma árvore, já posicionado no talhão.
    """
    semi_maior = (comprimento_sombra / 2) + raio_copa
    semi_menor = raio_copa

    circulo = Point(0, 0).buffer(1, quad_segs=8)
    elipse = escalar(circulo, xfact=semi_menor, yfact=semi_maior)
    elipse = rotacionar(elipse, -direcao_sombra, origin=(0, 0))

    deslocamento_x = math.sin(math.radians(direcao_sombra)) * (comprimento_sombra / 2)
    deslocamento_y = math.cos(math.radians(direcao_sombra)) * (comprimento_sombra / 2)
    elipse = transladar(elipse, centro_x + deslocamento_x, centro_y + deslocamento_y)

    return elipse


def simular_talhao(largura_talhao, comprimento_talhao, espacamento_linhas, espacamento_plantas,
                    altura, raio_copa, elevacao_solar, azimute_solar):
    """
    Simula um talhão retangular com árvores em grade regular, calculando
    a sombra de cada árvore para a posição solar informada e a área total
    sombreada no talhão — contando sobreposições apenas uma vez (união
    geométrica dos polígonos de sombra via shapely).

    NOTA: o percentual retornado aqui é a sombra instantânea projetada
    para a hora/data selecionadas — varia fortemente ao longo do dia
    (curta perto do meio-dia solar, alongada perto do nascer/pôr do sol)
    e NÃO deve ser usado como métrica de classificação agronômica de
    sombreamento. Para isso, use calcular_cobertura_dossel().
    """
    posicoes = gerar_grade_arvores(largura_talhao, comprimento_talhao, espacamento_linhas, espacamento_plantas)
    area_talhao = largura_talhao * comprimento_talhao

    if elevacao_solar <= 0:
        return {
            "arvores": posicoes, "poligonos": [], "area_sombreada": 0,
            "area_talhao": area_talhao, "percentual": 0, "num_arvores": len(posicoes)
        }

    comprimento_sombra, direcao_sombra = calcular_sombra(altura, elevacao_solar, azimute_solar)

    poligonos = [
        _elipse_sombra(x, y, raio_copa, comprimento_sombra, direcao_sombra)
        for x, y in posicoes
    ]

    uniao = unary_union(poligonos)
    limite_talhao = box(0, 0, largura_talhao, comprimento_talhao)
    area_sombreada = uniao.intersection(limite_talhao).area
    percentual = min(100, (area_sombreada / area_talhao) * 100) if area_talhao > 0 else 0

    return {
        "arvores": posicoes,
        "poligonos": poligonos,
        "area_sombreada": area_sombreada,
        "area_talhao": area_talhao,
        "percentual": percentual,
        "num_arvores": len(posicoes)
    }


def calcular_cobertura_dossel(largura_talhao, comprimento_talhao, espacamento_linhas,
                                espacamento_plantas, raio_copa):
    """
    Calcula a cobertura de dossel (crown cover) do talhão: fração da área
    coberta pela projeção vertical das copas das árvores, vista de cima,
    independente de hora do dia ou posição solar. Sobreposições entre
    copas vizinhas são contadas uma única vez (união geométrica via
    shapely).

    É esta métrica — e não a sombra projetada em um horário específico,
    que varia fortemente ao longo do dia — que deve ser comparada à faixa
    de sombreamento ideal da literatura agronômica (ex.: ~25-50% para
    cacau em SAF), já que essas referências tratam de cobertura de copa/
    interceptação de luz, não de sombra instantânea.
    """
    posicoes = gerar_grade_arvores(largura_talhao, comprimento_talhao,
                                    espacamento_linhas, espacamento_plantas)
    area_talhao = largura_talhao * comprimento_talhao

    copas = [Point(x, y).buffer(raio_copa, resolution=32) for x, y in posicoes]
    uniao = unary_union(copas)
    area_copas = uniao.area
    percentual = min(100, (area_copas / area_talhao) * 100) if area_talhao > 0 else 0

    return {
        "area_copas": area_copas,
        "area_talhao": area_talhao,
        "percentual": percentual,
        "num_arvores": len(posicoes)
    }