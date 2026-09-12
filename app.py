import streamlit as st
import streamlit.components.v1 as components
from sombra_cacau.solar import calcular_posicao_solar
from sombra_cacau.sombra import calcular_sombra
from sombra_cacau.copa_sombra import projetar_sombra_copa
from sombra_cacau.idade_altura import altura_por_idade
from sombra_cacau.visualizacao import criar_visualizacao
from datetime import date
from streamlit_geolocation import streamlit_geolocation
from sombra_cacau.geolocalizacao import obter_localizacao_por_ip
from sombra_cacau.cena3d import gerar_cena_3d
from sombra_cacau.talhao import simular_talhao, calcular_cobertura_dossel
from sombra_cacau.visualizacao_talhao import criar_grafico_talhao
from sombra_cacau.recomendacoes import classificar_sombreamento, recomendar_especies_saf
from sombra_cacau.clima import obter_radiacao_solar_mensal
from sombra_cacau.visualizacao_clima import criar_grafico_radiacao
from sombra_cacau.sazonal import variacao_sazonal
from sombra_cacau.visualizacao_sazonal import criar_grafico_sazonal
from sombra_cacau.relatorio import gerar_relatorio_pdf
from sombra_cacau.pwa import injetar_pwa


st.set_page_config(page_title="Sombra do Cacaueiro")
injetar_pwa()
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

if modo == "Idade (anos)":
    with st.expander("🌴 Recomendação de espécies de sombreamento (SAF)"):
        recomendacao = recomendar_especies_saf(idade)
        st.write(f"**Estágio:** {recomendacao['estagio']}")
        st.write("**Espécies sugeridas:**")
        for especie in recomendacao["especies"]:
            st.write(f"- {especie}")
        st.caption(recomendacao["observacao"])

st.header("🌾 Modo de análise")
modo_analise = st.radio("Analisar:", ["Árvore única", "Talhão (múltiplas árvores)"])

if modo_analise == "Talhão (múltiplas árvores)":
    col_a, col_b = st.columns(2)
    largura_talhao = col_a.number_input("Largura do talhão (m)", min_value=5.0, value=20.0, step=1.0)
    comprimento_talhao = col_b.number_input("Comprimento do talhão (m)", min_value=5.0, value=20.0, step=1.0)
    col_c, col_d = st.columns(2)
    espacamento_linhas = col_c.number_input("Espaçamento entre linhas (m)", min_value=1.0, value=4.0, step=0.5)
    espacamento_plantas = col_d.number_input("Espaçamento entre plantas (m)", min_value=1.0, value=3.0, step=0.5)

# ---------- Cálculo reativo: roda de novo sempre que qualquer campo acima muda ----------
data_hora = f"{data_selecionada} {hora_selecionada:02d}:00"
elevacao, azimute = calcular_posicao_solar(latitude, longitude, data_hora)

st.divider()

if elevacao <= 0:
    st.warning("O sol está abaixo do horizonte nesse horário — não há sombra.")

