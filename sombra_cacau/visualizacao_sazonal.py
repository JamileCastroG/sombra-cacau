import plotly.graph_objects as go


def criar_grafico_sazonal(dados_sazonais):
    """
    Cria um gráfico de linha mostrando o comprimento da sombra
    (no mesmo horário fixo) ao longo dos 12 meses do ano.
    """
    meses = [d["mes"] for d in dados_sazonais]
    comprimentos = [d["comprimento_sombra"] if d["comprimento_sombra"] is not None else 0 for d in dados_sazonais]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses, y=comprimentos, mode="lines+markers",
        line=dict(color="#6B4226", width=3),
        marker=dict(size=7, color="#E67E00")
    ))
    fig.update_layout(
        yaxis_title="Comprimento da sombra (m)",
        height=380,
        margin=dict(l=10, r=10, t=20, b=10),
        plot_bgcolor="white"
    )
    return fig