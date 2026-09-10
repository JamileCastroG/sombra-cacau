import folium
import math

def metros_para_graus(delta_x_m, delta_y_m, latitude_ref):
    """
    Converte um deslocamento em metros (Leste-Oeste, Norte-Sul) para
    graus de latitude/longitude, usando aproximação local.
    """
    delta_lat = delta_y_m / 111320  # 1 grau de latitude ≈ 111.32 km
    delta_lon = delta_x_m / (111320 * math.cos(math.radians(latitude_ref)))
    return delta_lat, delta_lon


def criar_mapa_sombra(latitude, longitude, resultado_sombra, raio_copa):
    """
    Cria um mapa com a árvore (posição original) e a sombra projetada.
    """
    mapa = folium.Map(location=[latitude, longitude], zoom_start=19, tiles="OpenStreetMap")

    # Marca a base da árvore
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=6,
        color="green",
        fill=True,
        fill_color="green",
        popup="Base da árvore"
    ).add_to(mapa)

    # Círculo representando a copa (vista de cima)
    folium.Circle(
        location=[latitude, longitude],
        radius=raio_copa,
        color="darkgreen",
        fill=True,
        fill_opacity=0.3,
        popup="Copa da árvore"
    ).add_to(mapa)

    # Calcula a posição do centro da sombra em lat/lon
    delta_lat, delta_lon = metros_para_graus(
        resultado_sombra["centro_x"], resultado_sombra["centro_y"], latitude
    )
    lat_sombra = latitude + delta_lat
    lon_sombra = longitude + delta_lon

    # Círculo representando a sombra projetada no solo
    folium.Circle(
        location=[lat_sombra, lon_sombra],
        radius=resultado_sombra["raio_projetado"],
        color="black",
        fill=True,
        fill_color="gray",
        fill_opacity=0.4,
        popup=f"Sombra projetada ({resultado_sombra['area_m2']:.2f} m²)"
    ).add_to(mapa)

    return mapa