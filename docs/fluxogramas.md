# Fluxogramas do Sistema

## 1. Fluxo geral de navegação

Do acesso ao sistema até cada operação disponível no quadro.

```mermaid
flowchart TD
    inicio([Início]) --> acessa[Usuário acessa a página inicial /]
    acessa --> carrega[Sistema lista as tarefas ativas]
    carrega --> quadro[/Exibe quadro: A Fazer · Em Progresso · Concluído/]
    quadro --> acao{Qual ação?}

    acao -->|Criar| criar[[Fluxo: criar tarefa]]
    acao -->|Avançar / Voltar| mover[[Fluxo: mover tarefa]]
    acao -->|Editar| editar[[Fluxo: editar tarefa]]
    acao -->|Remover| remover[[Fluxo: remover tarefa]]
    acao -->|Sair| fim([Fim])

    criar --> carrega
    mover --> carrega
    editar --> carrega
    remover --> carrega
```

## 2. Criar tarefa

```mermaid
flowchart TD
    a([Início]) --> b[/Usuário informa título e descrição/]
    b --> c[POST /tarefas]
    c --> d{Título preenchido?}
    d -->|Não| e[Erro: O título é obrigatório]
    d -->|Sim| f{Título até 100 caracteres?}
    f -->|Não| g[Erro: máximo de 100 caracteres]
    f -->|Sim| h[(INSERT na tabela tarefas<br/>status = A Fazer)]
    h --> i[Mensagem: Tarefa criada com sucesso]
    e --> j[Redireciona para o quadro]
    g --> j
    i --> j
    j --> k([Fim])
```

## 3. Editar tarefa

```mermaid
flowchart TD
    a([Início]) --> b[Usuário clica em Editar]
    b --> c{Tarefa existe e está ativa?}
    c -->|Não| d[Erro 404]
    c -->|Sim| e[/Exibe formulário preenchido/]
    e --> f[/Usuário altera título, descrição e status/]
    f --> g[POST /tarefas/id/editar]
    g --> h{Dados válidos?}
    h -->|Não| i[Mostra erros e mantém no formulário]
    i --> f
    h -->|Sim| j[(UPDATE tarefas)]
    j --> k[Mensagem de sucesso e volta ao quadro]
    d --> z([Fim])
    k --> z
```

## 4. Mover tarefa (Avançar / Voltar)

```mermaid
flowchart TD
    a([Início]) --> b[Usuário clica em Avançar ou Voltar]
    b --> c[POST /tarefas/id/status<br/>com o status da coluna vizinha]
    c --> d{Tarefa existe?}
    d -->|Não| e[Erro 404]
    d -->|Sim| f{Status é válido?}
    f -->|Não| g[Mensagem: Status inválido]
    f -->|Sim| h[(UPDATE status)]
    h --> i[Mensagem: TF-0000 movida para ...]
    g --> j[Volta ao quadro]
    i --> j
    e --> k([Fim])
    j --> k
```

## 5. Remover tarefa (exclusão lógica)

```mermaid
flowchart TD
    a([Início]) --> b[Usuário clica em Remover]
    b --> c{Confirma no diálogo?}
    c -->|Não| z([Fim])
    c -->|Sim| d[POST /tarefas/id/remover]
    d --> e{Tarefa existe?}
    e -->|Não| f[Erro 404]
    e -->|Sim| g[(UPDATE excluida_em = agora)]
    g --> h[Tarefa some do quadro,<br/>registro continua no banco]
    f --> z
    h --> z
```

## 6. Ciclo de vida da tarefa (estados)

```mermaid
stateDiagram-v2
    [*] --> AFazer : criar
    AFazer : A Fazer
    EmProgresso : Em Progresso
    Concluido : Concluído

    AFazer --> EmProgresso : avançar
    EmProgresso --> Concluido : avançar
    Concluido --> EmProgresso : voltar
    EmProgresso --> AFazer : voltar

    AFazer --> Removida : remover
    EmProgresso --> Removida : remover
    Concluido --> Removida : remover
    Removida : Removida (exclusão lógica)
    Removida --> [*]
```

> Pela tela de edição também é possível trocar o status diretamente para qualquer coluna.

## 7. Fluxo de desenvolvimento e CI

Como uma mudança sai do Kanban e chega à branch `main`.

```mermaid
flowchart LR
    a[Issue no Kanban<br/>GitHub Projects] --> b[Desenvolvimento local]
    b --> c[Commit com<br/>closes #N]
    c --> d[git push / Pull Request]
    d --> e[GitHub Actions]
    e --> f[flake8]
    f --> g[pytest]
    g --> h{Passou?}
    h -->|Não| b
    h -->|Sim| i[Merge na main]
    i --> j[Issue fechada<br/>card vai para Done]
```
