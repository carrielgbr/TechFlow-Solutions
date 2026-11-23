# Documentação do TechFlow Tasks

Diagramas do sistema escritos em Markdown com [Mermaid](https://mermaid.js.org/).
O GitHub renderiza os diagramas automaticamente ao abrir cada arquivo.

| Documento | Conteúdo |
|---|---|
| [Mapa mental](mapa-mental.md) | Visão geral do sistema: funcionalidades, arquitetura, dados, qualidade e metodologia |
| [Casos de uso (UML)](casos-de-uso.md) | Ator, casos de uso e descrição de cada um |
| [Diagrama de classes (UML)](diagrama-de-classes.md) | Classe `Tarefa`, módulos `database` e `app`, e diagrama de sequência |
| [MER e DER](mer-der.md) | Modelo conceitual, modelo lógico/físico e dicionário de dados do SQLite |
| [Fluxogramas](fluxogramas.md) | Fluxo de navegação, fluxo de cada operação, estados da tarefa e pipeline de CI |

## Como visualizar fora do GitHub

- **VS Code:** instale a extensão *Markdown Preview Mermaid Support* e abra o preview (`Ctrl+Shift+V`).
- **Online:** copie o bloco `mermaid` para o [Mermaid Live Editor](https://mermaid.live) e exporte em PNG/SVG.
