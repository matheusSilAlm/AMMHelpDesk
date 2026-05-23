# Plano de Implementação — Refatoração e Reestruturação (Fase 1)

Este plano descreve as alterações para reestruturar o projeto **AMMHelpDesk**, movendo os arquivos da pasta interna `AmmHelpDesk` para a raiz do repositório, configurando variáveis de ambiente seguras com `.env` (ocultando credenciais atuais) e preparando a base para o Docker.

---

## 📌 Análise e Decisão de Estrutura (PS do Usuário)

Atualmente, o projeto Django está aninhado dentro de um subdiretório `AmmHelpDesk/`, resultando em caminhos confusos como `AMMHelpDesk/AmmHelpDesk/AmmHelpDesk/settings.py`. 

### Proposta de Estrutura Simplificada (Sem Aninhamento Excessivo)
Para manter as melhores práticas e simplificar o uso do Docker e comandos `manage.py`, vamos puxar todos os arquivos para a raiz do repositório (`AMMHelpDesk/`).

Adicionalmente, propomos a seguinte simplificação em relação ao design spec original:
- Em vez de criar uma pasta `apps/helpdesk/` (que exige manipulação do `sys.path` no Python/Django para evitar problemas de importação), manteremos a pasta do aplicativo principal como `app_helpdesk` diretamente na raiz.
- A pasta de configuração do Django (`AmmHelpDesk/AmmHelpDesk`) será renomeada para `config/` na raiz do repositório.
- A pasta de arquivos estáticos `Static/` será renomeada para `static/` (tudo em minúsculo, padrão web).

Isso resultará na seguinte estrutura limpa e profissional:

```
AMMHelpDesk/                     # Raiz do Repositório (Workspace)
├── config/                      # Renomeado de AmmHelpDesk/AmmHelpDesk/
│   ├── __init__.py
│   ├── settings.py              # Configurações refatoradas (com python-decouple)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── app_helpdesk/                # Aplicativo Django (movido para a raiz)
│   ├── migrations/
│   ├── templates/
│   │   └── app_helpdesk/        # Templates organizados e nomespaced
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── views.py
├── static/                      # Renomeado de Static/ e movido para a raiz
│   ├── css/
│   ├── js/
│   └── img/
├── requirements.txt             # Renomeado de requirements.tx
├── .env                         # NOVO - Contém credenciais (NÃO commitado no git)
├── .env.example                 # NOVO - Modelo de variáveis para o time
├── .gitignore                   # Atualizado para ignorar o .env e arquivos locais
├── manage.py                    # Movido para a raiz
└── claude.md                    # Guia de contexto para a IA
```

---

## 🔒 Variáveis de Ambiente e Segurança

Migraremos as seguintes credenciais expostas para o arquivo `.env`:
- `SECRET_KEY` do Django (gerada de forma aleatória e segura).
- Configuração de e-mail SMTP do Gmail (`EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD`).
- Configurações do Banco de Dados MySQL atual (Host remoto, Porta, Usuário, Senha e Nome do Banco).

---

## 🛠️ Alterações Propostas

### 1. Reestruturação de Arquivos e Pastas
- Mover todos os arquivos da pasta intermediária `AmmHelpDesk/` para a raiz do workspace.
- Excluir a pasta intermediária vazia `AmmHelpDesk/`.
- Renomear o diretório de configurações `AmmHelpDesk/AmmHelpDesk/` para `config/`.
- Renomear `requirements.tx` para `requirements.txt` e adicionar `python-decouple` às dependências.
- Renomear a pasta `Static` para `static`.

### 2. Atualização de Configurações (`config/settings.py`)
- Instalar e configurar `python-decouple` para ler do `.env`.
- Substituir as configurações estáticas de banco de dados e e-mail por chamadas `config()`.
- Atualizar a variável `ROOT_URLCONF` para `'config.urls'`.
- Atualizar a variável `WSGI_APPLICATION` para `'config.wsgi.application'`.
- Ajustar os caminhos de `STATICFILES_DIRS` e `TEMPLATES['DIRS']` para apontar para a nova estrutura na raiz do projeto.

### 3. Ajuste de Importações e Caminhos
- Atualizar `manage.py` para apontar para `config.settings`.
- Atualizar `config/wsgi.py` e `config/asgi.py` para apontar para `config.settings`.
- Atualizar imports internos de `app_helpdesk` (se houver alguma referência ao antigo nome do módulo).

---

## 📋 Open Questions (Perguntas para o Usuário)

> [!IMPORTANT]
> 1. **Deseja que já criemos os arquivos do Docker (`Dockerfile` e `docker-compose.yml`) com o PostgreSQL nesta primeira fase**, de modo que você possa testar o DBeaver imediatamente, ou prefere primeiro estabilizar o projeto com a nova estrutura de pastas na raiz usando o banco de dados MySQL atual?
> 2. **Validação das rotas:** Você gostaria que mantivéssemos o banco MySQL remoto ativo no `.env` durante os testes iniciais na nova estrutura para garantir que nada quebrou, antes de migrar definitivamente os dados para o PostgreSQL local no Docker?

---

## 🧪 Plano de Verificação

### Testes Manuais
1. Executar as migrações locais (se necessário) e iniciar o servidor na raiz:
   ```bash
   python manage.py runserver
   ```
2. Validar o carregamento da página de login (`/login/`).
3. Validar a submissão de um chamado de teste e conferir se as credenciais do `.env` foram lidas com sucesso.