elif modo_analise == "Talhão (múltiplas árvores)":
    resultado_t = simular_talhao(
        largura_talhao, comprimento_talhao, espacamento_linhas, espacamento_plantas,
        altura, raio_copa, elevacao, azimute
    )
    cobertura = calcular_cobertura_dossel(
        largura_talhao, comprimento_talhao, espacamento_linhas, espacamento_plantas, raio_copa
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Número de árvores", resultado_t["num_arvores"])
    col2.metric(
        "Sombra projetada agora", f"{resultado_t['percentual']:.1f}%",
        help="Sombra instantânea para a hora selecionada — varia ao longo do dia, não é a métrica de referência agronômica."
    )
    col3.metric(
        "Cobertura de dossel", f"{cobertura['percentual']:.1f}%",
        help="Fração fixa da área coberta pela copa das árvores, independente da hora — é esta que é comparada à faixa ideal."
    )

    status, mensagem = classificar_sombreamento(cobertura["percentual"])
    if status == "ideal":
        st.success(mensagem)
    elif status == "abaixo":
        st.warning(mensagem)
    else:
        st.warning(mensagem)

    st.subheader("Vista de cima do talhão")
    fig = criar_grafico_talhao(resultado_t, largura_talhao, comprimento_talhao, raio_copa)
    st.plotly_chart(fig, use_container_width=True)

    parametros_pdf = [
        ("Latitude", f"{latitude:.4f}"), ("Longitude", f"{longitude:.4f}"),
        ("Data/hora", data_hora), ("Altura da árvore (m)", f"{altura:.2f}"),
        ("Raio da copa (m)", f"{raio_copa:.2f}"),
        ("Dimensões do talhão (m)", f"{largura_talhao} x {comprimento_talhao}"),
        ("Espaçamento linhas x plantas (m)", f"{espacamento_linhas} x {espacamento_plantas}")
    ]
    resultados_pdf = [
        ("Número de árvores", resultado_t["num_arvores"]),
        ("Área sombreada", f"{resultado_t['area_sombreada']:.1f} m²"),
        ("% do talhão sombreado", f"{resultado_t['percentual']:.1f}%")
    ]
    dados_clima_pdf = obter_radiacao_solar_mensal(latitude, longitude)
    dados_sazonais_pdf = variacao_sazonal(latitude, longitude, altura, data_selecionada.year, hora_selecionada)
    pdf_bytes = gerar_relatorio_pdf(
        "Análise de talhão", parametros_pdf, resultados_pdf, observacoes=mensagem,
        dados_clima=dados_clima_pdf, dados_sazonais=dados_sazonais_pdf
    )
    st.download_button("📄 Baixar relatório PDF", data=pdf_bytes, file_name="relatorio_talhao_cacau.pdf", mime="application/pdf")

else:
    comprimento, direcao = calcular_sombra(altura, elevacao, azimute)
    resultado = projetar_sombra_copa(raio_copa, comprimento, direcao)

    st.success("Cálculo concluído!")
    col1, col2, col3 = st.columns(3)
    col1.metric("Elevação solar", f"{elevacao:.1f}°")
    col2.metric("Comprimento da sombra", f"{comprimento:.2f} m")
    col3.metric("Área de sombra", f"{resultado['area_m2']:.2f} m²")

    st.subheader("Visualização")
    aba_3d, aba_mapa = st.tabs(["🌳 Cena 3D", "🗺️ Mapa real"])

    with aba_3d:
        html_cena = gerar_cena_3d(altura, raio_copa, comprimento, direcao, elevacao, azimute)
        components.html(html_cena, height=610, scrolling=False)
        st.caption("Arraste para girar a câmera. Silhueta ao lado: pessoa de 1,70 m, para referência de escala.")

    with aba_mapa:
        mapa = criar_visualizacao(latitude, longitude, raio_copa, comprimento, direcao)
        st.pydeck_chart(mapa)

        parametros_pdf = [
        ("Latitude", f"{latitude:.4f}"), ("Longitude", f"{longitude:.4f}"),
        ("Data/hora", data_hora), ("Altura da árvore (m)", f"{altura:.2f}"),
        ("Raio da copa (m)", f"{raio_copa:.2f}")
    ]
    resultados_pdf = [
        ("Elevação solar", f"{elevacao:.1f}°"),
        ("Comprimento da sombra", f"{comprimento:.2f} m"),
        ("Área de sombra", f"{resultado['area_m2']:.2f} m²")
    ]
    dados_clima_pdf = obter_radiacao_solar_mensal(latitude, longitude)
    dados_sazonais_pdf = variacao_sazonal(latitude, longitude, altura, data_selecionada.year, hora_selecionada)
    pdf_bytes = gerar_relatorio_pdf(
        "Árvore única", parametros_pdf, resultados_pdf,
        dados_clima=dados_clima_pdf, dados_sazonais=dados_sazonais_pdf
    )
    st.download_button("📄 Baixar relatório PDF", data=pdf_bytes, file_name="relatorio_sombra_cacau.pdf", mime="application/pdf")

st.divider()
with st.expander("🌦️ Clima real da região (NASA POWER)"):
    st.caption(
        "Radiação solar média histórica (dados de longo prazo, via NASA POWER) "
        "comparada com a radiação teórica de céu limpo — mostra o quanto a "
        "nebulosidade típica da região reduz a radiação real recebida."
    )
    dados_clima = obter_radiacao_solar_mensal(latitude, longitude)

    if dados_clima is None:
        st.warning("Não foi possível obter os dados climáticos agora (verifique a conexão com a internet).")
    else:
        fig_clima = criar_grafico_radiacao(dados_clima)
        st.plotly_chart(fig_clima, use_container_width=True)

        indice_medio = sum(v for v in dados_clima["indice_ceu_claro"] if v is not None) / 12
        st.metric("Índice médio de céu claro (anual)", f"{indice_medio*100:.0f}%")
        st.caption(
            "Esse índice indica que, em média, a região recebe esse percentual "
            "da radiação solar teórica de céu limpo — o restante é atenuado por nuvens."
        )

with st.expander("📅 Variação sazonal (ano inteiro)"):
    st.caption(
        f"Comprimento da sombra às {hora_selecionada:02d}h, calculado no dia 15 "
        "de cada mês — mostra como a trajetória solar muda ao longo do ano."
    )
    dados_sazonais = variacao_sazonal(latitude, longitude, altura, data_selecionada.year, hora_selecionada)
    fig_sazonal = criar_grafico_sazonal(dados_sazonais)
    st.plotly_chart(fig_sazonal, use_container_width=True)