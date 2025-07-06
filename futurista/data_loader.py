"""
Módulo responsável pelo carregamento e processamento de dados econômicos.
"""
import pandas as pd
import world_bank_data as wb
import pycountry
import numpy as np
from datetime import datetime

class EconomicDataLoader:
    """
    Classe para carregamento e processamento de dados econômicos.
    Suporta carregamento de dados de um único ano ou séries históricas.
    """
    
    def __init__(self):
        """
        Inicializa o carregador de dados econômicos.
        """
        self.default_start_year = 1990
        self.default_end_year = datetime.now().year - 1  # Ano anterior ao atual
        self.indicators = {
            "inflation": "FP.CPI.TOTL.ZG",  # Inflação anual (%)
            "interest": "FR.INR.RINR"       # Taxa real de juros (%)
        }
    
    @staticmethod
    def get_country_info(name):
        """
        Obtém o código ISO3 e nome oficial de um país.
        
        Args:
            name (str): Nome do país para busca
            
        Returns:
            pd.Series: Série com [código ISO3, nome oficial]
        """
        try:
            country = pycountry.countries.lookup(name)
            return pd.Series([country.alpha_3, country.name])
        except:
            return pd.Series([None, name])
    
    def load_data(self, year=None):
        """
        Carrega dados econômicos para o ano especificado ou o mais recente disponível.
        
        Args:
            year (int, optional): Ano específico para busca. Se None, usa o mais recente.
            
        Returns:
            pd.DataFrame: DataFrame processado com os dados econômicos
        """
        # Carregar todos os dados históricos
        df = self.load_historical_data()
        
        # Se não especificou ano, usar o mais recente disponível
        if year is None:
            year = df['year'].max()
        
        # Filtrar para o ano desejado
        return df[df['year'] == year]
    
    def load_historical_data(self, start_year=None, end_year=None):
        """
        Carrega dados históricos de inflação e juros do Banco Mundial.
        
        Args:
            start_year (int, optional): Ano inicial para busca
            end_year (int, optional): Ano final para busca
            
        Returns:
            pd.DataFrame: DataFrame processado com os dados econômicos históricos
        """
        # Usar valores padrão se não especificados
        if start_year is None:
            start_year = self.default_start_year
        if end_year is None:
            end_year = self.default_end_year
            
        date_range = f"{start_year}:{end_year}"
        
        # Carregar dados
        inflation = wb.get_series(self.indicators["inflation"], date=date_range, id_or_value="id").reset_index()
        interest = wb.get_series(self.indicators["interest"], date=date_range, id_or_value="id").reset_index()
        
        # Processar dados
        merged = pd.merge(inflation, interest, on=["Country", "Year"], how="inner")
        merged.rename(columns={
            "Country": "country_raw",
            "Year": "year",
            self.indicators["inflation"]: "inflation",
            self.indicators["interest"]: "interest"
        }, inplace=True)
        
        # Adicionar informações do país
        merged[["iso3", "country"]] = merged["country_raw"].apply(self.get_country_info)
        
        # Calcular indicadores
        merged["ratio"] = merged["interest"] / merged["inflation"]
        merged["gap"] = merged["interest"] - merged["inflation"]
        
        # Filtrar dados
        filtered = merged[
            (merged["inflation"] > 0) & 
            (merged["iso3"].notna()) & 
            (merged["ratio"].notna())
        ]
        
        return filtered.sort_values(["country", "year"]).reset_index(drop=True)
