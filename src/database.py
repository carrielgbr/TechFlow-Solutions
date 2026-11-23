"""Acesso ao banco SQLite."""
import sqlite3

from src.models import Tarefa

DB_PADRAO = "tarefas.db"


def conectar(caminho=DB_PADRAO):
    """Abre uma conexão com o banco (linhas acessíveis por nome)."""
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    return conn


def _para_tarefa(linha):
    """Converte uma linha do banco em um objeto Tarefa."""
    return Tarefa(
        linha["titulo"], linha["descricao"], linha["status"], linha["id"]
    )


def criar_tabela(caminho=DB_PADRAO):
    """Cria a tabela de tarefas caso ela ainda não exista."""
    with conectar(caminho) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'A Fazer',
                excluida_em TEXT DEFAULT NULL
            )
            """
        )


def criar_tarefa(tarefa, caminho=DB_PADRAO):
    """Insere uma tarefa no banco e devolve o id gerado."""
    with conectar(caminho) as conn:
        cursor = conn.execute(
            "INSERT INTO tarefas (titulo, descricao, status) VALUES (?, ?, ?)",
            (tarefa.titulo, tarefa.descricao, tarefa.status),
        )
        return cursor.lastrowid


def listar_tarefas(caminho=DB_PADRAO):
    """Devolve as tarefas ativas, da mais recente para a mais antiga."""
    with conectar(caminho) as conn:
        linhas = conn.execute(
            "SELECT * FROM tarefas "
            "WHERE excluida_em IS NULL ORDER BY id DESC"
        ).fetchall()
    return [_para_tarefa(linha) for linha in linhas]


def buscar_tarefa(id_tarefa, caminho=DB_PADRAO):
    """Devolve uma tarefa ativa pelo id, ou None se não existir."""
    with conectar(caminho) as conn:
        linha = conn.execute(
            "SELECT * FROM tarefas WHERE id = ? AND excluida_em IS NULL",
            (id_tarefa,),
        ).fetchone()
    if linha is None:
        return None
    return _para_tarefa(linha)


def atualizar_tarefa(tarefa, caminho=DB_PADRAO):
    """Grava no banco as alterações de uma tarefa existente."""
    with conectar(caminho) as conn:
        conn.execute(
            "UPDATE tarefas SET titulo = ?, descricao = ?, status = ? "
            "WHERE id = ?",
            (tarefa.titulo, tarefa.descricao, tarefa.status, tarefa.id),
        )


def remover_tarefa(id_tarefa, caminho=DB_PADRAO):
    """Exclusão lógica: marca a tarefa como excluída, sem apagar o registro."""
    with conectar(caminho) as conn:
        conn.execute(
            "UPDATE tarefas SET excluida_em = datetime('now') WHERE id = ?",
            (id_tarefa,),
        )
