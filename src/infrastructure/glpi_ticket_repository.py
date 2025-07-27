"""
Repositório para gerenciar tickets do GLPI.
"""
import urllib.parse
from typing import List, Optional, Dict, Any
from src.core.glpi_entities import GLPITicket, TicketStatus, TicketPriority
from src.core.use_cases import TicketRepository
from src.infrastructure.glpi_client import GLPIHTTPClient


class GLPITicketRepository(TicketRepository):
    """Implementação do repositório de tickets usando a API do GLPI."""

    def __init__(self, glpi_client: GLPIHTTPClient):
        self.client = glpi_client

    def get_all(self) -> List[GLPITicket]:
        """Obtém todos os tickets."""
        # Busca os últimos 50 tickets (limitado para evitar sobrecarga)
        response = self.client.make_request("GET", "/search/Ticket?range=0-49")

        if response.is_success():
            tickets_data = response.data.get("data", [])
            tickets = []

            for ticket_data in tickets_data:
                ticket = self._parse_ticket_data(ticket_data)
                if ticket:
                    tickets.append(ticket)

            return tickets

        return []

    def get_by_id(self, ticket_id: int) -> Optional[GLPITicket]:
        """Obtém um ticket pelo ID."""
        response = self.client.make_request("GET", f"/Ticket/{ticket_id}")

        if response.is_success() and response.data:
            return self._parse_ticket_data(response.data)

        return None

    def create(self, ticket: GLPITicket) -> Optional[GLPITicket]:
        """Cria um novo ticket."""
        if not ticket.is_valid():
            return None

        payload = {
            "input": {
                "name": ticket.name,
                "content": ticket.content,
                "status": ticket.status.value,
                "priority": ticket.priority.value,
                "itilcategories_id": ticket.category_id,
                "users_id_tech": ticket.assigned_user_id,
                "groups_id_tech": ticket.assigned_group_id,
            }
        }

        if ticket.due_date:
            payload["input"]["time_to_resolve"] = ticket.due_date.isoformat()

        response = self.client.make_request("POST", "/Ticket", payload)

        if response.is_success() and "id" in response.data:
            ticket.id = response.data["id"]
            return ticket

        return None

    def update(self, ticket_id: int, ticket: GLPITicket) -> Optional[GLPITicket]:
        """Atualiza um ticket existente."""
        if not ticket.is_valid():
            return None

        payload = {
            "input": {
                "id": ticket_id,
                "name": ticket.name,
                "content": ticket.content,
                "status": ticket.status.value,
                "priority": ticket.priority.value,
                "itilcategories_id": ticket.category_id,
                "users_id_tech": ticket.assigned_user_id,
                "groups_id_tech": ticket.assigned_group_id,
            }
        }

        if ticket.due_date:
            payload["input"]["time_to_resolve"] = ticket.due_date.isoformat()

        response = self.client.make_request("PUT", f"/Ticket/{ticket_id}", payload)

        if response.is_success():
            ticket.id = ticket_id
            return ticket

        return None

    def delete(self, ticket_id: int) -> bool:
        """Deleta um ticket."""
        response = self.client.make_request("DELETE", f"/Ticket/{ticket_id}")
        return response.is_success()

    def search_by_project_tag(self, project_tag: str) -> List[GLPITicket]:
        """Busca tickets relacionados a um projeto."""
        # Esta é uma implementação simplificada
        # Na prática, você pode querer usar critérios de busca mais complexos
        search_query = urllib.parse.quote(f"%{project_tag}%")
        endpoint = (
            f"/search/Ticket?criteria[0][field]=1&criteria[0][searchtype]=contains"
            f"&criteria[0][value]={search_query}"
        )

        response = self.client.make_request("GET", endpoint)

        if response.is_success():
            tickets_data = response.data.get("data", [])
            tickets = []

            for ticket_data in tickets_data:
                ticket = self._parse_ticket_data(ticket_data)
                if ticket:
                    tickets.append(ticket)

            return tickets

        return []

    def _parse_ticket_data(self, ticket_data: Dict[str, Any]) -> Optional[GLPITicket]:
        """Converte dados do ticket do GLPI para objeto GLPITicket."""
        try:
            # Mapeamento de campos do GLPI (os números são os IDs dos campos no GLPI)
            ticket = GLPITicket(
                id=ticket_data.get("id"),
                name=ticket_data.get("1", ""),  # Nome do ticket
                content=ticket_data.get("2", ""),  # Conteúdo do ticket
                status=TicketStatus(int(ticket_data.get("12", 1))),  # Status
                priority=TicketPriority(int(ticket_data.get("3", 3))),  # Prioridade
                category_id=ticket_data.get("7"),  # Categoria
                assigned_user_id=ticket_data.get("5"),  # Usuário atribuído
                assigned_group_id=ticket_data.get("8"),  # Grupo atribuído
            )

            return ticket
        except Exception as e:
            print(f"Erro ao parsear ticket: {e}")
            return None
