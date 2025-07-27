"""
Handlers HTTP para a API.
"""
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler
from src.core.glpi_use_cases import GLPITicketUseCase


class APIHandler(BaseHTTPRequestHandler):
    """Handler principal para a API."""

    def __init__(self, ticket_use_case: GLPITicketUseCase, *args, **kwargs):
        self.ticket_use_case = ticket_use_case
        super().__init__(*args, **kwargs)

    def set_headers(self, content_type="application/json"):
        """Configura os cabeçalhos da resposta."""
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        """Tratamento para requisições OPTIONS (preflight CORS)."""
        self.set_headers()

    def do_GET(self):
        """Tratamento para requisições GET."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        # query_params = urllib.parse.parse_qs(parsed_path.query)  # Não usado

        if path == "/tickets":
            tickets = self.ticket_use_case.list_tickets()
            self.set_headers()
            self.wfile.write(
                json.dumps(
                    [
                        {
                            "id": ticket.id,
                            "name": ticket.name,
                            "status": ticket.status.name,
                            "priority": ticket.priority.name,
                        }
                        for ticket in tickets
                    ]
                ).encode()
            )

        elif path.startswith("/tickets/"):
            try:
                ticket_id = int(path.split("/")[-1])
                ticket = self.ticket_use_case.get_ticket(ticket_id)
                if ticket:
                    self.set_headers()
                    self.wfile.write(
                        json.dumps(
                            {
                                "id": ticket.id,
                                "name": ticket.name,
                                "content": ticket.content,
                                "status": ticket.status.name,
                                "priority": ticket.priority.name,
                                "assigned_user_id": ticket.assigned_user_id,
                                "assigned_group_id": ticket.assigned_group_id,
                            }
                        ).encode()
                    )
                else:
                    self.send_error(404, "Ticket não encontrado")
            except (ValueError, IndexError):
                self.send_error(400, "ID inválido")

        elif path.startswith("/projects/") and path.endswith("/progress"):
            try:
                project_tag = path.split("/")[2]
                progress = self.ticket_use_case.get_project_progress(project_tag)
                self.set_headers()
                self.wfile.write(json.dumps(progress).encode())
            except Exception as e:
                self.send_error(500, f"Erro ao calcular progresso: {str(e)}")

        elif path == "/":
            self.set_headers()
            response = {
                "message": "API Python MCP - Clean Architecture com integração GLPI"
            }
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_error(404, "Endpoint não encontrado")

    def do_POST(self):
        """Tratamento para requisições POST."""
        if self.path == "/tickets":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                ticket_data = json.loads(post_data.decode())

                # Importações locais para evitar dependências circulares
                from src.core.glpi_entities import (
                    GLPITicket,
                    TicketStatus,
                    TicketPriority,
                )

                ticket = GLPITicket(
                    name=ticket_data.get("name", ""),
                    content=ticket_data.get("content", ""),
                    status=TicketStatus[ticket_data.get("status", "NEW")]
                    if ticket_data.get("status")
                    else TicketStatus.NEW,
                    priority=TicketPriority[ticket_data.get("priority", "MEDIUM")]
                    if ticket_data.get("priority")
                    else TicketPriority.MEDIUM,
                    category_id=ticket_data.get("category_id"),
                    assigned_user_id=ticket_data.get("assigned_user_id"),
                    assigned_group_id=ticket_data.get("assigned_group_id"),
                )

                created_ticket = self.ticket_use_case.create_ticket(ticket)
                if created_ticket and created_ticket.id:
                    self.set_headers()
                    self.wfile.write(
                        json.dumps(
                            {
                                "id": created_ticket.id,
                                "name": created_ticket.name,
                                "status": created_ticket.status.name,
                                "priority": created_ticket.priority.name,
                            }
                        ).encode()
                    )
                else:
                    self.send_error(400, "Dados de ticket inválidos")
            except json.JSONDecodeError:
                self.send_error(400, "JSON inválido")
            except Exception as e:
                self.send_error(500, f"Erro ao criar ticket: {str(e)}")
        else:
            self.send_error(404, "Endpoint não encontrado")

    def do_PUT(self):
        """Tratamento para requisições PUT."""
        if self.path.startswith("/tickets/"):
            try:
                ticket_id = int(self.path.split("/")[-1])
                content_length = int(self.headers["Content-Length"])
                put_data = self.rfile.read(content_length)
                ticket_data = json.loads(put_data.decode())

                # Importações locais para evitar dependências circulares
                from src.core.glpi_entities import TicketStatus, TicketPriority

                # Criar um ticket parcial com os dados fornecidos
                from src.core.glpi_entities import GLPITicket

                ticket = GLPITicket(
                    name=ticket_data.get("name", ""),
                    content=ticket_data.get("content", ""),
                    status=TicketStatus[ticket_data.get("status", "NEW")]
                    if ticket_data.get("status")
                    else TicketStatus.NEW,
                    priority=TicketPriority[ticket_data.get("priority", "MEDIUM")]
                    if ticket_data.get("priority")
                    else TicketPriority.MEDIUM,
                    category_id=ticket_data.get("category_id"),
                    assigned_user_id=ticket_data.get("assigned_user_id"),
                    assigned_group_id=ticket_data.get("assigned_group_id"),
                )

                updated_ticket = self.ticket_use_case.update_ticket(ticket_id, ticket)
                if updated_ticket:
                    self.set_headers()
                    self.wfile.write(
                        json.dumps(
                            {
                                "id": updated_ticket.id,
                                "name": updated_ticket.name,
                                "status": updated_ticket.status.name,
                                "priority": updated_ticket.priority.name,
                            }
                        ).encode()
                    )
                else:
                    self.send_error(404, "Ticket não encontrado ou dados inválidos")
            except (ValueError, IndexError):
                self.send_error(400, "ID inválido")
            except json.JSONDecodeError:
                self.send_error(400, "JSON inválido")
            except Exception as e:
                self.send_error(500, f"Erro ao atualizar ticket: {str(e)}")
        else:
            self.send_error(404, "Endpoint não encontrado")

    def do_DELETE(self):
        """Tratamento para requisições DELETE."""
        if self.path.startswith("/tickets/"):
            try:
                ticket_id = int(self.path.split("/")[-1])
                if self.ticket_use_case.delete_ticket(ticket_id):
                    self.set_headers()
                    response = {"message": f"Ticket com ID {ticket_id} foi excluído"}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_error(404, "Ticket não encontrado")
            except (ValueError, IndexError):
                self.send_error(400, "ID inválido")
        else:
            self.send_error(404, "Endpoint não encontrado")
