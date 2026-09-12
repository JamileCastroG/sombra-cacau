# Software de Projeção de Sombra — Cacaueiro

Ferramenta para calcular a área de sombra projetada por árvores de cacau, 
com base em coordenadas geográficas, data/horário e características da árvore 
(altura ou idade, raio da copa).

## Como instalar

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `venv\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute: `streamlit run app.py`

## Status

Protótipo funcional em desenvolvimento — projeto acadêmico (Agrometeorologia).


## Funcionamento offline

O núcleo de cálculo do software funciona **sem necessidade de internet**:

- Cálculo de posição solar (biblioteca `pvlib` + `timezonefinder`, totalmente local)
- Cálculo de sombra (árvore única e talhão com múltiplas árvores)
- Cena 3D ilustrativa (árvore, sombra, sol, bússola — bibliotecas JS embutidas localmente)
- Recomendação de espécies de sombreamento (SAF)
- Classificação do percentual de sombreamento ideal
- Relatório em PDF (parâmetros e resultados do cálculo)

As seguintes funcionalidades **exigem conexão com a internet**:

- Geolocalização automática (GPS do navegador ou estimativa por IP) — sem internet, usa a localização padrão configurada (Tomé-Açu, PA), que pode ser ajustada manualmente
- Aba "Mapa real" (imagem de satélite)
- Dados climáticos históricos reais (NASA POWER) e a seção correspondente no relatório PDF
- Variação sazonal ao longo do ano (usa os mesmos cálculos locais de posição solar, então na prática funciona offline — só a seção de clima do relatório depende de internet)

- **Nota sobre GPS em rede local**: o botão de GPS do navegador só funciona em `localhost` ou HTTPS (restrição de segurança dos navegadores) — ao acessar pelo IP da rede local (ex.: pelo celular), o GPS do navegador fica indisponível; nesse caso, digite as coordenadas manualmente (lidas de outro app de mapa, por exemplo).