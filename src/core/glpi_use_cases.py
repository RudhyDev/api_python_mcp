"""
Casos de uso para gerenciamento de tickets do GLPI.
"""
from typing import List, Optional
from .glpi_entities import GLPITicket, TicketStatus, TicketPriority
from .use_cases import TicketRepository


class GLPITicketUseCase:
    """Caso de uso para gerenciamento de tickets do GLPI."""

    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository

    def list_tickets(self) -> List[GLPITicket]:
        """Lista todos os tickets."""
        return self.ticket_repository.get_all()

    def get_ticket(self, ticket_id: int) -> Optional[GLPITicket]:
        """Obtém um ticket pelo ID."""
        return self.ticket_repository.get_by_id(ticket_id)

    def create_ticket(self, ticket: GLPITicket) -> Optional[GLPITicket]:
        """Cria um novo ticket."""
        if not ticket.is_valid():
            return None
        return self.ticket_repository.create(ticket)

    def update_ticket(self, ticket_id: int, ticket: GLPITicket) -> Optional[GLPITicket]:
        """Atualiza um ticket existente."""
        if not ticket.is_valid():
            return None
        return self.ticket_repository.update(ticket_id, ticket)

    def delete_ticket(self, ticket_id: int) -> bool:
        """Deleta um ticket."""
        return self.ticket_repository.delete(ticket_id)

    def search_project_tickets(self, project_tag: str) -> List[GLPITicket]:
        """Busca tickets relacionados a um projeto."""
        return self.ticket_repository.search_by_project_tag(project_tag)

    def get_project_progress(self, project_tag: str) -> dict:
        """Calcula progresso de um projeto baseado nos tickets."""
        tickets = self.search_project_tickets(project_tag)

        total_tickets = len(tickets)
        completed_tickets = sum(
            1
            for ticket in tickets
            if ticket.status == TicketStatus.SOLVED
            or ticket.status == TicketStatus.CLOSED
        )
        in_progress_tickets = sum(
            1
            for ticket in tickets
            if ticket.status == TicketStatus.ASSIGNED
            or ticket.status == TicketStatus.PLANNED
        )

        progress_percentage = (
            (completed_tickets / total_tickets * 100) if total_tickets > 0 else 0
        )

        return {
            "project_tag": project_tag,
            "total_tickets": total_tickets,
            "completed_tickets": completed_tickets,
            "in_progress_tickets": in_progress_tickets,
            "progress_percentage": round(progress_percentage, 2),
            "remaining_tickets": total_tickets - completed_tickets,
        }

    def create_project_milestone(
        self, name: str, description: str, due_date
    ) -> Optional[GLPITicket]:
        """Cria um marco do projeto como ticket."""
        milestone_ticket = GLPITicket(
            name=f"📍 MILESTONE: {name}",
            content=description,
            priority=TicketPriority.HIGH,
            due_date=due_date,
        )

        return self.create_ticket(milestone_ticket)

    def update_ticket_status(self, ticket_id: int, status: TicketStatus) -> bool:
        """Atualiza status de um ticket."""
        ticket = self.get_ticket(ticket_id)
        if ticket:
            ticket.status = status
            updated_ticket = self.update_ticket(ticket_id, ticket)
            return updated_ticket is not None
        return False
