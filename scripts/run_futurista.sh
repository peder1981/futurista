#!/bin/bash

echo "🧠 Projeto Futurista - Menu Interativo"

while true; do
  echo ""
  echo "1. Criar ambiente virtual e instalar dependências"
  echo "2. Executar futurista_app.py (versão modularizada)"
  echo "3. Executar futurista.py (versão original)"
  echo "4. Iniciar painel web (Streamlit)"
  echo "5. Sair"
  read -p "Escolha uma opção: " opcao

  case $opcao in
    1)
      [ ! -d "venv" ] && python3 -m venv venv
      source venv/bin/activate
      pip install --upgrade pip
      pip install -r requirements.txt
      ;;
    2)
      source venv/bin/activate
      python futurista_app.py
      ;;
    3)
      source venv/bin/activate
      python futurista.py
      ;;
    4)
      source venv/bin/activate
      streamlit run futurista_streamlit.py
      ;;
    5)
      echo "👋 Encerrando..."
      break
      ;;
    *)
      echo "❌ Opção inválida."
      ;;
  esac
done

