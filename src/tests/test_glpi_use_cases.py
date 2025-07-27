"""
Testes para os casos de uso do GLPI.
"""

from unittest.mock import Mock

import pytest

from src.core.glpi_entities import GLPITicket, TicketStatus
from src.core.glpi_use_cases import GLPITicketUseCase


class TestGLPITicketUseCase:
    """Testes para o caso de uso de tickets do GLPI."""

    @pytest.fixture
    def mock_ticket_repository(self):
        """Fixture para mock do repositório de tickets."""
        return Mock()

    @pytest.fixture
    def ticket_use_case(self, mock_ticket_repository):
        """Fixture para instância do caso de uso."""
        return GLPITicketUseCase(mock_ticket_repository)

    def test_list_tickets(self, ticket_use_case, mock_ticket_repository):
        """Testa listagem de tickets."""
        # Arrange
        tickets = [
            GLPITicket(name="Ticket 1", content="Content 1"),
            GLPITicket(name="Ticket 2", content="Content 2"),
        ]
        mock_ticket_repository.get_all.return_value = tickets

        # Act
        result = ticket_use_case.list_tickets()

        # Assert
        assert result == tickets
        mock_ticket_repository.get_all.assert_called_once()

    def test_get_ticket(self, ticket_use_case, mock_ticket_repository):
        """Testa obtenção de ticket por ID."""
        # Arrange
        ticket = GLPITicket(name="Test Ticket", content="Test Content")
        mock_ticket_repository.get_by_id.return_value = ticket

        # Act
        result = ticket_use_case.get_ticket(1)

        # Assert
        assert result == ticket
        mock_ticket_repository.get_by_id.assert_called_once_with(1)

    def test_create_ticket_valid(self, ticket_use_case, mock_ticket_repository):
        """Testa criação de ticket válido."""
        # Arrange
        ticket = GLPITicket(name="New Ticket", content="New Content")
        created_ticket = GLPITicket(id=1, name="New Ticket", content="New Content")
        mock_ticket_repository.create.return_value = created_ticket

        # Act
        result = ticket_use_case.create_ticket(ticket)

        # Assert
        assert result == created_ticket
        mock_ticket_repository.create.assert_called_once_with(ticket)

    def test_create_ticket_invalid(self, ticket_use_case, mock_ticket_repository):
        """Testa criação de ticket inválido."""
        # Arrange
        ticket = GLPITicket(name="", content="")  # Ticket inválido
        mock_ticket_repository.create.return_value = None

        # Act
        result = ticket_use_case.create_ticket(ticket)

        # Assert
        assert result is None
        mock_ticket_repository.create.assert_not_called()

    def test_update_ticket_valid(self, ticket_use_case, mock_ticket_repository):
        """Testa atualização de ticket válido."""
        # Arrange
        ticket = GLPITicket(name="Updated Ticket", content="Updated Content")
        updated_ticket = GLPITicket(
            id=1, name="Updated Ticket", content="Updated Content"
        )
        mock_ticket_repository.update.return_value = updated_ticket

        # Act
        result = ticket_use_case.update_ticket(1, ticket)

        # Assert
        assert result == updated_ticket
        mock_ticket_repository.update.assert_called_once_with(1, ticket)

    def test_update_ticket_invalid(self, ticket_use_case, mock_ticket_repository):
        """Testa atualização de ticket inválido."""
        # Arrange
        ticket = GLPITicket(name="", content="")  # Ticket inválido
        mock_ticket_repository.update.return_value = None

        # Act
        result = ticket_use_case.update_ticket(1, ticket)

        # Assert
        assert result is None
        mock_ticket_repository.update.assert_not_called()

    def test_delete_ticket(self, ticket_use_case, mock_ticket_repository):
        """Testa exclusão de ticket."""
        # Arrange
        mock_ticket_repository.delete.return_value = True

        # Act
        result = ticket_use_case.delete_ticket(1)

        # Assert
        assert result is True
        mock_ticket_repository.delete.assert_called_once_with(1)

    def test_search_project_tickets(self, ticket_use_case, mock_ticket_repository):
        """Testa busca de tickets por tag de projeto."""
        # Arrange
        tickets = [
            GLPITicket(name="Ticket 1", content="Content 1"),
            GLPITicket(name="Ticket 2", content="Content 2"),
        ]
        mock_ticket_repository.search_by_project_tag.return_value = tickets

        # Act
        result = ticket_use_case.search_project_tickets("PROJECT-123")

        # Assert
        assert result == tickets
        mock_ticket_repository.search_by_project_tag.assert_called_once_with(
            "PROJECT-123"
        )

    def test_get_project_progress(self, ticket_use_case, mock_ticket_repository):
        """Testa cálculo de progresso do projeto."""
        # Arrange
        tickets = [
            GLPITicket(name="Ticket 1", content="Content 1", status=TicketStatus.NEW),
            GLPITicket(
                name="Ticket 2", content="Content 2", status=TicketStatus.ASSIGNED
            ),
            GLPITicket(
                name="Ticket 3", content="Content 3", status=TicketStatus.SOLVED
            ),
            GLPITicket(
                name="Ticket 4", content="Content 4", status=TicketStatus.CLOSED
            ),
        ]
        mock_ticket_repository.search_by_project_tag.return_value = tickets

        # Act
        result = ticket_use_case.get_project_progress("PROJECT-123")

        # Assert
        assert result["project_tag"] == "PROJECT-123"
        assert result["total_tickets"] == 4
        assert result["completed_tickets"] == 2
        assert result["in_progress_tickets"] == 1
        assert result["progress_percentage"] == 50.0
        assert result["remaining_tickets"] == 2

    def test_create_project_milestone(self, ticket_use_case, mock_ticket_repository):
        """Testa criação de marco do projeto."""
        # Arrange
        created_ticket = GLPITicket(
            id=1, name="📍 MILESTONE: Release 1.0", content="Release description"
        )
        mock_ticket_repository.create.return_value = created_ticket

        # Act
        result = ticket_use_case.create_project_milestone(
            "Release 1.0", "Release description", "2023-12-31"
        )

        # Assert
        assert result == created_ticket
        mock_ticket_repository.create.assert_called_once()

    def test_update_ticket_status(self, ticket_use_case, mock_ticket_repository):
        """Testa atualização de status de ticket."""
        # Arrange
        ticket = GLPITicket(
            id=1, name="Test Ticket", content="Test Content", status=TicketStatus.NEW
        )
        updated_ticket = GLPITicket(
            id=1,
            name="Test Ticket",
            content="Test Content",
            status=TicketStatus.ASSIGNED,
        )
        mock_ticket_repository.get_by_id.return_value = ticket
        mock_ticket_repository.update.return_value = updated_ticket

        # Act
        result = ticket_use_case.update_ticket_status(1, TicketStatus.ASSIGNED)

        # Assert
        assert result is True
        mock_ticket_repository.get_by_id.assert_called_once_with(1)
        mock_ticket_repository.update.assert_called_once()
