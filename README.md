# 🌎 Futurista — Análise Econômica Interativa

O **Futurista** é uma aplicação Python para análise, visualização e comparação interativa entre **juros reais** e **inflação anual** com dados do Banco Mundial.

---

## 🚀 Funcionalidades

- 📊 Tabela ordenada com todos os países disponíveis
- 🗺️ Mapa interativo com escala de razão juros/inflação
- 📉 Gráfico de dispersão com gap e escalas ajustáveis
- 💾 Exportação de CSV e Markdown
- 💻 Interface em Streamlit (painel web)

---

## 🔨 Uso

### Via Script Python Interativo

Execute o script Python com interface interativa:

```bash
python futurista_app.py
```

### Via Módulos (uso avançado)

```python
# Importando os componentes individuais
from futurista.data_loader import load_economic_data
from futurista.visualizer import EconomicVisualizer
from futurista.exporter import DataExporter

# Carregando dados
dados = load_economic_data(start_year=1990, end_year=2023)

# Filtrando para um ano específico
ano = 2023
df = dados[dados["year"] == ano].sort_values("ratio", ascending=False)

# Criando visualizações
mapa = EconomicVisualizer.create_choropleth_map(df, ano)
mapa.show()

# Exportando dados
DataExporter.export_all_formats(df, ano)
```

### Via Terminal (script original)

```bash
python futurista.py  # Gera relatório para o ano mais recente
```

### Via Streamlit

```bash
streamlit run futurista_streamlit.py
```

---

## 📁 Estrutura do Projeto

```
futurista/
├── futurista/                # Pacote principal
│   ├── __init__.py          # Exportação das funções principais
│   ├── data_loader.py       # Módulo para carregamento de dados
│   ├── visualizer.py        # Módulo para visualização
│   └── exporter.py          # Módulo para exportação de dados
├── futurista_app.py         # Aplicação interativa modularizada
├── futurista.py             # Script principal original
├── futurista_streamlit.py   # Interface Streamlit
└── requirements.txt         # Dependências do projeto
```

## 📈 Próximos Passos e Oportunidades de Melhoria

1. **Cache de Dados**: Implementar cache para as consultas ao Banco Mundial, reduzindo o tempo de carregamento.
2. **Testes Unitários**: Adicionar testes para garantir a robustez das funções.
3. **Personalização Visual**: Permitir que o usuário customize as visualizações.
4. **Indicadores Adicionais**: Expandir para outros indicadores econômicos.
5. **APIs Alternativas**: Implementar suporte a outras fontes de dados econômicos.
6. **Análise Histórica**: Adicionar gráficos temporais para analisar a evolução dos indicadores.
7. **Internacionalização**: Suporte a múltiplos idiomas.

---

## ⚙️ Instalação

```bash
git clone https://github.com/seuusuario/futurista.git
cd futurista
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt

