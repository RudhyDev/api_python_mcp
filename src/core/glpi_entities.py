"""
Entidades do GLPI para gerenciamento de projetos de TI.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class TicketStatus(Enum):
    """Status dos tickets no GLPI."""

    NEW = 1
    ASSIGNED = 2
    PLANNED = 3
    WAITING = 4
    SOLVED = 5
    CLOSED = 6


class TicketPriority(Enum):
    """Prioridades dos tickets no GLPI."""

    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5
    MAJOR = 6


@dataclass
class GLPITicket:
    """Representa um ticket do GLPI."""

    id: Optional[int] = None
    name: str = ""
    content: str = ""
    status: TicketStatus = TicketStatus.NEW
    priority: TicketPriority = TicketPriority.MEDIUM
    category_id: Optional[int] = None
    assigned_user_id: Optional[int] = None
    assigned_group_id: Optional[int] = None
    due_date: Optional[datetime] = None
    created_date: Optional[datetime] = None
    time_to_resolve: Optional[datetime] = None

    def is_valid(self) -> bool:
        """Verifica se o ticket tem dados válidos."""
        return bool(self.name and self.content)


@dataclass
class GLPIProject:
    """Representa um projeto de TI no GLPI."""

    id: Optional[int] = None
    name: str = ""
    description: str = ""
    manager_id: Optional[int] = None
    team_members: Optional[List[int]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tickets: Optional[List[GLPITicket]] = None

    def __post_init__(self):
        if self.team_members is None:
            self.team_members = []
        if self.tickets is None:
            self.tickets = []

    def is_valid(self) -> bool:
        """Verifica se o projeto tem dados válidos."""
        return bool(self.name and self.description)


@dataclass
class GLPIConfig:
    """Configuração para conexão com a API do GLPI."""

    base_url: str
    app_token: str
    user_token: str
    timeout: int = 30


@dataclass
class GLPIResponse:
    """Representa uma resposta da API do GLPI."""

    status_code: int
    data: Dict[str, Any]
    error: Optional[str] = None

    def is_success(self) -> bool:
        """Verifica se a requisição foi bem sucedida."""
        return 200 <= self.status_code < 300
