import plotly.graph_objects as go


def criar_grafico_radiacao(dados_clima):
    """
    Cria um gráfico de barras comparando a radiação solar real média
    histórica (ALLSKY) com a radiação teórica de céu limpo (CLRSKY),
    mês a mês.
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dados_clima["meses"], y=dados_clima["clrsky"],
        name="Céu limpo (teórico)",
        marker_color="rgba(255,196,74,0.55)"
    ))
    fig.add_trace(go.Bar(
        x=dados_clima["meses"], y=dados_clima["allsky"],
        name="Real (histórico)",
        marker_color="rgba(107,66,38,0.85)"
    ))

    fig.update_layout(
        barmode="group",
        yaxis_title="Radiação solar (kWh/m²/dia)",
        height=380,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="white"
    )
    return fig