"""Aplicação web Flask do TechFlow Tasks."""
from flask import Flask, abort, render_template, request, redirect, url_for, flash

from src.database import (
    DB_PADRAO, criar_tabela, criar_tarefa, listar_tarefas, buscar_tarefa,
    atualizar_tarefa, remover_tarefa,
)
from src.models import Tarefa, STATUS_VALIDOS

app = Flask(__name__)
app.secret_key = "dev-troque-em-producao"  # necessário para as mensagens flash
app.config["DATABASE"] = DB_PADRAO  # os testes trocam por um banco temporário


def _db():
    """Caminho do banco configurado na aplicação."""
    return app.config["DATABASE"]


criar_tabela(_db())


def _buscar_ou_404(id_tarefa):
    """Busca a tarefa ativa ou responde 404."""
    tarefa = buscar_tarefa(id_tarefa, _db())
    if tarefa is None:
        abort(404)
    return tarefa


@app.route("/")
def index():
    """Página principal: quadro Kanban com as tarefas e formulário de criação."""
    tarefas = listar_tarefas(_db())
    colunas = {s: [t for t in tarefas if t.status == s] for s in STATUS_VALIDOS}
    return render_template(
        "index.html", colunas=colunas, total=len(tarefas), status_validos=STATUS_VALIDOS
    )


@app.route("/tarefas", methods=["POST"])
def criar():
    """Recebe o formulário, valida e cria a tarefa."""
    tarefa = Tarefa(request.form.get("titulo", ""), request.form.get("descricao", ""))
    erros = tarefa.validar()

    if erros:
        for erro in erros:
            flash(erro, "erro")
    else:
        criar_tarefa(tarefa, _db())
        flash("Tarefa criada com sucesso!", "sucesso")

    return redirect(url_for("index"))


@app.route("/tarefas/<int:id_tarefa>/editar", methods=["GET", "POST"])
def editar(id_tarefa):
    """Mostra o formulário de edição (GET) e salva as alterações (POST)."""
    tarefa = _buscar_ou_404(id_tarefa)

    if request.method == "POST":
        tarefa.titulo = request.form.get("titulo", "")
        tarefa.descricao = request.form.get("descricao", "")
        tarefa.status = request.form.get("status", tarefa.status)
        erros = tarefa.validar()

        if erros:
            for erro in erros:
                flash(erro, "erro")
        else:
            atualizar_tarefa(tarefa, _db())
            flash("Tarefa atualizada com sucesso!", "sucesso")
            return redirect(url_for("index"))

    return render_template("editar.html", tarefa=tarefa, status_validos=STATUS_VALIDOS)


@app.route("/tarefas/<int:id_tarefa>/status", methods=["POST"])
def mover(id_tarefa):
    """Move a tarefa para outra coluna do quadro (muda só o status)."""
    tarefa = _buscar_ou_404(id_tarefa)
    tarefa.status = request.form.get("status", "")
    erros = tarefa.validar()
    if erros:
        for erro in erros:
            flash(erro, "erro")
    else:
        atualizar_tarefa(tarefa, _db())
        flash(f"{tarefa.codigo} movida para {tarefa.status}.", "sucesso")

    return redirect(url_for("index"))


@app.route("/tarefas/<int:id_tarefa>/remover", methods=["POST"])
def remover(id_tarefa):
    """Exclusão lógica da tarefa (o registro continua no banco)."""
    tarefa = _buscar_ou_404(id_tarefa)
    remover_tarefa(tarefa.id, _db())
    flash(f"{tarefa.codigo} removida.", "sucesso")
    return redirect(url_for("index"))
