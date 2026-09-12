import math
import pydeck as pdk


def _deslocamento_metros_para_latlon(delta_x_m, delta_y_m, latitude_ref):
    delta_lat = delta_y_m / 111320
    delta_lon = delta_x_m / (111320 * math.cos(math.radians(latitude_ref)))
    return delta_lat, delta_lon


def _gerar_elipse(lat_centro, lon_centro, semi_maior_m, semi_menor_m, direcao_graus, pontos=40):
    """Gera os vértices de uma elipse (lat/lon) orientada na direção informada."""
    coords = []
    direcao_rad = math.radians(direcao_graus)
    for i in range(pontos + 1):
        t = 2 * math.pi * i / pontos
        x_local = semi_maior_m * math.cos(t)
        y_local = semi_menor_m * math.sin(t)

        x_metros = x_local * math.sin(direcao_rad) + y_local * math.cos(direcao_rad)
        y_metros = x_local * math.cos(direcao_rad) - y_local * math.sin(direcao_rad)

        delta_lat, delta_lon = _deslocamento_metros_para_latlon(x_metros, y_metros, lat_centro)
        coords.append([lon_centro + delta_lon, lat_centro + delta_lat])
    return coords


def criar_visualizacao(latitude, longitude, raio_copa, comprimento_sombra, direcao_sombra):
    """
    Cria uma visualização 3D profissional (pydeck) com a copa da árvore
    e a sombra projetada como uma elipse real (mais longa quando o sol
    está baixo, quase circular quando o sol está a pino).
    """
    copa_coords = _gerar_elipse(latitude, longitude, raio_copa, raio_copa, 0)

    centro_x = math.sin(math.radians(direcao_sombra)) * (comprimento_sombra / 2)
    centro_y = math.cos(math.radians(direcao_sombra)) * (comprimento_sombra / 2)
    delta_lat, delta_lon = _deslocamento_metros_para_latlon(centro_x, centro_y, latitude)
    lat_sombra = latitude + delta_lat
    lon_sombra = longitude + delta_lon

    semi_maior = (comprimento_sombra / 2) + raio_copa
    semi_menor = raio_copa
    sombra_coords = _gerar_elipse(lat_sombra, lon_sombra, semi_maior, semi_menor, direcao_sombra)

    camada_sombra = pdk.Layer(
        "PolygonLayer",
        data=[{"polygon": sombra_coords}],
        get_polygon="polygon",
        get_fill_color=[255, 152, 0, 110],   # âmbar translúcido — visível em fundo claro ou escuro
        get_line_color=[230, 100, 0, 220],
        line_width_min_pixels=2,
    )

    camada_copa = pdk.Layer(
        "PolygonLayer",
        data=[{"polygon": copa_coords}],
        get_polygon="polygon",
        get_fill_color=[46, 148, 74, 230],
        get_line_color=[20, 90, 40, 255],
        line_width_min_pixels=2,
    )

    view_state = pdk.ViewState(latitude=latitude, longitude=longitude, zoom=19, pitch=45)

    mapa = pdk.Deck(
        layers=[camada_sombra, camada_copa],
        initial_view_state=view_state,
        map_provider="carto",
        map_style="dark",
    )

    return mapa