# Gerenciador de Tarefas

Aplicação web de lista de tarefas feita com **Python**, **Flask** e **SQLite**.
Projeto de portfólio que demonstra um CRUD completo, organização em camadas,
validação de dados e testes automatizados.

## Funcionalidades

- Adicionar, editar, concluir e excluir tarefas
- Prioridade (baixa, média, alta) com ordenação automática
- Filtros: todas, pendentes e concluídas
- Contador de progresso
- Endpoint JSON em `/api/tarefas`
- Testes automatizados com `pytest`

## Tecnologias

- Python 3.10+
- Flask (application factory + Blueprints)
- SQLite (módulo `sqlite3` da biblioteca padrão, com consultas parametrizadas)
- Jinja2 (templates) e CSS puro
- pytest

## Como executar

```bash
# 1. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Rode a aplicação
python run.py
```

Acesse http://127.0.0.1:5000

## Como rodar os testes

```bash
pytest -v
```

## Estrutura do projeto

```
gerenciador-tarefas/
├── app/
│   ├── __init__.py      # create_app(): configura e monta a aplicação
│   ├── db.py            # conexão e criação da tabela
│   ├── routes.py        # rotas (Blueprint)
│   ├── static/style.css
│   └── templates/       # base.html, index.html, editar.html
├── tests/test_app.py
├── run.py
└── requirements.txt
```

## Decisões técnicas

- **Application factory**: facilita testes, pois cada teste cria um app com um banco temporário.
- **Consultas parametrizadas** (`?`): evitam SQL Injection.
- **Escape automático do Jinja2**: evita XSS (há um teste para isso).
- **Validação no servidor**: título obrigatório e prioridade restrita a valores válidos (também garantida por `CHECK` no banco).

## Próximos passos (ideias para evoluir)

- Autenticação de usuários (Flask-Login)
- Proteção CSRF (Flask-WTF)
- Data de vencimento e busca por texto
- Trocar SQLite por PostgreSQL com SQLAlchemy
- Deploy (Render, Railway ou PythonAnywhere)
- Integração contínua com GitHub Actions rodando o `pytest`

## Autor

Ismael Costa Marques —  [LinkedIn](https://linkedin.com/in/ismael-costa-marques)
