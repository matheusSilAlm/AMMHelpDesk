# AMMHelpDesk — Project Knowledge Base & AI Guide

Este arquivo funciona como a documentação central e guia de contexto para a inteligência artificial. Ele foi gerado para otimizar o fluxo de trabalho e resumir a estrutura, o estado atual e o plano de refatoração do projeto **AMMHelpDesk**.

---

## 📌 Visão Geral do Projeto
O **AMMHelpDesk** é um sistema de Help Desk desenvolvido em **Django (Python)** para gerenciamento de chamados de clientes. O sistema permite:
- **Clientes:** Submeterem chamados informando seus dados, assunto e descrição detalhada do problema.
- **Operadores (Agentes):** Fazerem login, visualizarem a lista de chamados ordenados por ID, definirem prioridades, atualizarem o status (ABERTO, EM ANDAMENTO, FECHADO), responderem aos chamados diretamente com imagens embutidas (convertidas de base64) e anexos, além de enviarem e-mails automáticos com as respostas.
- **FAQ:** Consulta pública e busca de chamados e soluções anteriores.

---

## 📁 Estrutura Atual do Projeto
O projeto foi reestruturado de forma limpa e profissional diretamente na raiz do repositório:

```
AMMHelpDesk/
├── .antigravitycli/           # Configuração de Skills adotadas pela IA
│   ├── caveman-review.md      # Instruções para code review ultra-curto (terse)
│   └── fix-review.md          # Diretrizes para correções de bugs, segurança e transações
├── .claude/
│   └── settings.local.json    # Configurações de permissões locais
├── config/                    # Módulo de configuração do Django (renomeado de AmmHelpDesk/AmmHelpDesk/)
│   ├── __init__.py
│   ├── settings.py            # Configurações refatoradas lendo do .env
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── app_helpdesk/              # Aplicativo principal do Help Desk (movido para a raiz)
│   ├── migrations/            # Migrações do banco de dados
│   ├── templates/             # Arquivos HTML da aplicação
│   ├── admin.py               # Registro de modelos no Django Admin
│   ├── apps.py                # Configuração do app
│   ├── models.py              # Definição dos modelos Django (ORM)
│   ├── tests.py               # Testes unitários da aplicação
│   └── views.py               # Lógica das rotas, envio de e-mails e controle
├── static/                    # Arquivos estáticos (renomeado para lowercase e movido para a raiz)
│   ├── css/
│   ├── js/
│   └── img/
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-05-22-helpdesk-refactor-design.md # Especificação do refactoring planejado
├── .env                       # Variáveis de ambiente seguras (com senhas e chaves)
├── .env.example               # Exemplo de variáveis de ambiente para a equipe
├── .gitignore                 # Arquivo de ignores do Git atualizado
├── Anotações                  # Esquema SQL original (DDL para MySQL)
├── db.sqlite3                 # Banco SQLite local
├── requirements.txt           # Dependências do projeto atualizadas (com python-decouple)
├── manage.py                  # Script de gerenciamento do Django (movido para a raiz)
├── README.md                  # Arquivo básico de README
└── claude.md                  # [ESTE ARQUIVO] Base de conhecimento da IA
```

---

## 🗄️ Esquema de Modelos & Banco de Dados
A modelagem é baseada no banco de dados **MySQL** (`hdesk`), cujas credenciais atuais estão expostas no arquivo `settings.py` (com acesso remoto configurado).

### Modelos Principais (`app_helpdesk/models.py`)

1. **`Cliente`**
   - Armazena dados cadastrais do cliente que abriu o chamado.
   - Campos: `idcliente` (Auto-increment PK), `nomecliente`, `cpf_cnpj`, `datacriacao`, `email_cliente`, `telefone_cliente`, `assunto`, `descricao`, `resposta_usuario` (rica em HTML), `faq_enviar`.
2. **`Usuario`**
   - Representa os operadores/agentes do Help Desk.
   - Campos: `idusuario` (Auto-increment PK), `nomeusuario`, `email_usuario`, `setor`, `turno`, `usuario_ativo`.
3. **`Solicitacao`**
   - Associa um cliente a um atendente e define a prioridade.
   - Relacionamentos: `idcliente` (FK -> Cliente), `idusuario` (FK -> Usuario).
   - Campos: `assunto`, `prioridade`, `data_solicitacao`, `solicitacaoaativo`.
