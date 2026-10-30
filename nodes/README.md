# nodes — estudos de LangGraph

Exemplos de **grafos de estado** com LangGraph + LangChain + Ollama, evoluindo do
mais simples até um caso com validação automática em loop.

Cada arquivo é um script independente: define o estado, os nós, monta o grafo e
roda um chat no terminal.

## Os arquivos, em ordem de evolução

| Arquivo | Grafo | O que muda em relação ao anterior |
|---------|-------|-----------------------------------|
| `test.py` | `START → a → b → c → END` | Primeira versão. O estado guarda `prompt` e `answer`. O nó `c` só devolve o prompt como `HumanMessage` no histórico. |
| `test1.py` | `START → a → b → c → END` | Mesma estrutura, mas o `HumanMessage` da pergunta passa a ser enviado já no `invoke`, em vez de ser criado no fim pelo nó `c`. |
| `test2.py` | `START → a ⇄ b` (b decide quando parar) | O nó `c` desaparece. `a` passa a usar o histórico completo (`messages`) como contexto do LLM, e a pergunta entra no histórico direto no `invoke`. |

## O que cada nó faz

- **`node_a`** — conversa com o modelo (`ChatOllama`, `llama3.2:3b`) e devolve a
  resposta no estado.
- **`node_b`** — validador. Um `SystemMessage` manda a IA responder só `YES` ou
  `NO` + justificativa, e o código decide o próximo passo conforme esse retorno.
  É o exemplo mais claro de *roteamento condicional* do LangGraph.
- **`node_c`** — só existe em `test.py` / `test1.py`; acrescenta a pergunta do
  usuário ao histórico de mensagens.

## Como rodar

Precisa de [uv](https://docs.astral.sh/uv/) e do [Ollama](https://ollama.com/)
rodando localmente com o modelo `llama3.2:3b`:

```bash
ollama pull llama3.2:3b
uv run python nodes/test2.py
```

Para sair do chat digite `quit`, `q`, `end` ou `exit`.

## Conceitos que aparecem aqui

- **`AgentState` como `TypedDict`** — o "formato" dos dados que circulam entre os
  nós. Todo nó recebe o estado e devolve só as chaves que quer atualizar.
- **`Annotated[Sequence[BaseMessage], add_messages]`** — o reducer. Sem ele, cada
  nó sobrescreveria a lista de mensagens; com ele, as mensagens são **concatenadas**.
- **`StateGraph` + `add_conditional_edges`** — a aresta condicional chama uma
  função que retorna o nome do próximo nó. Se a função retornar `"__end__"`, o
  grafo termina.
- **`InMemorySaver` + `thread_id`** — checkpointer que guarda o estado da conversa
  em memória entre chamadas do `invoke`, permitindo histórico multi-turno dentro
  da mesma thread.

## Pendências conhecidas

- **Loop sem limite em `test2.py`**: quando o validador responde `NO`, o grafo
  volta para `node_a`, mas `node_a` reenvia o mesmo contexto — a IA tende a repetir
  a resposta e o loop não termina. Uma saída seria contar tentativas no estado e
  cortar depois de N, ou passar a justificativa do validador para o próximo turno.
- **Imports não usados** (`sqlite3`, `init_chat_model`, `Markdown`) herdados de
  autocomplete. Inofensivos, mas sujam a leitura.
- As f-strings usam aspas aninhadas (`f"{result["answer"]}"`), o que exige
  **Python 3.12+**.
