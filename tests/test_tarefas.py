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


@pytest.fixture
def cliente(db):
    """Cliente de teste do Flask apontando para o banco temporário."""
    app.config["DATABASE"] = db
    app.config["TESTING"] = True
    yield app.test_client()
    app.config["DATABASE"] = "tarefas.db"


def test_pagina_inicial_responde(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert "Quadro de tarefas" in resposta.get_data(as_text=True)


def test_criar_pela_rota(cliente, db):
    cliente.post("/tarefas", data={"titulo": "Via formulário", "descricao": ""})
    assert listar_tarefas(db)[0].titulo == "Via formulário"


def test_mover_tarefa_de_coluna(cliente, db):
    id_tarefa = criar_tarefa(Tarefa("Mover"), db)
    resposta = cliente.post(f"/tarefas/{id_tarefa}/status", data={"status": "Em Progresso"})
    assert resposta.status_code == 302
    assert buscar_tarefa(id_tarefa, db).status == "Em Progresso"


def test_mover_com_status_invalido_nao_altera(cliente, db):
    id_tarefa = criar_tarefa(Tarefa("Mover"), db)
    cliente.post(f"/tarefas/{id_tarefa}/status", data={"status": "Qualquer"})
    assert buscar_tarefa(id_tarefa, db).status == "A Fazer"


def test_remover_pela_rota(cliente, db):
    id_tarefa = criar_tarefa(Tarefa("Remover"), db)
    cliente.post(f"/tarefas/{id_tarefa}/remover")
    assert buscar_tarefa(id_tarefa, db) is None


def test_tarefa_inexistente_da_404(cliente):
    assert cliente.get("/tarefas/999/editar").status_code == 404
    assert cliente.post("/tarefas/999/remover").status_code == 404
