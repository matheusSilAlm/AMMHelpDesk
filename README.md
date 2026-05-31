# AMM HelpDesk

Sistema de suporte técnico desenvolvido com Django. Permite abertura de chamados por clientes, gerenciamento pela equipe de suporte e publicação de FAQ.

## Tecnologias

- **Backend**: Python 3.11 + Django 4.2
- **Banco de Dados**: PostgreSQL (produção) / SQLite (desenvolvimento local)
- **Frontend**: Tailwind CSS (CDN) + Alpine.js
- **Editor de Texto**: CKEditor 4.22
- **Containerização**: Docker + Docker Compose + Nginx
- **Segurança**: django-axes (rate limiting), HSTS, CSP headers

## Configuração local

1. Copie as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite .env com suas credenciais
   ```

2. Suba os containers:
   ```bash
   docker compose up --build
   ```

3. Acesse em `http://localhost`

## Rotas principais

| URL | Acesso | Descrição |
|-----|--------|----------|
| `/login/` | Público | Autenticação staff |
| `/formshd/` | Público | Abertura de chamado |
| `/FAQ/` | Público | Perguntas frequentes |
| `/home/` | Staff | Lista de chamados |
| `/home/pagecliente/` | Staff | Detalhe do chamado |

## Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements/development.txt

# Verificar formatação
black --check .
isort --check-only .
flake8 .

# Aplicar formatação
black .
isort .
```
