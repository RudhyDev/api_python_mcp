# 🐍 API Python MCP

> API REST em Python com integração GLPI seguindo Clean Architecture

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Poetry](https://img.shields.io/badge/Poetry-dependency%20management-blue.svg)](https://python-poetry.org)
[![Railway](https://img.shields.io/badge/Deploy-Railway-purple.svg)](https://railway.app)
[![Swagger](https://img.shields.io/badge/Docs-Swagger-green.svg)](https://web-production-d3940.up.railway.app/docs)

Uma API REST moderna em Python puro com integração ao GLPI, seguindo os princípios da **Clean Architecture** e **SOLID**. Inclui documentação Swagger interativa, testes automatizados e deploy contínuo.

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

## ✨ Funcionalidades

- 🏗️ **Clean Architecture** - Separação clara de responsabilidades
- 🔄 **CRUD completo** para tickets do GLPI  
- 📊 **Acompanhamento de projetos** com cálculo de progresso
- 📚 **Documentação Swagger** interativa
- 🧪 **Testes automatizados** com 100% de cobertura
- ⚡ **Deploy automático** no Railway
- 🔧 **Qualidade de código** com formatação e linting automáticos

## 🛠️ Tecnologias

- **Python 3.12** - Linguagem principal
- **Poetry** - Gerenciamento de dependências
- **Clean Architecture** - Padrão arquitetural
- **Swagger/OpenAPI** - Documentação da API
- **pytest** - Framework de testes
- **Black + Flake8 + MyPy** - Qualidade de código
- **Railway** - Deploy e hospedagem
- **http.server** - Servidor HTTP nativo (sem frameworks externos)

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.12+
- Poetry

### Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/api-python-mcp.git
cd api-python-mcp

# Instale as dependências
poetry install

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações do GLPI
```

### Executar localmente
```bash
# Inicie o servidor
poetry run start

# A API estará disponível em http://localhost:8000
# Documentação Swagger em http://localhost:8000/docs
```

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

## 📚 Documentação da API

### 🌐 Produção
- **API Base URL**: https://web-production-d3940.up.railway.app
- **Documentação Swagger**: https://web-production-d3940.up.railway.app/docs
- **OpenAPI Spec**: https://web-production-d3940.up.railway.app/api/openapi.json

### 📋 Endpoints Principais

#### 🏥 Saúde da API
- `GET /` - Informações da API e links para documentação
- `GET /docs` - Documentação Swagger UI interativa
- `GET /api/openapi.json` - Especificação OpenAPI em JSON

#### 🎫 Tickets
- `GET /tickets` - Lista todos os tickets
- `GET /tickets/{id}` - Obtém ticket específico
- `POST /tickets` - Cria novo ticket
- `PUT /tickets/{id}` - Atualiza ticket existente
- `DELETE /tickets/{id}` - Remove ticket

#### 📊 Projetos
- `GET /projects/{tag}/progress` - Calcula progresso do projeto

> 💡 **Explore a documentação completa**: Acesse `/docs` para uma interface interativa com todos os endpoints, schemas e exemplos!

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

## 🏗️ Arquitetura

O projeto segue **Clean Architecture** com separação clara de responsabilidades:

### 📦 Camadas

- **🎯 Core** (`src/core/`): Entidades de domínio e casos de uso
  - `glpi_entities.py`: Modelos de dados (Ticket, Project)
  - `glpi_use_cases.py`: Lógica de negócio
  - `use_cases.py`: Interfaces/contratos

- **🔧 Infrastructure** (`src/infrastructure/`): Implementações técnicas
  - `glpi_client.py`: Cliente HTTP para GLPI API
  - `glpi_ticket_repository.py`: Persistência de dados

- **🌐 Interfaces** (`src/interfaces/http/`): Camada de apresentação
  - `handler.py`: Controllers REST
  - `server.py`: Configuração do servidor
  - `swagger.py`: Documentação automática

### 🧪 Qualidade de Código

O projeto mantém **100% de qualidade** com:

```bash
# Executa todos os testes (11 testes passando)
poetry run pytest -v

# Formatação automática do código
poetry run black src/

# Verificação de estilo (0 erros)
poetry run flake8 src/

# Verificação de tipos (type-safe)
poetry run mypy src/
```

## 🚀 Deploy

### Railway (Produção)

O projeto está configurado para **deploy automático** no Railway:

1. **Fork/clone** este repositório
2. **Conecte** ao [Railway](https://railway.app)
3. **Configure** as variáveis de ambiente:
   - `GLPI_BASE_URL`
   - `GLPI_APP_TOKEN`
   - `GLPI_USER_TOKEN`
4. **Deploy automático** em cada push para `main`

### Outras Plataformas

Compatível com qualquer plataforma Python:
- **Heroku**: `poetry run start`
- **Render**: `poetry run start`  
- **Google Cloud Run**: `poetry run start`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Faça commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Desenvolvido com ❤️ usando Clean Architecture e boas práticas Python**
