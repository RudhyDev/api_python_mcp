"""
Gerador de documentação OpenAPI/Swagger para a API.
"""
import json
from typing import Dict, Any


class SwaggerGenerator:
    """Gerador de documentação Swagger/OpenAPI."""

    def __init__(self, title: str = "API Python MCP", version: str = "1.0.0"):
        self.title = title
        self.version = version

    def generate_openapi_spec(self) -> Dict[str, Any]:
        """Gera a especificação OpenAPI completa."""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "description": "API REST em Python com integração GLPI seguindo Clean Architecture",
                "version": self.version,
                "contact": {
                    "name": "API Support",
                    "url": "https://github.com/seu-usuario/api-python-mcp",
                },
            },
            "servers": [
                {
                    "url": "https://web-production-d3940.up.railway.app",
                    "description": "Servidor de Produção",
                },
                {"url": "http://localhost:8000", "description": "Servidor Local"},
            ],
            "tags": [
                {
                    "name": "tickets",
                    "description": "Operações CRUD para tickets do GLPI",
                },
                {
                    "name": "projects",
                    "description": "Gerenciamento de projetos e progresso",
                },
                {"name": "health", "description": "Verificação de saúde da API"},
            ],
            "paths": self._generate_paths(),
            "components": {
                "schemas": self._generate_schemas(),
                "examples": self._generate_examples(),
            },
        }

    def _generate_paths(self) -> Dict[str, Any]:
        """Gera as definições dos endpoints."""
        return {
            "/": {
                "get": {
                    "tags": ["health"],
                    "summary": "Verificação de saúde da API",
                    "description": "Retorna informações básicas sobre a API",
                    "responses": {
                        "200": {
                            "description": "API funcionando corretamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HealthResponse"
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/tickets": {
                "get": {
                    "tags": ["tickets"],
                    "summary": "Lista todos os tickets",
                    "description": "Retorna uma lista de todos os tickets do GLPI",
                    "responses": {
                        "200": {
                            "description": "Lista de tickets retornada com sucesso",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/TicketSummary"
                                        },
                                    },
                                    "examples": {
                                        "tickets_list": {
                                            "$ref": "#/components/examples/TicketsList"
                                        }
                                    },
                                }
                            },
                        }
                    },
                },
                "post": {
                    "tags": ["tickets"],
                    "summary": "Cria um novo ticket",
                    "description": "Cria um novo ticket no GLPI",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TicketCreate"},
                                "examples": {
                                    "new_ticket": {
                                        "$ref": "#/components/examples/NewTicket"
                                    }
                                },
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Ticket criado com sucesso",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TicketResponse"
                                    }
                                }
                            },
                        },
                        "400": {
                            "description": "Dados de ticket inválidos",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ErrorResponse"
                                    }
                                }
                            },
                        },
                    },
                },
            },
            "/tickets/{id}": {
                "get": {
                    "tags": ["tickets"],
                    "summary": "Obtém um ticket específico",
                    "description": "Retorna os detalhes de um ticket pelo ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do ticket",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Ticket encontrado",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TicketDetail"
                                    }
                                }
                            },
                        },
                        "404": {"description": "Ticket não encontrado"},
                    },
                },
                "put": {
                    "tags": ["tickets"],
                    "summary": "Atualiza um ticket",
                    "description": "Atualiza os dados de um ticket existente",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do ticket",
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TicketUpdate"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Ticket atualizado com sucesso",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TicketResponse"
                                    }
                                }
                            },
                        },
                        "404": {"description": "Ticket não encontrado"},
                    },
                },
                "delete": {
                    "tags": ["tickets"],
                    "summary": "Deleta um ticket",
                    "description": "Remove um ticket do GLPI",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do ticket",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Ticket deletado com sucesso",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/DeleteResponse"
                                    }
                                }
                            },
                        },
                        "404": {"description": "Ticket não encontrado"},
                    },
                },
            },
            "/projects/{tag}/progress": {
                "get": {
                    "tags": ["projects"],
                    "summary": "Obtém progresso do projeto",
                    "description": "Calcula o progresso de um projeto baseado nos tickets relacionados",
                    "parameters": [
                        {
                            "name": "tag",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "Tag/identificador do projeto",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Progresso calculado com sucesso",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ProjectProgress"
                                    },
                                    "examples": {
                                        "project_progress": {
                                            "$ref": "#/components/examples/ProjectProgress"
                                        }
                                    },
                                }
                            },
                        }
                    },
                }
            },
        }

    def _generate_schemas(self) -> Dict[str, Any]:
        """Gera os schemas dos modelos."""
        return {
            "HealthResponse": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "API Python MCP - Clean Architecture com integração GLPI",
                    }
                },
            },
            "TicketSummary": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 123},
                    "name": {"type": "string", "example": "Problema no sistema"},
                    "status": {"type": "string", "example": "NEW"},
                    "priority": {"type": "string", "example": "MEDIUM"},
                },
            },
            "TicketDetail": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 123},
                    "name": {"type": "string", "example": "Problema no sistema"},
                    "content": {
                        "type": "string",
                        "example": "Descrição detalhada do problema",
                    },
                    "status": {"type": "string", "example": "NEW"},
                    "priority": {"type": "string", "example": "MEDIUM"},
                    "assigned_user_id": {"type": "integer", "nullable": True},
                    "assigned_group_id": {"type": "integer", "nullable": True},
                },
            },
            "TicketCreate": {
                "type": "object",
                "required": ["name", "content"],
                "properties": {
                    "name": {"type": "string", "example": "Novo problema identificado"},
                    "content": {"type": "string", "example": "Descrição do problema"},
                    "status": {
                        "type": "string",
                        "enum": [
                            "NEW",
                            "ASSIGNED",
                            "PLANNED",
                            "WAITING",
                            "SOLVED",
                            "CLOSED",
                        ],
                        "default": "NEW",
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "VERY_LOW",
                            "LOW",
                            "MEDIUM",
                            "HIGH",
                            "VERY_HIGH",
                            "MAJOR",
                        ],
                        "default": "MEDIUM",
                    },
                    "category_id": {"type": "integer", "nullable": True},
                    "assigned_user_id": {"type": "integer", "nullable": True},
                    "assigned_group_id": {"type": "integer", "nullable": True},
                },
            },
            "TicketUpdate": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "content": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": [
                            "NEW",
                            "ASSIGNED",
                            "PLANNED",
                            "WAITING",
                            "SOLVED",
                            "CLOSED",
                        ],
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "VERY_LOW",
                            "LOW",
                            "MEDIUM",
                            "HIGH",
                            "VERY_HIGH",
                            "MAJOR",
                        ],
                    },
                    "category_id": {"type": "integer", "nullable": True},
                    "assigned_user_id": {"type": "integer", "nullable": True},
                    "assigned_group_id": {"type": "integer", "nullable": True},
                },
            },
            "TicketResponse": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 123},
                    "name": {"type": "string", "example": "Problema no sistema"},
                    "status": {"type": "string", "example": "NEW"},
                    "priority": {"type": "string", "example": "MEDIUM"},
                },
            },
            "ProjectProgress": {
                "type": "object",
                "properties": {
                    "project_tag": {"type": "string", "example": "PROJ-001"},
                    "total_tickets": {"type": "integer", "example": 10},
                    "completed_tickets": {"type": "integer", "example": 3},
                    "in_progress_tickets": {"type": "integer", "example": 4},
                    "progress_percentage": {"type": "number", "example": 30.0},
                    "remaining_tickets": {"type": "integer", "example": 7},
                },
            },
            "DeleteResponse": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Ticket com ID 123 foi excluído",
                    }
                },
            },
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Dados de ticket inválidos"}
                },
            },
        }

    def _generate_examples(self) -> Dict[str, Any]:
        """Gera exemplos para a documentação."""
        return {
            "TicketsList": {
                "summary": "Lista de tickets",
                "value": [
                    {
                        "id": 1,
                        "name": "Problema de rede",
                        "status": "NEW",
                        "priority": "HIGH",
                    },
                    {
                        "id": 2,
                        "name": "Atualização sistema",
                        "status": "ASSIGNED",
                        "priority": "MEDIUM",
                    },
                ],
            },
            "NewTicket": {
                "summary": "Novo ticket",
                "value": {
                    "name": "Problema no servidor",
                    "content": "O servidor está apresentando lentidão",
                    "priority": "HIGH",
                    "category_id": 5,
                },
            },
            "ProjectProgress": {
                "summary": "Progresso do projeto",
                "value": {
                    "project_tag": "PROJ-001",
                    "total_tickets": 15,
                    "completed_tickets": 8,
                    "in_progress_tickets": 5,
                    "progress_percentage": 53.33,
                    "remaining_tickets": 7,
                },
            },
        }

    def get_json(self) -> str:
        """Retorna a especificação em formato JSON."""
        return json.dumps(self.generate_openapi_spec(), indent=2, ensure_ascii=False)

    def get_yaml(self) -> str:
        """Retorna a especificação em formato YAML."""
        try:
            import yaml
            return yaml.dump(
                self.generate_openapi_spec(), default_flow_style=False, allow_unicode=True
            )
        except ImportError:
            # Fallback para JSON se YAML não estiver disponível
            return self.get_json()
