"""
Script para testar a criação de tickets diretamente com o repositório.
"""
import os
import sys

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.glpi_entities import GLPITicket, TicketStatus, TicketPriority
from src.infrastructure.glpi_client import GLPIHTTPClient
from src.infrastructure.glpi_ticket_repository import GLPITicketRepository
from src.core.glpi_entities import GLPIConfig


def test_ticket_creation():
    """Testa a criação de um ticket."""
    # Configuração do GLPI (valores de exemplo)
    glpi_config = GLPIConfig(
        base_url=os.getenv('GLPI_BASE_URL', 'http://localhost/glpi/apirest.php'),
        app_token=os.getenv('GLPI_APP_TOKEN', ''),
        user_token=os.getenv('GLPI_USER_TOKEN', ''),
        timeout=30
    )
    
    # Cria o cliente e repositório
    glpi_client = GLPIHTTPClient(glpi_config)
    ticket_repository = GLPITicketRepository(glpi_client)
    
    # Cria um ticket de teste
    ticket = GLPITicket(
        name="Teste de Ticket Direto",
        content="Este é um ticket de teste criado diretamente",
        status=TicketStatus.NEW,
        priority=TicketPriority.MEDIUM
    )
    
    print("Tentando criar ticket...")
    print(f"Ticket válido: {ticket.is_valid()}")
    print(f"Nome: {ticket.name}")
    print(f"Conteúdo: {ticket.content}")
    
    # Tenta criar o ticket
    created_ticket = ticket_repository.create(ticket)
    
    if created_ticket:
        print(f"Ticket criado com sucesso! ID: {created_ticket.id}")
    else:
        print("Falha ao criar ticket")
        
        # Verifica se há erro de autenticação
        try:
            response = glpi_client.make_request('GET', '/getFullSession')
            print(f"Status da sessão: {response.status_code}")
            print(f"Dados da sessão: {response.data}")
        except Exception as e:
            print(f"Erro ao verificar sessão: {e}")

if __name__ == "__main__":
    test_ticket_creation()
