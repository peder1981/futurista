"""
Painel Streamlit do projeto Futurista com visualizações aprimoradas.
Inclui gráficos lineares e recursos avançados de análise financeira.
"""
import pandas as pd
import streamlit as st
from futurista.data_loader import EconomicDataLoader
from futurista.visualizer import EconomicVisualizer
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Futurista", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregamento de dados com cache
@st.cache_data(ttl=3600)
def load_data():
    loader = EconomicDataLoader()
    return loader.load_data()

# Carregamento de dados históricos com cache
@st.cache_data(ttl=3600)
def load_historical_data():
    loader = EconomicDataLoader()
    return loader.load_historical_data()

# Função principal
def main():
    # Carregar dados
    df = load_data()
    df_historical = load_historical_data()
    
    # Anos disponíveis
    anos = sorted(df["year"].unique(), reverse=True)
    
    # Título
    st.title(f"🌐 Futurista — Análise Econômica Global")
    st.markdown("Análise avançada entre **juros reais** e **inflação**, com dados do Banco Mundial e projeções futuras.")
    
    # Criação de abas principais
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard Principal", "📈 Análise Histórica", "🔮 Projeções"])
    
    with tab1:
        # Sidebar para Dashboard Principal
        st.sidebar.header("📊 Configurações")
        ano = st.sidebar.selectbox("Selecione o ano", anos, key="ano_dashboard")
        top_n = st.sidebar.slider("Quantidade de países na tabela", 10, 100, 30, key="top_n_dashboard")
        escala_x = st.sidebar.selectbox("Escala eixo X (Inflação)", ["Linear", "Log"], key="escala_x")
        escala_y = st.sidebar.selectbox("Escala eixo Y (Juros)", ["Linear", "Log"], key="escala_y")
        
        # Filtrar dados para o ano selecionado
        df_ano = df[df["year"] == ano].sort_values("ratio", ascending=False).reset_index(drop=True)
        
        # Layout de duas colunas para o mapa e gráfico de dispersão
        col1, col2 = st.columns(2)
        
        with col1:
            # Mapa coroplético
            st.subheader("🗺️ Mapa Global")
            fig_map = EconomicVisualizer.create_choropleth_map(df_ano, ano)
            st.plotly_chart(fig_map, use_container_width=True)
            
        with col2:
            # Gráfico de dispersão modificado (sem bolhas)
            st.subheader("📉 Comparativo: Inflação × Juros")
            fig_scatter = EconomicVisualizer.create_scatter_plot(df_ano, ano)
            fig_scatter.update_layout(
                xaxis_type="log" if escala_x == "Log" else "linear",
                yaxis_type="log" if escala_y == "Log" else "linear"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Gráfico de barras comparativo
        st.subheader(f"📊 Top {top_n} países: Juros vs Inflação")
        fig_bar = EconomicVisualizer.create_comparative_bar_chart(df_ano, ano, top_n=10)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Tabela com os dados
        st.subheader(f"📋 Dados Detalhados — Top {top_n} países")
        st.dataframe(
            df_ano[["country", "iso3", "interest", "inflation", "gap", "ratio"]].head(top_n),
            use_container_width=True,
            column_config={
                "country": "País",
                "iso3": "ISO3",
                "interest": st.column_config.NumberColumn("Juros (%)", format="%.2f"),
                "inflation": st.column_config.NumberColumn("Inflação (%)", format="%.2f"),
                "gap": st.column_config.NumberColumn("Diferença (pp)", format="%.2f"),
                "ratio": st.column_config.NumberColumn("Razão", format="%.2f")
            }
        )
        
        # Downloads
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            csv = df_ano.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Baixar CSV completo", 
                csv, 
                f"futurista_{ano}.csv", 
                mime="text/csv"
            )
        
        with col2:
            md = EconomicVisualizer.create_markdown_table(df_ano, ano, max_rows=top_n)
            st.download_button(
                "📄 Baixar Markdown", 
                md.encode("utf-8"), 
                f"relatorio_{ano}.md", 
                mime="text/markdown"
            )
        
    with tab2:
        # Análise histórica
        st.sidebar.header("📈 Análise Histórica")
        
        # Seleção de países para análise histórica
        preferred_countries = ["Brazil", "United States", "China", "Germany", "Japan"]
        available_countries = sorted(df["country"].unique())
        
        # Filtrar apenas os países preferidos que realmente existem nos dados
        default_countries = [c for c in preferred_countries if c in available_countries]
        
        # Se não houver correspondência, usar os 5 primeiros disponíveis
        if not default_countries and len(available_countries) > 0:
            default_countries = available_countries[:min(5, len(available_countries))]
        
        selected_countries = st.sidebar.multiselect(
            "Selecione os países para análise",
            available_countries,
            default=default_countries,
            key="countries_historical"
        )
        
        indicator = st.sidebar.selectbox(
            "Indicador para análise",
            ["ratio", "interest", "inflation", "gap"],
            format_func=lambda x: {
                "ratio": "Juros / Inflação", 
                "interest": "Juros (%)", 
                "inflation": "Inflação (%)", 
                "gap": "Diferença (pp)"
            }.get(x),
            key="indicator_historical"
        )
        
        if selected_countries:
            st.subheader("📈 Análise Histórica")
            fig_trend = EconomicVisualizer.create_trend_line_chart(
                df_historical, 
                countries=selected_countries, 
                indicator=indicator
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Tabela histórica
            st.subheader("📋 Dados Históricos")
            df_historical_filtered = df_historical[
                (df_historical["country"].isin(selected_countries)) & 
                (df_historical[indicator].notna())
            ].sort_values(["country", "year"])
            
            st.dataframe(
                df_historical_filtered[["country", "year", "interest", "inflation", "gap", "ratio"]],
                use_container_width=True,
                column_config={
                    "country": "País",
                    "year": "Ano",
                    "interest": st.column_config.NumberColumn("Juros (%)", format="%.2f"),
                    "inflation": st.column_config.NumberColumn("Inflação (%)", format="%.2f"),
                    "gap": st.column_config.NumberColumn("Diferença (pp)", format="%.2f"),
                    "ratio": st.column_config.NumberColumn("Razão", format="%.2f")
                }
            )
        else:
            st.info("Selecione pelo menos um país para ver a análise histórica.")
        
    with tab3:
        # Projeções
        st.sidebar.header("🔮 Projeções")
        
        projection_countries = st.sidebar.multiselect(
            "Selecione os países para projeção",
            available_countries,
            default=default_countries[:3],
            key="countries_projection"
        )
        
        projection_indicator = st.sidebar.selectbox(
            "Indicador para projeção",
            ["ratio", "interest", "inflation", "gap"],
            format_func=lambda x: {
                "ratio": "Juros / Inflação", 
                "interest": "Juros (%)", 
                "inflation": "Inflação (%)", 
                "gap": "Diferença (pp)"
            }.get(x),
            key="indicator_projection"
        )
        
        years_ahead = st.sidebar.slider("Anos de projeção", 1, 10, 5, key="years_ahead")
        
        if projection_countries:
            st.subheader("🔮 Projeção de Tendências Futuras")
            
            try:
                fig_projection, df_projection = EconomicVisualizer.create_projection_chart(
                    df_historical, 
                    countries=projection_countries,
                    indicator=projection_indicator,
                    years_ahead=years_ahead
                )
                st.plotly_chart(fig_projection, use_container_width=True)
                
                # Dados da projeção
                st.subheader("📋 Dados da Projeção")
                st.dataframe(
                    df_projection,
                    use_container_width=True,
                    column_config={
                        "country": "País",
                        "year": "Ano",
                        projection_indicator: st.column_config.NumberColumn(
                            {
                                "ratio": "Juros / Inflação", 
                                "interest": "Juros (%)", 
                                "inflation": "Inflação (%)", 
                                "gap": "Diferença (pp)"
                            }.get(projection_indicator),
                            format="%.2f"
                        ),
                        "type": "Tipo"
                    }
                )
                
                # Download dos dados de projeção
                csv_projection = df_projection.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Baixar projeção (CSV)", 
                    csv_projection, 
                    f"projecao_{anos[-1] + years_ahead}.csv", 
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Erro ao gerar projeção: {e}")
                st.info("Verifique se há dados históricos suficientes para os países selecionados.")
        else:
            st.info("Selecione pelo menos um país para ver as projeções.")

    # Rodapé
    st.divider()
    st.caption("Fonte: Dados do Banco Mundial | Projeto Futurista")

if __name__ == "__main__":
    main()
