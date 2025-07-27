"""
Casos de uso da aplicação.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .glpi_entities import GLPITicket


class TicketRepository(ABC):
    """Interface para o repositório de tickets."""

    @abstractmethod
    def get_all(self) -> List[GLPITicket]:
        """Obtém todos os tickets."""
        pass

    @abstractmethod
    def get_by_id(self, ticket_id: int) -> Optional[GLPITicket]:
        """Obtém um ticket pelo ID."""
        pass

    @abstractmethod
    def create(self, ticket: GLPITicket) -> Optional[GLPITicket]:
        """Cria um novo ticket."""
        pass

    @abstractmethod
    def update(self, ticket_id: int, ticket: GLPITicket) -> Optional[GLPITicket]:
        """Atualiza um ticket existente."""
        pass

    @abstractmethod
    def delete(self, ticket_id: int) -> bool:
        """Deleta um ticket."""
        pass

    @abstractmethod
    def search_by_project_tag(self, project_tag: str) -> List[GLPITicket]:
        """Busca tickets relacionados a um projeto."""
        pass
