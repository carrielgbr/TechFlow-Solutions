"""Aplicação web Flask do TechFlow Tasks."""
from flask import Flask, abort, render_template, request, redirect, url_for, flash

from src.database import (
    criar_tabela, criar_tarefa, listar_tarefas, buscar_tarefa, atualizar_tarefa
)
from src.models import Tarefa, STATUS_VALIDOS

app = Flask(__name__)
app.secret_key = "dev-troque-em-producao"  # necessário para as mensagens flash

criar_tabela()


@app.route("/")
def index():
    """Página principal: lista as tarefas e mostra o formulário."""
    return render_template(
        "index.html", tarefas=listar_tarefas(), status_validos=STATUS_VALIDOS
    )


@app.route("/tarefas", methods=["POST"])
def criar():
    """Recebe o formulário, valida e cria a tarefa."""
    tarefa = Tarefa(request.form.get("titulo", ""), request.form.get("descricao", ""))
    erros = tarefa.validar()

    if erros:
        for erro in erros:
            flash(erro)
    else:
        criar_tarefa(tarefa)
        flash("Tarefa criada com sucesso!")

    return redirect(url_for("index"))


@app.route("/tarefas/<int:id_tarefa>/editar", methods=["GET", "POST"])
def editar(id_tarefa):
    """Mostra o formulário de edição (GET) e salva as alterações (POST)."""
    tarefa = buscar_tarefa(id_tarefa)
    if tarefa is None:
        abort(404)

    if request.method == "POST":
        tarefa.titulo = request.form.get("titulo", "")
        tarefa.descricao = request.form.get("descricao", "")
        tarefa.status = request.form.get("status", tarefa.status)
        erros = tarefa.validar()

        if erros:
            for erro in erros:
                flash(erro)
        else:
            atualizar_tarefa(tarefa)
            flash("Tarefa atualizada com sucesso!")
            return redirect(url_for("index"))

    return render_template("editar.html", tarefa=tarefa, status_validos=STATUS_VALIDOS)
