#!/bin/bash

echo "🚀 Iniciando execução do projeto futurista..."

# Verifica se o ambiente virtual já existe
if [ ! -d "venv" ]; then
    echo "🛠️ Criando ambiente virtual 'venv'..."
    python3 -m venv venv
fi

# Ativa o ambiente virtual
source venv/bin/activate

# Atualiza pip
pip install --upgrade pip

# Instala dependências necessárias
echo "📦 Instalando dependências..."
pip install pandas world_bank_data pycountry plotly

# Executa o script principal
echo "▶️ Executando futurista.py..."
python futurista.py

# Desativa o ambiente virtual
deactivate

