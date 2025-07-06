"""
Aplicação interativa para análise de juros e inflação mundial.

Versão modularizada e melhorada do notebook futurista_interativo.ipynb.
"""
import ipywidgets as widgets
from IPython.display import display

from futurista.data_loader import EconomicDataLoader
from futurista.visualizer import EconomicVisualizer
from futurista.exporter import DataExporter

def main():
    """
    Inicializa a aplicação interativa.
    """
    print("🔧 Carregando dados econômicos...")
    # Carregar dados
    loader = EconomicDataLoader()
    dados = loader.load_historical_data()
    print(f"✅ Dados carregados com sucesso! {dados.shape[0]} registros disponíveis.")
    
    # Configurar interface
    anos_disponiveis = sorted(dados["year"].unique(), reverse=True)
    ano_widget = widgets.Dropdown(options=anos_disponiveis, description="Ano:")
    
    def atualizar_analise(ano):
        """
        Atualiza a análise com base no ano selecionado.
        
        Args:
            ano (int): Ano para análise
        """
        # Filtrar dados
        df = dados[dados["year"] == ano].copy()
        df_sorted = df.sort_values("ratio", ascending=False).reset_index(drop=True)
        
        # Exibir tabela
        EconomicVisualizer.display_markdown_table(df_sorted, ano)
        
        # Criar e exibir mapa
        mapa = EconomicVisualizer.create_choropleth_map(df_sorted, ano)
        mapa.show()
        
        # Criar e exibir gráfico de dispersão
        scatter = EconomicVisualizer.create_scatter_plot(df_sorted, ano)
        scatter.show()
        
        # Criar e exibir gráfico comparativo para os top 10 países
        bar = EconomicVisualizer.create_comparative_bar_chart(df_sorted, ano, top_n=10)
        bar.show()
        
        # Analisar tendências históricas para os top 5 países
        top_countries = df_sorted.head(5)["country"].tolist()
        print(f"\n📈 Analisando tendências históricas para {', '.join(top_countries)}...")
        
        # Gráfico de tendência histórica
        trend = EconomicVisualizer.create_trend_line_chart(dados, top_countries)
        trend.show()
        
        # Exportar dados
        DataExporter.export_all_formats(df_sorted, ano)
    
    # Conectar widget à função
    widgets.interact(atualizar_analise, ano=ano_widget)

if __name__ == "__main__":
    # Executar para uso direto do script
    print("🚀 Inicializando Futurista App...")
    main()
    
# Para usar em um notebook:
"""
# Execute este código em uma célula de notebook para iniciar a aplicação
from futurista_app import main
main()
"""
