# API Python MCP

API REST em Python puro com integração ao GLPI, seguindo os princípios do SOLID e da Clean Architecture.

## Estrutura do Projeto

```
api_python_mcp/
├── src/
│   ├── core/              # Camada de domínio (entidades, casos de uso)
│   ├── infrastructure/     # Camada de infraestrutura (repositórios, clientes HTTP)
│   ├── interfaces/         # Camada de interfaces (handlers HTTP)
│   └── tests/             # Testes unitários
├── run_server.py          # Script para iniciar o servidor
├── pyproject.toml         # Configuração do Poetry
├── pytest.ini             # Configuração do pytest
├── .env.example           # Exemplo de variáveis de ambiente
└── README.md              # Documentação
```

## Tecnologias

- Python 3.12
- Poetry (gerenciamento de dependências)
- http.server (servidor HTTP embutido)
- Testes com pytest
- Formatação com black
- Linting com flake8
- Type checking com mypy

## Instalação

1. Certifique-se de ter o Python 3.12 e o Poetry instalados
2. Clone o repositório
3. Execute `poetry install` para instalar as dependências

## Configuração

Crie um arquivo `.env` com as configurações do GLPI:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com as suas configurações:

- `GLPI_BASE_URL`: URL da API REST do GLPI (ex: https://seu-glpi.example.com/apirest.php)
- `GLPI_APP_TOKEN`: Token da aplicação GLPI (obtido nas configurações do GLPI)
- `GLPI_USER_TOKEN`: Token do usuário GLPI (obtido no perfil do usuário)
- `SERVER_PORT`: Porta do servidor (opcional, padrão 8000)

### Configuração do GLPI

Para usar a integração com o GLPI, você precisa:

1. Ter acesso a uma instância do GLPI com a API REST habilitada
2. Criar um token de aplicação nas configurações do GLPI
3. Criar um token de usuário no perfil do usuário
4. Configurar as permissões adequadas para os tokens

Se você não tiver acesso a um GLPI, pode usar uma instância de teste ou desenvolvimento. Para isso, consulte a documentação oficial do GLPI sobre como configurar a API REST.

## Uso

### Iniciar o servidor

```bash
# Iniciar o servidor
poetry run start

# Alternativas
poetry run server
poetry run dev
```

O servidor estará disponível em `http://localhost:8000`

### Endpoints

- `GET /` - Mensagem de boas-vindas

### Tickets do GLPI

- `GET /tickets` - Lista todos os tickets
- `GET /tickets/{id}` - Obtém um ticket específico
- `POST /tickets` - Cria um novo ticket
- `PUT /tickets/{id}` - Atualiza um ticket existente
- `DELETE /tickets/{id}` - Deleta um ticket
- `GET /projects/{tag}/progress` - Obtém o progresso de um projeto (baseado em tickets com uma tag específica)

### Testes

```bash
poetry run pytest          # Executa todos os testes
poetry run pytest -v       # Testes com output verboso
```

### Formatação de código

```bash
poetry run black src/
```

### Verificação de estilo

```bash
poetry run flake8 src/
```

### Verificação de tipos

```bash
poetry run mypy src/
```

### Limpeza

```bash
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete
```

## Desenvolvimento

O projeto segue os princípios da Clean Architecture:

- **Camada core**: Contém as entidades e casos de uso
- **Camada infrastructure**: Implementa os repositórios e clientes HTTP
- **Camada interfaces**: Define os handlers HTTP

Todos os comandos são executados através do Poetry.
