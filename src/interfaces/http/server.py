"""
Servidor HTTP principal.
"""
import socketserver
import os
from functools import partial
from src.core.glpi_use_cases import GLPITicketUseCase
from src.infrastructure.glpi_client import GLPIHTTPClient
from src.infrastructure.glpi_ticket_repository import GLPITicketRepository
from src.interfaces.http.handler import APIHandler
from src.core.glpi_entities import GLPIConfig


def create_handler(*args, **kwargs):
    """Factory para criar o handler com as dependências injetadas."""
    # Inicializa as dependências do GLPI a partir das variáveis de ambiente
    glpi_config = GLPIConfig(
        base_url=os.getenv("GLPI_BASE_URL", "http://localhost/glpi/apirest.php"),
        app_token=os.getenv("GLPI_APP_TOKEN", ""),
        user_token=os.getenv("GLPI_USER_TOKEN", ""),
        timeout=30,
    )
    glpi_client = GLPIHTTPClient(glpi_config)
    ticket_repository = GLPITicketRepository(glpi_client)
    ticket_use_case = GLPITicketUseCase(ticket_repository)

    # Cria o handler com as dependências
    return APIHandler(ticket_use_case, *args, **kwargs)


def run_server(port=None):
    """Executa o servidor HTTP."""
    if port is None:
        # Railway usa PORT, outros podem usar SERVER_PORT
        port = int(os.getenv("PORT", os.getenv("SERVER_PORT", 8000)))

    handler = partial(create_handler)

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Servidor rodando em http://localhost:{port}")
        print("Pressione Ctrl+C para parar o servidor")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado")
            httpd.server_close()


if __name__ == "__main__":
    run_server()
