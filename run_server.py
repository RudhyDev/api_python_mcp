"""
Script para executar o servidor adicionando o diretório raiz ao PYTHONPATH.
"""
import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa e executa o servidor
from src.interfaces.http.server import run_server

def main():
    """Função principal para executar o servidor."""
    run_server()


if __name__ == "__main__":
    main()
