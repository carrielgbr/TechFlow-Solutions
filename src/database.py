"""Acesso ao banco SQLite."""
import sqlite3

from src.models import Tarefa

DB_PADRAO = "tarefas.db"


def conectar(caminho=DB_PADRAO):
    """Abre uma conexão com o banco. Linhas acessíveis pelo nome da coluna."""
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela(caminho=DB_PADRAO):
    """Cria a tabela de tarefas caso ela ainda não exista."""
    with conectar(caminho) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'A Fazer'
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
    """Devolve todas as tarefas, da mais recente para a mais antiga."""
    with conectar(caminho) as conn:
        linhas = conn.execute("SELECT * FROM tarefas ORDER BY id DESC").fetchall()
    return [
        Tarefa(l["titulo"], l["descricao"], l["status"], l["id"]) for l in linhas
    ]