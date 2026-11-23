# TechFlow-Solutions
Sistema web de gerenciamento de tarefas com metodologia ágil, Kanban e CI com GitHub Actions


# TechFlow Solutions: Sistema de Gerenciamento de Tarefas

## Objetivo
Sistema web para a startup de logística acompanhar o fluxo de trabalho,
priorizar tarefas críticas e monitorar o desempenho da equipe.

## Escopo inicial
- Criar, listar, editar e remover tarefas (CRUD, com exclusão lógica)
- Quadro Kanban com as colunas A Fazer, Em Progresso e Concluído
- Mover tarefas entre colunas com os botões Avançar e Voltar

## Metodologia
Kanban híbrido com Scrum: quadro no GitHub Projects, entregas pequenas
e commits frequentes, cada card vinculado a uma issue.

## Como executar
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask --app src.app run --debug
```
Acesse http://127.0.0.1:5000.

## Testes e qualidade
```bash
pytest -v
flake8 src tests
```
O GitHub Actions roda os mesmos comandos a cada push e pull request na `main`.

## Documentação
Diagramas UML (casos de uso, classes, sequência), mapa mental, MER/DER e fluxogramas
estão em [`docs/`](docs/README.md).