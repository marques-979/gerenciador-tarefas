"""Rotas da aplicação: CRUD de tarefas e uma pequena API JSON."""

from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from .db import get_db

bp = Blueprint("tarefas", __name__)

PRIORIDADES = ("baixa", "media", "alta")
FILTROS = {
    "todas": "",
    "pendentes": "WHERE concluida = 0",
    "concluidas": "WHERE concluida = 1",
}


def buscar_tarefa(tarefa_id):
    tarefa = get_db().execute(
        "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
    ).fetchone()
    if tarefa is None:
        abort(404)
    return tarefa


@bp.route("/")
def index():
    filtro = request.args.get("filtro", "todas")
    if filtro not in FILTROS:
        filtro = "todas"

    # A cláusula WHERE vem do dicionário FILTROS (nunca do usuário),
    # então é seguro concatenar aqui.
    tarefas = get_db().execute(
        f"""
        SELECT * FROM tarefas {FILTROS[filtro]}
        ORDER BY concluida,
                 CASE prioridade WHEN 'alta' THEN 0 WHEN 'media' THEN 1 ELSE 2 END,
                 id DESC
        """
    ).fetchall()

    total = get_db().execute("SELECT COUNT(*) FROM tarefas").fetchone()[0]
    feitas = get_db().execute(
        "SELECT COUNT(*) FROM tarefas WHERE concluida = 1"
    ).fetchone()[0]

    return render_template(
        "index.html",
        tarefas=tarefas,
        filtro=filtro,
        total=total,
        feitas=feitas,
        prioridades=PRIORIDADES,
    )


@bp.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form.get("titulo", "").strip()
    prioridade = request.form.get("prioridade", "media")

    if not titulo:
        flash("Digite um título para a tarefa.", "erro")
    elif prioridade not in PRIORIDADES:
        flash("Prioridade inválida.", "erro")
    else:
        db = get_db()
        db.execute(
            "INSERT INTO tarefas (titulo, prioridade) VALUES (?, ?)",
            (titulo, prioridade),
        )
        db.commit()
        flash("Tarefa adicionada!", "sucesso")

    return redirect(url_for("tarefas.index"))


@bp.route("/<int:tarefa_id>/alternar", methods=["POST"])
def alternar(tarefa_id):
    buscar_tarefa(tarefa_id)
    db = get_db()
    db.execute(
        "UPDATE tarefas SET concluida = 1 - concluida WHERE id = ?", (tarefa_id,)
    )
    db.commit()
    return redirect(request.referrer or url_for("tarefas.index"))


@bp.route("/<int:tarefa_id>/editar", methods=["GET", "POST"])
def editar(tarefa_id):
    tarefa = buscar_tarefa(tarefa_id)

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        prioridade = request.form.get("prioridade", tarefa["prioridade"])

        if not titulo:
            flash("O título não pode ficar vazio.", "erro")
        elif prioridade not in PRIORIDADES:
            flash("Prioridade inválida.", "erro")
        else:
            db = get_db()
            db.execute(
                "UPDATE tarefas SET titulo = ?, prioridade = ? WHERE id = ?",
                (titulo, prioridade, tarefa_id),
            )
            db.commit()
            flash("Tarefa atualizada!", "sucesso")
            return redirect(url_for("tarefas.index"))

    return render_template("editar.html", tarefa=tarefa, prioridades=PRIORIDADES)


@bp.route("/<int:tarefa_id>/excluir", methods=["POST"])
def excluir(tarefa_id):
    buscar_tarefa(tarefa_id)
    db = get_db()
    db.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    db.commit()
    flash("Tarefa excluída.", "sucesso")
    return redirect(url_for("tarefas.index"))


@bp.route("/api/tarefas")
def api_tarefas():
    """Lista as tarefas em JSON (útil para mostrar uma API no portfólio)."""
    linhas = get_db().execute("SELECT * FROM tarefas ORDER BY id").fetchall()
    return jsonify([dict(linha) | {"concluida": bool(linha["concluida"])} for linha in linhas])
