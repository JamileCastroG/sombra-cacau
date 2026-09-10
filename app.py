import streamlit as st
from sombra_cacau.solar import calcular_posicao_solar
from sombra_cacau.sombra import calcular_sombra
from sombra_cacau.copa_sombra import projetar_sombra_copa
from sombra_cacau.idade_altura import altura_por_idade
from sombra_cacau.visualizacao import criar_visualizacao
from datetime import date
from streamlit_geolocation import streamlit_geolocation
from sombra_cacau.geolocalizacao import obter_localizacao_por_ip

st.set_page_config(page_title="Sombra do Cacaueiro")
st.title("Projeção de Sombra — Cacaueiro")
st.write("Calcule a área de sombra projetada por uma árvore de cacau em qualquer data e local.")

st.header("1. Localização")

col_gps, col_ip = st.columns(2)

with col_gps:
    st.caption("Opção A: usar GPS do dispositivo")
    localizacao_gps = streamlit_geolocation()

with col_ip:
    st.caption("Opção B: estimar pela conexão de internet")
    usar_ip = st.button("📡 Estimar por IP")

# Define valores padrão (Tomé-Açu) caso nada tenha sido detectado ainda
if "latitude_atual" not in st.session_state:
    st.session_state["latitude_atual"] = -2.42
    st.session_state["longitude_atual"] = -48.15

if localizacao_gps and localizacao_gps.get("latitude"):
    st.session_state["latitude_atual"] = localizacao_gps["latitude"]
    st.session_state["longitude_atual"] = localizacao_gps["longitude"]
    st.success("Localização obtida via GPS do dispositivo.")

if usar_ip:
    lat_ip, lon_ip = obter_localizacao_por_ip()
    if lat_ip is not None:
        st.session_state["latitude_atual"] = lat_ip
        st.session_state["longitude_atual"] = lon_ip
        st.info("Localização estimada pelo IP (aproximada).")
    else:
        st.warning("Não foi possível estimar a localização pelo IP.")

col1, col2 = st.columns(2)
latitude = col1.number_input("Latitude", value=st.session_state["latitude_atual"], format="%.4f")
longitude = col2.number_input("Longitude", value=st.session_state["longitude_atual"], format="%.4f")

st.header("2. Data e horário")
data_selecionada = st.date_input("Data", value=date.today())
hora_selecionada = st.slider("Hora do dia", 0, 23, 12)

st.header("3. Árvore")
modo = st.radio("Como deseja informar o porte da árvore?", ["Idade (anos)", "Altura direta (m)"])

if modo == "Idade (anos)":
    idade = st.number_input("Idade da árvore (anos)", min_value=0.5, max_value=30.0, value=4.0)
    altura = altura_por_idade(idade)
    st.caption(f"Altura estimada: {altura:.2f} m")
else:
    altura = st.number_input("Altura da árvore (m)", min_value=0.5, max_value=15.0, value=4.0)

raio_copa = st.number_input("Raio da copa (m)", min_value=0.5, max_value=6.0, value=2.5)

if st.button("Calcular sombra"):
    data_hora = f"{data_selecionada} {hora_selecionada:02d}:00"
    elevacao, azimute = calcular_posicao_solar(latitude, longitude, data_hora)

    if elevacao <= 0:
        st.session_state["resultado_calculo"] = None
        st.warning("O sol está abaixo do horizonte nesse horário — não há sombra.")
    else:
        comprimento, direcao = calcular_sombra(altura, elevacao, azimute)
        resultado = projetar_sombra_copa(raio_copa, comprimento, direcao)
        st.session_state["resultado_calculo"] = {
            "elevacao": elevacao,
            "comprimento": comprimento,
            "direcao": direcao,
            "resultado": resultado,
            "latitude": latitude,
            "longitude": longitude,
            "raio_copa": raio_copa
        }

if st.session_state.get("resultado_calculo"):
    dados = st.session_state["resultado_calculo"]
    resultado = dados["resultado"]

    st.success("Cálculo concluído!")
    col1, col2, col3 = st.columns(3)
    col1.metric("Elevação solar", f"{dados['elevacao']:.1f}°")
    col2.metric("Comprimento da sombra", f"{dados['comprimento']:.2f} m")
    col3.metric("Área de sombra", f"{resultado['area_m2']:.2f} m²")

    st.subheader("Visualização")
    mapa = criar_visualizacao(
        dados["latitude"], dados["longitude"], dados["raio_copa"],
        dados["comprimento"], resultado.get("direcao_sombra", 0)
    )
    st.pydeck_chart(mapa)