4. **`Solicitacaostatus`**
   - Controla o estado atual de cada chamado (ex: ABERTO, EM ANDAMENTO, FECHADO).
   - Relacionamentos: `idsolicitacao` (FK -> Solicitacao), `idusuario` (FK -> Usuario).
   - Campos: `idstatus`, `datastatus`.

---

## 🛠️ Skills Adotadas (`.antigravitycli/`)
Como assistente de IA, adotei completamente as diretrizes e "skills" definidas na pasta `.antigravitycli`:

1. **`caveman-review`**
   - **Objetivo:** Revisões de código extremamente compactas e diretas.
   - **Formato:** Uma única linha por observação no padrão: `L<linha>: <🔴 bug|🟡 risk|🔵 nit|❓ q>: <descrição do problema>. <ação concreta para consertar>.`
   - **Aplicação:** Usado automaticamente quando solicitado um review de código, diff ou PR.

2. **`fix-review`**
   - **Objetivo:** Regras rigorosas de engenharia para correção de bugs.
   - **Diretrizes Principais:**
     - Corrigir bugs de alta prioridade primeiro.
     - **Tratamento defensivo:** Verificar cabeçalhos de resposta e tipos de dados antes de processar/decodificar payloads.
     - **Integridade de Transações:** Efeitos colaterais (como envio de e-mails) só devem acontecer *após* o commit definitivo no banco de dados (`transaction.on_commit`).
     - **Validação no Servidor:** Nunca confiar exclusivamente na validação cliente-side.
     - **UI Segura:** Operações assíncronas não devem falhar silenciosamente; tratamento visual obrigatório.
     - Fornecer explicações técnicas concisas do fluxo arquitetural de cada modificação.

---

## 🚀 Plano de Refatoração Planejado (Design Spec)
Conforme documentado em [2026-05-22-helpdesk-refactor-design.md](file:///C:/Users/vibon/OneDrive/%C3%81rea%20de%20Trabalho/dev/python/django/HelpDeskTchola/AMMHelpDesk/docs/superpowers/specs/2026-05-22-helpdesk-refactor-design.md), o projeto passará por um processo de refatoração em fases:

### 🧩 Fase 1 — Estrutura do Projeto + Configurações
- **Organização:** Mover configurações para `config/settings/` (base.py, development.py, production.py).
- **Segurança:** Isolar credenciais em arquivo `.env` usando `python-decouple`. Mapear variáveis de ambiente.
- **Refatoração de Formulários:** Substituir o tratamento de posts brutos por formulários Django (`forms.py`) com validações robustas (CPF/CNPJ, e-mail, telefone).
- **Separação de Requisitos:** Criar arquivos específicos na pasta `requirements/` (base.txt, development.txt, production.txt).

### ⚙️ Fase 2 — Backend, PostgreSQL e Docker
- **Readequação de Performance:** Resolver o problema de N+1 queries na listagem de chamados usando `select_related`/`prefetch_related`.
- **Banco de Dados:** Migrar de MySQL remoto para PostgreSQL (com backup e restauração dos dados atuais via JSON).
- **Tratamento de Exceções:** Adicionar logs e tratamento de erros no envio de e-mails.
- **Docker:** Containerizar a aplicação (`Dockerfile`, `docker-compose.yml` e Nginx).

### 🎨 Fase 3 — Reorganização de Templates e Tailwind CSS
- **Herança de Templates:** Criar `base.html` como layout master global.
- **Tailwind CSS:** Implementar Tailwind CSS nos templates de forma responsiva e visualmente premium.
- **Limpeza de Estilo:** Remover estilos inline antigos e consolidar parciais reutilizáveis (navbar, footer, paginação).

### 🔒 Fase 4 — Polimento e Auditoria de Segurança
- **Segurança de Produção:** Configurar cabeçalhos HSTS, cookies seguros, redirecionamentos HTTPS.
- **Limitação de Taxa:** Implementar rate-limiting nas rotas críticas (como login).
- **Garantia de Transação:** Assegurar que os e-mails só sejam enviados após commits atômicos confirmados.

---

## 💡 Como Executar e Validar o Projeto
Atualmente, o projeto está configurado para executar com MySQL:
1. Instale os requisitos atuais:
   ```bash
   pip install -r requirements.tx
   ```
2. Inicie o servidor Django local:
   ```bash
   python AmmHelpDesk/manage.py runserver
   ```
3. Acesse a aplicação em: `http://127.0.0.1:8000/`

---

> **Nota para a IA:** Sempre que interagir com este repositório, consulte este arquivo para manter a consistência com as regras de design e de engenharia estabelecidas para o projeto.
