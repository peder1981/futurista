@echo off
echo 🚀 Iniciando execução do projeto futurista...

REM Verifica se o ambiente virtual já existe
IF NOT EXIST venv (
    echo 🛠️ Criando ambiente virtual 'venv'...
    python -m venv venv
)

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Atualiza pip
python -m pip install --upgrade pip

REM Instala dependências
echo 📦 Instalando dependências...
pip install pandas world_bank_data pycountry plotly

REM Executa o script principal
echo ▶️ Executando futurista.py...
python futurista.py

REM Desativa o ambiente virtual
deactivate

