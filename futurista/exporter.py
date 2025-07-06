"""
Módulo responsável pela exportação de dados para diversos formatos.
"""
import os

class DataExporter:
    """
    Classe para exportação de dados econômicos.
    """
    
    @staticmethod
    def export_to_csv(df, year, prefix="analise_mundial"):
        """
        Exporta os dados para CSV.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            year (int): Ano dos dados
            prefix (str): Prefixo para o nome do arquivo
            
        Returns:
            str: Caminho do arquivo gerado
        """
        filename = f"{prefix}_{year}.csv"
        df[["country", "iso3", "year", "interest", "inflation", "gap", "ratio"]].to_csv(
            filename, index=False
        )
        return filename
    
    @staticmethod
    def export_to_markdown(df, year, prefix="relatorio_mundial"):
        """
        Exporta os dados para Markdown.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            year (int): Ano dos dados
            prefix (str): Prefixo para o nome do arquivo
            
        Returns:
            str: Caminho do arquivo gerado
        """
        filename = f"{prefix}_{year}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# 🌍 Análise Econômica Mundial — {year}\n\n")
            f.write("| País | ISO3 | Juros (%) | Inflação (%) | Diferença (pp) | Razão |\n")
            f.write("|------|------|------------|----------------|----------------|--------|\n")
            for _, row in df.iterrows():
                f.write(
                    f"| {row['country']} | {row['iso3']} | {row['interest']:.2f} | "
                    f"{row['inflation']:.2f} | {row['gap']:.2f} | {row['ratio']:.2f} |\n"
                )
        return filename
    
    @staticmethod
    def export_all_formats(df, year):
        """
        Exporta os dados para todos os formatos disponíveis.
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            year (int): Ano dos dados
            
        Returns:
            dict: Dicionário com os caminhos dos arquivos gerados
        """
        csv_file = DataExporter.export_to_csv(df, year)
        md_file = DataExporter.export_to_markdown(df, year)
        
        print(f"📁 Exportado: {csv_file} e {md_file}")
        return {"csv": csv_file, "markdown": md_file}
