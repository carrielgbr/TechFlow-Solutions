"""Testes automatizados do TechFlow Tasks."""
import pytest

from src.app import app
from src.database import (
    conectar, criar_tabela, criar_tarefa, listar_tarefas,
    buscar_tarefa, atualizar_tarefa, remover_tarefa,
)
from src.models import Tarefa


@pytest.fixture
def db(tmp_path):
    """Banco temporário: cada teste começa com o banco vazio."""
    caminho = str(tmp_path / "teste.db")
    criar_tabela(caminho)
    return caminho


# ---------- Modelo ----------

def test_tarefa_valida_nao_tem_erros():
    assert Tarefa("Escrever README").validar() == []


def test_titulo_vazio_e_invalido():
    assert "O título é obrigatório." in Tarefa("   ").validar()


def test_titulo_muito_longo_e_invalido():
    assert Tarefa("x" * 101).validar() != []


def test_status_invalido():
    assert "Status inválido." in Tarefa("Teste", status="Qualquer").validar()


def test_codigo_da_tarefa():
    assert Tarefa("Teste", id=1).codigo == "TF-0001"
    assert Tarefa("Teste", id=12345).codigo == "TF-12345"


# ---------- Banco ----------

def test_criar_e_listar(db):
    criar_tarefa(Tarefa("Primeira"), db)
    tarefas = listar_tarefas(db)
    assert len(tarefas) == 1
    assert tarefas[0].titulo == "Primeira"


def test_atualizar_status(db):
    id_tarefa = criar_tarefa(Tarefa("Mudar status"), db)
    tarefa = buscar_tarefa(id_tarefa, db)
    tarefa.status = "Concluído"
    atualizar_tarefa(tarefa, db)
    assert buscar_tarefa(id_tarefa, db).status == "Concluído"


def test_exclusao_logica_esconde_mas_mantem_no_banco(db):
    id_tarefa = criar_tarefa(Tarefa("Apagar"), db)
    remover_tarefa(id_tarefa, db)

    assert listar_tarefas(db) == []
    assert buscar_tarefa(id_tarefa, db) is None

    # o registro continua no banco, só está marcado como excluído
    with conectar(db) as conn:
        linha = conn.execute(
            "SELECT excluida_em FROM tarefas WHERE id = ?", (id_tarefa,)
        ).fetchone()
    assert linha["excluida_em"] is not None


# ---------- Rotas ----------

def test_pagina_inicial_responde():
    resposta = app.test_client().get("/")
    assert resposta.status_code == 200