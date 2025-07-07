"""
Interface web Streamlit para o Futurista: análise econômica interativa de juros e inflação.
"""
import streamlit as st
import pandas as pd

from futurista.data_loader import EconomicDataLoader
from futurista.visualizer import EconomicVisualizer
from futurista.exporter import DataExporter

# Configuração da página
st.set_page_config(
    page_title="Futurista - Análise Econômica",
    page_icon="🌎",
    layout="wide"
)

# Título e descrição
st.title("🌎 Futurista — Análise Econômica Interativa")
st.markdown("""
Análise e visualização interativa entre **juros reais** e **inflação anual** com dados do Banco Mundial.
""")

# Inicialização do carregador de dados
@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_dados():
    """Função para carregar e cachear os dados econômicos"""
    loader = EconomicDataLoader()
    return loader.load_historical_data()

# Barra de progresso para carregamento
with st.spinner("🔄 Carregando dados econômicos do Banco Mundial..."):
    dados = carregar_dados()
    anos_disponiveis = sorted(dados["year"].unique(), reverse=True)

# Sidebar para controles
st.sidebar.header("📊 Controles")

# Seleção de ano
ano = st.sidebar.selectbox(
    "Selecione o ano:",
    anos_disponiveis,
    index=0  # Selecionar o ano mais recente por padrão
)

# Número de países a exibir
num_paises = st.sidebar.slider(
    "Número de países na tabela:",
    min_value=10,
    max_value=100,
    value=50,
    step=10
)

# Filtrar dados para o ano selecionado
df_ano = dados[dados["year"] == ano].copy()
df_sorted = df_ano.sort_values("ratio", ascending=False).reset_index(drop=True)

# Métricas principais
st.header(f"📈 Visão Geral — {ano}")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Países analisados",
        value=len(df_ano)
    )

with col2:
    media_juros = df_ano["interest"].mean()
    st.metric(
        label="Média de juros reais",
        value=f"{media_juros:.2f}%"
    )

with col3:
    media_inflacao = df_ano["inflation"].mean()
    st.metric(
        label="Média de inflação",
        value=f"{media_inflacao:.2f}%"
    )

# Tabela ordenada
st.header(f"🏆 Top {num_paises} países por razão juros/inflação")
df_display = df_sorted.head(num_paises).reset_index(drop=True)
df_display = df_display[["country", "iso3", "interest", "inflation", "gap", "ratio"]]
df_display.columns = ["País", "ISO3", "Juros (%)", "Inflação (%)", "Diferença (pp)", "Razão"]
st.dataframe(
    df_display, 
    use_container_width=True,
    hide_index=True
)

# Mapa interativo
st.header("🗺️ Mapa interativo: Juros/Inflação")
mapa = EconomicVisualizer.create_choropleth_map(df_sorted, ano)
st.plotly_chart(mapa, use_container_width=True)

# Gráfico de dispersão
st.header("📉 Dispersão: Inflação × Juros")
scatter = EconomicVisualizer.create_scatter_plot(df_sorted, ano)
st.plotly_chart(scatter, use_container_width=True)

# Gráfico comparativo para os top países
st.header(f"📊 Comparativo: Top 10 países ({ano})")
bar = EconomicVisualizer.create_comparative_bar_chart(df_sorted, ano, top_n=10)
st.plotly_chart(bar, use_container_width=True)

# Análise de tendência para países selecionados
st.header("📈 Análise de tendências históricas")

# Seleção de países para análise de tendência
paises_disponiveis = sorted(dados["country"].unique())
paises_selecionados = st.multiselect(
    "Selecione países para análise de tendência:",
    paises_disponiveis,
    default=df_sorted["country"].head(5).tolist()
)

if paises_selecionados:
    # Tipo de indicador para análise
    indicador = st.radio(
        "Indicador para análise:",
        ["ratio", "interest", "inflation", "gap"],
        format_func=lambda x: {
            "ratio": "Razão Juros/Inflação", 
            "interest": "Juros Reais (%)", 
            "inflation": "Inflação (%)",
            "gap": "Diferença (pp)"
        }[x],
        horizontal=True
    )
    
    # Gráfico de tendência
    trend = EconomicVisualizer.create_trend_line_chart(
        dados, 
        countries=paises_selecionados, 
        indicator=indicador
    )
    st.plotly_chart(trend, use_container_width=True)

    # Projeção futura
    st.header("🔮 Projeção futura")
    anos_projecao = st.slider(
        "Anos para projeção:",
        min_value=1,
        max_value=10,
        value=5
    )
    
    projection, proj_data = EconomicVisualizer.create_projection_chart(
        dados,
        countries=paises_selecionados,
        indicator=indicador,
        years_ahead=anos_projecao
    )
    st.plotly_chart(projection, use_container_width=True)

# Exportação de dados
st.sidebar.header("💾 Exportar dados")

if st.sidebar.button("Exportar dados do ano atual"):
    arquivos = DataExporter.export_all_formats(df_sorted, ano)
    st.sidebar.success(f"✅ Arquivos exportados: {', '.join(arquivos.values())}")
    
    # Links para download
    for formato, arquivo in arquivos.items():
        with open(arquivo, "rb") as f:
            st.sidebar.download_button(
                label=f"Baixar {formato.upper()}",
                data=f,
                file_name=arquivo,
                mime="text/csv" if formato == "csv" else "text/markdown"
            )

# Rodapé
st.sidebar.markdown("---")
st.sidebar.caption("© 2023-2025 Futurista")
st.sidebar.caption("Dados fornecidos pelo Banco Mundial")
