import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def _tabela(dados, colWidths):
    t = Table([[str(c) for c in linha] for linha in dados], colWidths=colWidths)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9E2D4")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def gerar_relatorio_pdf(titulo, parametros, resultados, observacoes=None,
                         dados_clima=None, dados_sazonais=None):
    """
    Gera um relatório em PDF com os parâmetros usados, os resultados
    calculados e, opcionalmente, os dados climáticos reais da região e a
    variação sazonal da sombra ao longo do ano.

    parametros, resultados: listas de tuplas (rótulo, valor)
    observacoes: texto opcional (ex.: recomendação de sombreamento/SAF)
    dados_clima: dicionário retornado por obter_radiacao_solar_mensal (ou None)
    dados_sazonais: lista retornada por variacao_sazonal (ou None)

    Retorna os bytes do PDF gerado (para usar em st.download_button).
    """
    buffer = io.BytesIO()
    documento = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm)
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Sombra Cacau - Relatorio", estilos["Title"]))
    elementos.append(Paragraph(titulo, estilos["Heading2"]))
    elementos.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilos["Normal"]))
    elementos.append(Spacer(1, 0.6 * cm))

    elementos.append(Paragraph("Parametros informados", estilos["Heading3"]))
    elementos.append(_tabela([("Parametro", "Valor")] + parametros, colWidths=[7 * cm, 7 * cm]))
    elementos.append(Spacer(1, 0.5 * cm))

    elementos.append(Paragraph("Resultados", estilos["Heading3"]))
    elementos.append(_tabela([("Resultado", "Valor")] + resultados, colWidths=[7 * cm, 7 * cm]))

    if observacoes:
        elementos.append(Spacer(1, 0.5 * cm))
        elementos.append(Paragraph("Observacoes", estilos["Heading3"]))
        elementos.append(Paragraph(observacoes, estilos["Normal"]))

    if dados_clima:
        elementos.append(Spacer(1, 0.6 * cm))
        elementos.append(Paragraph("Clima real da regiao (NASA POWER)", estilos["Heading3"]))
        elementos.append(Paragraph(
            "Radiacao solar media historica (real) comparada com a radiacao "
            "teorica de ceu limpo, em kWh/m2/dia.", estilos["Normal"]
        ))
        elementos.append(Spacer(1, 0.2 * cm))
        linhas_clima = [("Mes", "Real (kWh/m2/dia)", "Ceu limpo (kWh/m2/dia)")]
        for mes, allsky, clrsky in zip(dados_clima["meses"], dados_clima["allsky"], dados_clima["clrsky"]):
            linhas_clima.append((mes, f"{allsky:.2f}", f"{clrsky:.2f}"))
        elementos.append(_tabela(linhas_clima, colWidths=[4.6 * cm, 4.6 * cm, 4.8 * cm]))

    if dados_sazonais:
        elementos.append(Spacer(1, 0.6 * cm))
        elementos.append(Paragraph("Variacao sazonal (ano inteiro)", estilos["Heading3"]))
        elementos.append(Paragraph(
            "Elevacao solar e comprimento da sombra no dia 15 de cada mes, "
            "no mesmo horario.", estilos["Normal"]
        ))
        elementos.append(Spacer(1, 0.2 * cm))
        linhas_sazonais = [("Mes", "Elevacao solar", "Comprimento da sombra")]
        for item in dados_sazonais:
            elevacao_txt = f"{item['elevacao']:.1f}°" if item["elevacao"] is not None else "-"
            sombra_txt = f"{item['comprimento_sombra']:.2f} m" if item["comprimento_sombra"] is not None else "sem sombra"
            linhas_sazonais.append((item["mes"], elevacao_txt, sombra_txt))
        elementos.append(_tabela(linhas_sazonais, colWidths=[4.6 * cm, 4.6 * cm, 4.8 * cm]))

    documento.build(elementos)
    buffer.seek(0)
    return buffer.getvalue()