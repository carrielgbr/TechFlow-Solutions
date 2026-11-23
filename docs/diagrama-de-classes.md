# Diagrama de Classes (UML)

O sistema segue uma separação em três camadas:

- **Modelo** (`src/models.py`): a classe `Tarefa` e suas regras de validação.
- **Persistência** (`src/database.py`): funções de acesso ao SQLite.
- **Controle/Visão** (`src/app.py` + `templates/`): rotas Flask que recebem as requisições
  e renderizam as páginas.

Como `database.py` e `app.py` são módulos Python (funções, não classes), eles aparecem
com os estereótipos `<<módulo>>` e `<<controller>>`.

```mermaid
classDiagram
    direction TB

    class Tarefa {
        +int id
        +str titulo
        +str descricao
        +str status
        +codigo() str
        +validar() list~str~
    }
    note for Tarefa "status ∈ STATUS_VALIDOS<br>codigo = 'TF-' + id com 4 dígitos"

    class STATUS_VALIDOS {
        <<enumeration>>
        A Fazer
        Em Progresso
        Concluído
    }

    class database {
        <<módulo>>
        +str DB_PADRAO = "tarefas.db"
        +conectar(caminho) Connection
        +criar_tabela(caminho) None
        +criar_tarefa(tarefa, caminho) int
        +listar_tarefas(caminho) list~Tarefa~
        +buscar_tarefa(id_tarefa, caminho) Tarefa
        +atualizar_tarefa(tarefa, caminho) None
        +remover_tarefa(id_tarefa, caminho) None
        -_para_tarefa(linha) Tarefa
    }

    class app {
        <<controller>>
        +Flask app
        +index() GET /
        +criar() POST /tarefas
        +editar(id_tarefa) GET|POST /tarefas/id/editar
        +mover(id_tarefa) POST /tarefas/id/status
        +remover(id_tarefa) POST /tarefas/id/remover
        -_db() str
        -_buscar_ou_404(id_tarefa) Tarefa
    }

    Tarefa ..> STATUS_VALIDOS : valida contra
    database ..> Tarefa : cria e persiste
    app ..> database : usa
    app ..> Tarefa : instancia
```

## Responsabilidades

| Elemento | Responsabilidade |
|---|---|
| `Tarefa` | Guardar os dados de uma tarefa, gerar o código `TF-0000` e validar título/status |
| `STATUS_VALIDOS` | Lista fixa das colunas do Kanban |
| `database` | Abrir conexão, criar tabela e executar o CRUD (com exclusão lógica) |
| `app` | Receber as requisições HTTP, chamar validação/banco e renderizar os templates |

## Diagrama de sequência: criar tarefa

Mostra como as camadas conversam quando o usuário envia o formulário de nova tarefa.

```mermaid
sequenceDiagram
    actor U as Membro da equipe
    participant N as Navegador
    participant A as app.py (Flask)
    participant T as Tarefa
    participant D as database.py
    participant B as SQLite

    U->>N: Preenche título e descrição
    N->>A: POST /tarefas
    A->>T: Tarefa(titulo, descricao)
    A->>T: validar()
    T-->>A: lista de erros

    alt dados válidos
        A->>D: criar_tarefa(tarefa)
        D->>B: INSERT INTO tarefas
        B-->>D: id gerado
        A->>N: flash "Tarefa criada" + redirect /
    else dados inválidos
        A->>N: flash com os erros + redirect /
    end

    N->>A: GET /
    A->>D: listar_tarefas()
    D->>B: SELECT ... WHERE excluida_em IS NULL
    B-->>D: linhas
    D-->>A: list[Tarefa]
    A-->>N: index.html (quadro Kanban)
```
