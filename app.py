import streamlit as st
from solar import calcular_posicao_solar
from sombra import calcular_sombra
from copa_sombra import projetar_sombra_copa
from idade_altura import altura_por_idade
from mapa_sombra import criar_mapa_sombra
from streamlit_folium import st_folium
from datetime import date

st.set_page_config(page_title="Sombra do Cacaueiro", page_icon="🌳")
st.title("🌳 Projeção de Sombra — Cacaueiro")
st.write("Calcule a área de sombra projetada por uma árvore de cacau em qualquer data e local.")

st.header("1. Localização")
col1, col2 = st.columns(2)
latitude = col1.number_input("Latitude", value=-2.42, format="%.4f")
longitude = col2.number_input("Longitude", value=-48.15, format="%.4f")

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

    st.subheader("Visualização no mapa")
    mapa = criar_mapa_sombra(dados["latitude"], dados["longitude"], resultado, dados["raio_copa"])
    st_folium(mapa, width=700, height=500)