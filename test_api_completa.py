"""
Script para testar a funcionalidade completa da API.
"""
import os
import sys
import threading
import time
import requests

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.interfaces.http.server import run_server


def test_api_functionality():
    """Testa a funcionalidade completa da API."""
    print("Iniciando servidor de teste...")
    
    # Inicia o servidor em uma thread separada
    server_thread = threading.Thread(target=run_server, args=(5555,))
    server_thread.daemon = True
    server_thread.start()
    
    # Aguarda o servidor iniciar
    time.sleep(2)
    
    base_url = "http://localhost:5555"
    
    try:
        # Testa endpoint raiz
        print("\n1. Testando endpoint raiz...")
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
        
        # Testa endpoints de tickets
        print("\n2. Testando endpoints de tickets...")
        
        # Lista tickets
        response = requests.get(f"{base_url}/tickets")
        print(f"Lista de tickets - Status: {response.status_code}")
        
        # Testa endpoint de progresso de projeto (deve falhar pois não há tickets)
        response = requests.get(f"{base_url}/projects/TEST-001/progress")
        print(f"Progresso do projeto - Status: {response.status_code}")
        
        print("\nTestes concluídos com sucesso!")
        
    except Exception as e:
        print(f"Erro durante os testes: {e}")
    
    print("\nServidor de teste encerrado.")

if __name__ == "__main__":
    test_api_functionality()
