"""Aplicação web Flask do TechFlow Tasks."""
from flask import Flask, render_template, request, redirect, url_for, flash

from src.database import criar_tabela, criar_tarefa, listar_tarefas
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