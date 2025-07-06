"""
Módulo responsável pelas visualizações de dados econômicos.
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import display, Markdown
import numpy as np
from scipy import stats
import pandas as pd

class EconomicVisualizer:
    """
    Classe para criação de visualizações de dados econômicos.
    """
    
    @staticmethod
    def create_markdown_table(df, year, max_rows=50):
        """
        Cria uma tabela markdown formatada com os dados.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            year (int): Ano dos dados
            max_rows (int): Número máximo de linhas na tabela
            
        Returns:
            str: Tabela markdown formatada
        """
        md = f"## 🌍 Juros Reais vs Inflação — {year}\n\n"
        md += "| País | ISO3 | Juros (%) | Inflação (%) | Diferença (pp) | Razão |\n"
        md += "|------|------|------------|----------------|----------------|--------|\n"
        
        for _, row in df.head(max_rows).iterrows():
            md += f"| {row['country']} | {row['iso3']} | {row['interest']:.2f} | "
            md += f"{row['inflation']:.2f} | {row['gap']:.2f} | {row['ratio']:.2f} |\n"
            
        return md
    
    @staticmethod
    def display_markdown_table(df, year, max_rows=50):
        """
        Exibe uma tabela markdown formatada.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            year (int): Ano dos dados
            max_rows (int): Número máximo de linhas na tabela
        """
        md = EconomicVisualizer.create_markdown_table(df, year, max_rows)
        display(Markdown(md))
    
    @staticmethod
    def create_choropleth_map(df, year):
        """
        Cria um mapa coroplético com os dados.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            year (int): Ano dos dados
            
        Returns:
            plotly.graph_objects.Figure: Figura do mapa
        """
        fig = px.choropleth(
            df,
            locations="iso3",
            color="ratio",
            hover_name="country",
            color_continuous_scale="Plasma",
            title=f"🌐 Juros / Inflação — {year}",
            labels={"ratio": "Juros / Inflação"}
        )
        fig.update_geos(showframe=False, showcoastlines=False)
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
        
        return fig
    
    @staticmethod
    def create_scatter_plot(df, year):
        """
        Cria um gráfico de dispersão com os dados.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            year (int): Ano dos dados
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico de dispersão
        """
        fig = px.scatter(
            df,
            x="inflation",
            y="interest",
            color="ratio",
            hover_name="country",
            title=f"📉 Dispersão: Inflação × Juros — {year}",
            labels={"interest": "Juros (%)", "inflation": "Inflação (%)"}
        )
        fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1.0, color='DarkSlateGrey')))
        
        # Adiciona linha de referência onde juros = inflação
        max_val = max(df["interest"].max(), df["inflation"].max()) * 1.1
        fig.add_shape(
            type="line", 
            x0=0, y0=0, 
            x1=max_val, y1=max_val,
            line=dict(color="grey", width=1, dash="dash")
        )
        fig.add_annotation(
            x=max_val*0.7, 
            y=max_val*0.7, 
            text="Juros = Inflação", 
            showarrow=False,
            font=dict(color="grey")
        )
        
        return fig

    @staticmethod
    def create_trend_line_chart(df, countries=None, indicator="ratio"):
        """
        Cria um gráfico de linhas com tendências históricas.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados históricos
            countries (list): Lista de países para incluir no gráfico
            indicator (str): Indicador a ser plotado ('ratio', 'interest', 'inflation', 'gap')
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico de linhas
        """
        if countries:
            filtered_df = df[df["country"].isin(countries)]
        else:
            # Pegar os 10 países com os valores mais altos do indicador no ano mais recente
            max_year = df["year"].max()
            latest_df = df[df["year"] == max_year].sort_values(indicator, ascending=False)
            top_countries = latest_df["country"].head(10).unique().tolist()
            filtered_df = df[df["country"].isin(top_countries)]
        
        indicator_labels = {
            "ratio": "Juros / Inflação",
            "interest": "Juros (%)",
            "inflation": "Inflação (%)",
            "gap": "Diferença (pp)"
        }
        
        fig = px.line(
            filtered_df,
            x="year",
            y=indicator,
            color="country",
            hover_name="country",
            title=f"📈 Tendência Histórica: {indicator_labels.get(indicator, indicator)}",
            labels={
                "year": "Ano", 
                indicator: indicator_labels.get(indicator, indicator)
            }
        )
        
        fig.update_layout(
            legend_title_text="País",
            xaxis=dict(
                title="Ano",
                tickmode="linear",
                tick0=filtered_df["year"].min(),
                dtick=5  # Intervalo de 5 anos
            )
        )
        
        return fig
        
    @staticmethod
    def create_projection_chart(df, countries, indicator="ratio", years_ahead=5):
        """
        Cria um gráfico de projeção para os próximos anos.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados históricos
            countries (list): Lista de países para projetar
            indicator (str): Indicador a ser projetado
            years_ahead (int): Número de anos para projetar
            
        Returns:
            plotly.graph_objects.Figure: Figura com projeções
            pd.DataFrame: DataFrame com os dados projetados
        """
        indicator_labels = {
            "ratio": "Juros / Inflação",
            "interest": "Juros (%)",
            "inflation": "Inflação (%)",
            "gap": "Diferença (pp)"
        }
        
        # Filtrar dados para os países selecionados
        filtered_df = df[df["country"].isin(countries)]
        
        # Anos disponíveis e último ano
        years = filtered_df["year"].unique()
        max_year = filtered_df["year"].max()
        min_year = max(filtered_df["year"].min(), max_year - 10)  # Últimos 10 anos para projeção
        
        # DataFrame para armazenar projeções
        projection_data = []
        
        # Para cada país, calcular a tendência e projetar
        for country in countries:
            country_data = filtered_df[(filtered_df["country"] == country) & 
                                     (filtered_df["year"] >= min_year)]
            
            if len(country_data) < 3:  # Precisamos de pelo menos 3 pontos para uma regressão confiável
                continue
            
            x = country_data["year"].values
            y = country_data[indicator].values
            
            # Regressão linear para tendência
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Adicionar dados históricos ao resultado
            for idx, row in country_data.iterrows():
                projection_data.append({
                    "country": country,
                    "year": row["year"],
                    indicator: row[indicator],
                    "type": "Histórico"
                })
            
            # Calcular projeções
            for year in range(max_year + 1, max_year + years_ahead + 1):
                predicted_value = slope * year + intercept
                
                # Garantir valores mínimos razoáveis
                if indicator in ["interest", "inflation"]:
                    predicted_value = max(0.1, predicted_value)  # Mínimo de 0.1%
                
                projection_data.append({
                    "country": country,
                    "year": year,
                    indicator: predicted_value,
                    "type": "Projeção"
                })
        
        # Criar DataFrame com projeções
        projection_df = pd.DataFrame(projection_data)
        
        # Criar gráfico
        fig = px.line(
            projection_df,
            x="year",
            y=indicator,
            color="country",
            line_dash="type",  # Linha tracejada para projeções
            hover_name="country",
            title=f"🔮 Projeção: {indicator_labels.get(indicator, indicator)} para {max_year + years_ahead}",
            labels={"year": "Ano", indicator: indicator_labels.get(indicator, indicator)}
        )
        
        fig.update_layout(
            legend_title_text="País",
            xaxis=dict(
                title="Ano",
                tickmode="linear",
                tick0=min_year,
                dtick=2  # Intervalo de 2 anos
            )
        )
        
        # Adicionar linha vertical separando histórico de projeção
        fig.add_vline(
            x=max_year + 0.5,  # Linha entre último ano de dados e primeiro ano projetado
            line_width=1,
            line_dash="dash",
            line_color="grey",
            annotation_text="Início Projeção",
            annotation_position="top right"
        )
        
        return fig, projection_df
    
    @staticmethod
    def create_comparative_bar_chart(df, year, top_n=10, indicator="ratio"):
        """
        Cria um gráfico de barras comparativo para os principais países.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            year (int): Ano dos dados
            top_n (int): Número de países a incluir
            indicator (str): Indicador para ordenar os países
            
        Returns:
            plotly.graph_objects.Figure: Figura do gráfico de barras
        """
        indicator_labels = {
            "ratio": "Juros / Inflação",
            "interest": "Juros (%)",
            "inflation": "Inflação (%)",
            "gap": "Diferença (pp)"
        }
        
        # Filtrar para o ano selecionado e top N países
        filtered_df = df[df["year"] == year].sort_values(indicator, ascending=False).head(top_n)
        
        fig = px.bar(
            filtered_df,
            x="country",
            y=["interest", "inflation"],
            title=f"📊 Comparativo: Juros vs Inflação — Top {top_n} ({year})",
            labels={
                "value": "Percentual (%)", 
                "country": "País", 
                "variable": "Indicador"
            },
            barmode="group",
            color_discrete_map={"interest": "#2E86C1", "inflation": "#E74C3C"}
        )
        
        # Adicionar linha para a razão juros/inflação no eixo secundário
        if indicator == "ratio":
            fig.add_trace(
                px.line(
                    filtered_df, 
                    x="country", 
                    y="ratio", 
                    markers=True
                ).data[0],
                secondary_y=True
            )
            
            # Configurar eixo Y secundário
            fig.update_layout(
                yaxis2=dict(
                    title="Razão Juros/Inflação",
                    overlaying="y",
                    side="right"
                )
            )
        
        # Melhorar layout
        fig.update_layout(
            xaxis_tickangle=-45,
            legend_title_text="Indicador",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
