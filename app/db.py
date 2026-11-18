"""Acesso ao banco de dados SQLite."""

import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS tarefas (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo     TEXT    NOT NULL,
    prioridade TEXT    NOT NULL DEFAULT 'media'
               CHECK (prioridade IN ('baixa', 'media', 'alta')),
    concluida  INTEGER NOT NULL DEFAULT 0,
    criada_em  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
"""


def get_db():
    """Devolve a conexão do request atual (cria se ainda não existir)."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
    return g.db


def close_db(e=None):
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


def init_db():
    conexao = get_db()
    conexao.executescript(SCHEMA)
    conexao.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
