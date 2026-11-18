"""Fábrica da aplicação Flask (padrão "application factory")."""

import os

from flask import Flask

from . import db, routes


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Configuração padrão. Em produção, defina a variável SECRET_KEY.
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-troque-em-producao"),
        DATABASE=os.path.join(app.instance_path, "tarefas.db"),
    )

    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    app.register_blueprint(routes.bp)

    return app
