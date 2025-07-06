@echo off
:MENU
echo.
echo 🧠 Projeto Futurista - Menu Interativo
echo 1. Criar ambiente virtual e instalar dependências
echo 2. Executar futurista_app.py (versão modularizada)
echo 3. Executar futurista.py (versão original)
echo 4. Iniciar painel web (Streamlit)
echo 5. Sair
set /p opcao=Escolha uma opcao:

if "%opcao%"=="1" (
  if not exist venv (
    python -m venv venv
  )
  call venv\Scripts\activate.bat
  pip install --upgrade pip
  pip install -r requirements.txt
  goto MENU
)

if "%opcao%"=="2" (
  call venv\Scripts\activate.bat
  python futurista_app.py
  goto MENU
)

if "%opcao%"=="3" (
  call venv\Scripts\activate.bat
  python futurista.py
  goto MENU
)

if "%opcao%"=="4" (
  call venv\Scripts\activate.bat
  streamlit run futurista_streamlit.py
  goto MENU
)

if "%opcao%"=="5" (
  echo 👋 Encerrando...
  exit
)

echo ❌ Opção inválida.
goto MENU

