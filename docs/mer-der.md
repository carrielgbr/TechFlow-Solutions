# Modelagem do Banco de Dados (MER e DER)

O banco é um arquivo **SQLite** (`tarefas.db`) criado automaticamente por
`criar_tabela()` em `src/database.py`. A versão atual tem uma única entidade, `TAREFA`.

## 1. MER: Modelo Entidade-Relacionamento (conceitual)

Notação de Peter Chen: retângulo = entidade, elipse = atributo,
**PK** = identificador.

```mermaid
flowchart TB
    T[TAREFA]

    id(("id (PK)"))
    titulo((titulo))
    descricao((descricao))
    status((status))
    excluida((excluida_em))
    codigo(("codigo<br/>(derivado)"))

    T --- id
    T --- titulo
    T --- descricao
    T --- status
    T --- excluida
    T -.- codigo
```

- `codigo` é um **atributo derivado**: não é gravado no banco, é calculado a partir do `id`
  (`TF-0001`).
- `status` é um atributo com **domínio restrito**: `A Fazer`, `Em Progresso` ou `Concluído`.
- `excluida_em` registra a **exclusão lógica** (vazio = tarefa ativa).

## 2. DER: Diagrama Entidade-Relacionamento (lógico/físico)

Notação pé de galinha (Crow's Foot), com os tipos do SQLite.

```mermaid
erDiagram
    TAREFAS {
        INTEGER id PK "AUTOINCREMENT"
        TEXT titulo "NOT NULL, até 100 caracteres"
        TEXT descricao "DEFAULT ''"
        TEXT status "NOT NULL, DEFAULT 'A Fazer'"
        TEXT excluida_em "NULL = ativa; data = removida"
    }
```

## 3. Dicionário de dados

| Coluna | Tipo | Nulo? | Padrão | Restrição / regra |
|---|---|---|---|---|
| `id` | INTEGER | Não | auto | Chave primária, `AUTOINCREMENT` |
| `titulo` | TEXT | Não | — | Obrigatório, máx. 100 caracteres (validado em `Tarefa.validar()`) |
| `descricao` | TEXT | Sim | `''` | Texto livre |
| `status` | TEXT | Não | `'A Fazer'` | `A Fazer`, `Em Progresso` ou `Concluído` (validado na aplicação) |
| `excluida_em` | TEXT | Sim | `NULL` | Data/hora da exclusão lógica (`datetime('now')`) |

## 4. Script SQL (DDL)

```sql
CREATE TABLE IF NOT EXISTS tarefas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo      TEXT NOT NULL,
    descricao   TEXT DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'A Fazer',
    excluida_em TEXT DEFAULT NULL
);
```

## 5. Consultas usadas pelo sistema

| Operação | SQL |
|---|---|
| Criar | `INSERT INTO tarefas (titulo, descricao, status) VALUES (?, ?, ?)` |
| Listar ativas | `SELECT * FROM tarefas WHERE excluida_em IS NULL ORDER BY id DESC` |
| Buscar por id | `SELECT * FROM tarefas WHERE id = ? AND excluida_em IS NULL` |
| Atualizar / mover | `UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ?` |
| Remover (lógica) | `UPDATE tarefas SET excluida_em = datetime('now') WHERE id = ?` |

## 6. Evolução proposta (fora do escopo atual)

Para atender ao objetivo de *monitorar o desempenho da equipe*, uma próxima versão poderia
separar usuários e o histórico de mudanças de status. Este modelo **ainda não está
implementado**; serve como planejamento.

```mermaid
erDiagram
    USUARIOS ||--o{ TAREFAS : "é responsável por"
    TAREFAS ||--o{ HISTORICO_STATUS : "registra"
    USUARIOS ||--o{ HISTORICO_STATUS : "altera"

    USUARIOS {
        INTEGER id PK
        TEXT nome
        TEXT email UK
    }
    TAREFAS {
        INTEGER id PK
        TEXT titulo
        TEXT descricao
        TEXT status
        TEXT prioridade
        INTEGER responsavel_id FK
        TEXT criada_em
        TEXT excluida_em
    }
    HISTORICO_STATUS {
        INTEGER id PK
        INTEGER tarefa_id FK
        INTEGER usuario_id FK
        TEXT status_anterior
        TEXT status_novo
        TEXT alterado_em
    }
```
