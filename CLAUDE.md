# CLAUDE.md

Este arquivo fornece orientações para o Claude Code (claude.ai/code) ao trabalhar com código neste repositório.

## Visão Geral do Projeto

Uma API REST em Python com integração GLPI seguindo os princípios da Clean Architecture. A aplicação gerencia tickets de TI e projetos através da API do GLPI usando Python puro sem frameworks web externos.

## Comandos de Desenvolvimento

**Dependências e Instalação:**
```bash
poetry install        # Instala dependências
```

**Servidor:**
```bash
poetry run start      # Inicia servidor usando script Poetry
poetry run server     # Alternativa ao comando start
poetry run dev        # Alternativa para desenvolvimento
```

**Testes:**
```bash
poetry run pytest                                    # Executa todos os testes
poetry run pytest src/tests/                         # Executa testes específicos
poetry run pytest src/tests/test_glpi_use_cases.py   # Executa arquivo de teste específico
poetry run pytest -v                                 # Executa testes com output verboso
```

**Qualidade de Código:**
```bash
poetry run black src/      # Formata código com black
poetry run flake8 src/     # Verifica estilo do código com flake8
poetry run mypy src/       # Verificação de tipos com mypy
```

**Automação no VS Code:**
O projeto inclui configurações para automação completa no VS Code:
- **Format on Save**: Black executa automaticamente ao salvar
- **Lint on Save**: Flake8 e MyPy executam automaticamente
- **Import Organization**: Organiza imports automaticamente
- **Extensões recomendadas**: Instale as extensões sugeridas pelo VS Code

**Manutenção:**
```bash
find . -type f -name "*.pyc" -delete           # Remove arquivos Python compilados
find . -type d -name "__pycache__" -delete     # Remove diretórios __pycache__
```

## Arquitetura

O projeto segue Clean Architecture com três camadas principais:

**Camada Core (`src/core/`):**
- `glpi_entities.py`: Entidades de domínio (GLPITicket, GLPIProject, enums para status/prioridade)
- `glpi_use_cases.py`: Lógica de negócio para gerenciamento de tickets e acompanhamento de progresso de projetos
- `use_cases.py`: Interfaces abstratas para repositórios

**Camada Infrastructure (`src/infrastructure/`):**
- `glpi_client.py`: Cliente HTTP para API GLPI usando urllib (gerencia autenticação, sessão)
- `glpi_ticket_repository.py`: Implementação do repositório para operações CRUD de tickets

**Camada Interface (`src/interfaces/http/`):**
- `handler.py`: Handlers de requisições HTTP para endpoints REST
- `server.py`: Configuração do servidor e injeção de dependências

## Detalhes Importantes da Implementação

**Injeção de Dependências:** Usa padrão factory em `server.py:create_handler()` para injetar dependências das variáveis de ambiente no handler HTTP.

**Autenticação:** Cliente GLPI gerencia tokens de sessão automaticamente. Requer variáveis de ambiente `GLPI_BASE_URL`, `GLPI_APP_TOKEN` e `GLPI_USER_TOKEN`.

**Servidor HTTP:** Usa módulos nativos do Python `http.server` e `socketserver` - sem dependências de frameworks web externos.

**Tratamento de Erros:** Tratamento abrangente de erros no cliente GLPI com mensagens específicas para problemas de conexão e erros HTTP.

## Configuração

Variáveis de ambiente obrigatórias (copie de `.env.example`):
- `GLPI_BASE_URL`: Endpoint da API GLPI
- `GLPI_APP_TOKEN`: Token da aplicação do GLPI
- `GLPI_USER_TOKEN`: Token do usuário do GLPI  
- `SERVER_PORT`: Opcional, padrão 8000

## Endpoints da API

- `GET /` - Informações da API e links para documentação
- `GET /docs` - Documentação Swagger UI interativa
- `GET /api/openapi.json` - Especificação OpenAPI em JSON

### Tickets
- `GET /tickets` - Lista todos os tickets
- `GET /tickets/{id}` - Obtém ticket específico
- `POST /tickets` - Cria novo ticket
- `PUT /tickets/{id}` - Atualiza ticket
- `DELETE /tickets/{id}` - Deleta ticket

### Projetos
- `GET /projects/{tag}/progress` - Obtém progresso do projeto por tag

**📖 Documentação completa disponível em `/docs`**

## Deploy

### Railway.app

Para deploy no Railway:

1. **Conecte seu repositório GitHub/GitLab ao Railway**

2. **Configuração automática:**
   - Railway detecta automaticamente `pyproject.toml`
   - Usa o comando: `poetry run start` (definido no Procfile)
   - Porta configurada automaticamente via variável `PORT`

3. **Variáveis de ambiente obrigatórias no Railway:**
   ```bash
   GLPI_BASE_URL=https://seu-glpi-server.com/apirest.php
   GLPI_APP_TOKEN=seu_app_token_aqui
   GLPI_USER_TOKEN=seu_user_token_aqui
   ```

4. **Deploy automático:**
   - Push para branch main → Deploy automático
   - Logs disponíveis em tempo real no dashboard

### Outras plataformas

O projeto é compatível com qualquer plataforma que suporte Python 3.12+ e Poetry:
- Heroku: `poetry run start`
- Render: `poetry run start`
- Google Cloud Run: `poetry run start`