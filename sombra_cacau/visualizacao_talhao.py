import plotly.graph_objects as go


def criar_grafico_talhao(resultado, largura_talhao, comprimento_talhao, raio_copa):
    """
    Cria um gráfico 2D (vista de cima) do talhão: contorno da área,
    copas das árvores (verde) e sombra projetada de cada uma (laranja),
    já considerando a sobreposição entre árvores vizinhas.
    """
    fig = go.Figure()

    fig.add_shape(
        type="rect", x0=0, y0=0, x1=largura_talhao, y1=comprimento_talhao,
        line=dict(color="#3D2B1F", width=2)
    )

    for poligono in resultado["poligonos"]:
        x, y = poligono.exterior.xy
        fig.add_trace(go.Scatter(
            x=list(x), y=list(y), fill="toself",
            fillcolor="rgba(230,103,0,0.35)",
            line=dict(color="rgba(230,103,0,0.6)"),
            mode="lines", showlegend=False, hoverinfo="skip"
        ))

    for x, y in resultado["arvores"]:
        fig.add_shape(
            type="circle",
            x0=x - raio_copa, y0=y - raio_copa, x1=x + raio_copa, y1=y + raio_copa,
            fillcolor="rgba(46,125,69,0.85)", line=dict(color="#1F5C34")
        )

    fig.update_xaxes(title="Leste – Oeste (m)", scaleanchor="y", scaleratio=1)
    fig.update_yaxes(title="Norte – Sul (m)")
    fig.update_layout(
        height=520, margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white"
    )
    return fig