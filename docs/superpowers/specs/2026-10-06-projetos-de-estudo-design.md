# Repositório ProjetosDeEstudo — Especificação

**Data:** 2026-10-06

**Status:** Aguardando revisão do usuário

## Objetivo

Criar um repositório público no GitHub chamado `ProjetosDeEstudo` para reunir pequenos projetos independentes em subpastas. O projeto existente `AgendadorDeTarefas` será o primeiro subprojeto.

## Estrutura aprovada

Usar a pasta já existente `~/Documentos/ProjetosDeEstudo/` como raiz do repositório, mantendo o agendador em `AgendadorDeTarefas/`. O diretório Git que atualmente está dentro do agendador será promovido à raiz maior, evitando um repositório Git aninhado.

```text
ProjetosDeEstudo/
├── .git/
├── .gitignore
└── AgendadorDeTarefas/
    ├── backend/
    └── ...
```

O diretório do projeto e seus arquivos locais serão preservados. O repositório atual não tem commits nem remoto configurado.

## Proteção de dados e segurança

- Não criar nem editar arquivos README; o usuário cuidará dessa documentação.
- Manter na raiz um `.gitignore` que exclua ambientes virtuais, caches Python, arquivos `.env` e bancos SQLite locais. O `db.sqlite3` existente permanece no computador, mas não será publicado.
- O projeto Django contém uma `SECRET_KEY` fixa, marcada como insegura para desenvolvimento. Substituí-la por leitura da variável de ambiente `DJANGO_SECRET_KEY`; informar ao usuário como defini-la na conclusão, sem editar README. Não incluir o valor atual no GitHub.
- Preservar os arquivos do projeto, incluindo o README já existente, sem alterações de documentação.

## Publicação

Após a organização, verificar o projeto e conferir que banco, ambiente virtual, caches e segredos não estão no conjunto de arquivos a publicar. Criar um commit inicial na branch `main`, criar `ProjetosDeEstudo` como repositório público na conta GitHub do usuário e enviar o commit para o remoto `origin`.

Se não houver autenticação GitHub disponível no ambiente, interromper antes da criação/publicação remota e informar o bloqueio.

## Verificação e critérios de aceite

1. `ProjetosDeEstudo` é a raiz do único repositório Git local, com `AgendadorDeTarefas/` como subpasta.
2. `db.sqlite3`, `.venv`, caches e arquivos `.env` não são rastreados nem publicados.
3. Django obtém `DJANGO_SECRET_KEY` do ambiente.
4. O comando de verificação do Django termina sem erros.
5. O repositório GitHub público `ProjetosDeEstudo` existe, possui o commit inicial na branch `main`, e o remoto local `origin` aponta para ele.

## Fora de escopo

- Alterar funcionalidades, modelos, endpoints ou a arquitetura interna do agendador.
- Corrigir outros problemas de código que não sejam necessários para a verificação básica ou para evitar a publicação da chave fixa.
- Remover o banco local, o ambiente virtual ou qualquer arquivo do projeto.
