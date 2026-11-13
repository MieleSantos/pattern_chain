# Chain Patterns with LangChain

Implementações em Python de padrões para construir aplicações com LLMs usando [LangChain](https://docs.langchain.com/oss/python/langchain) e [LangGraph](https://docs.langchain.com/oss/python/langgraph), do primeiro prompt template a um RAG conversacional com memória.

Cada padrão tem um tutorial passo a passo na trilha **[Engenharia de Prompt](https://miele.dev.br/tutoriais/engenharia-de-prompt.html)**, no site [miele.dev.br](https://miele.dev.br/).

## Padrões

| # | Padrão | O que mostra | Executar | Tutorial |
|---|--------|--------------|----------|----------|
| 1 | [Prompt Template](#prompt-template-pattern) | Prompts reutilizáveis com variáveis e a primeira chain LCEL | `python src/main.py` | [Parte 1](https://miele.dev.br/tutoriais/prompt-template-pattern.html) |
| 2 | [Sequential Chain](#sequential-chain-pattern) | Etapas em sequência: traduzir → resumir → analisar sentimento | `python src/main_sequential.py` | [Parte 2](https://miele.dev.br/tutoriais/sequential-chain-pattern.html) |
| 3 | [Structured Output](#structured-output-pattern) | Resposta como objeto Pydantic validado (triagem de tickets) | `python src/main_structured.py` | [Parte 3](https://miele.dev.br/tutoriais/structured-output-pattern.html) |
| 4 | [Router Chain](#router-chain-pattern) | Classificar e mandar cada pedido para a chain especializada | `python src/main_router.py` | [Parte 4](https://miele.dev.br/tutoriais/router-chain-pattern.html) |
| 5 | [Parallel Chain](#parallel-chain-pattern) | Etapas independentes ao mesmo tempo com `RunnableParallel` | `python src/main_parallel.py` | [Parte 5](https://miele.dev.br/tutoriais/parallel-chain-pattern.html) |
| 6 | [Few-Shot Prompting](#few-shot-prompting-pattern) | Exemplos no prompt, fixos ou escolhidos por semelhança | `python src/main_few_shot.py` | [Parte 6](https://miele.dev.br/tutoriais/few-shot-prompting.html) |
| 7 | [RAG](#rag-pattern) | Respostas a partir de documentos, com fontes e "não encontrei" | `python src/main_rag.py` | [Parte 7](https://miele.dev.br/tutoriais/rag.html) |
| 8 | [Memory](#memory-pattern) | Histórico de conversa com LangGraph e RAG conversacional | `python src/main_memory.py` | [Parte 8](https://miele.dev.br/tutoriais/memoria-historico.html) |
| 9 | [Chain-of-Thought e Reflection](#chain-of-thought-and-reflection-patterns) | Raciocínio antes da resposta e um ciclo de revisão com limite | `python src/main_cot_reflection.py` | [Parte 9](https://miele.dev.br/tutoriais/chain-of-thought-reflection.html) |
| 10 | [Map-Reduce](#map-reduce-pattern) | Processar em lotes um texto que não cabe num prompt e consolidar | `python src/main_map_reduce.py` | [Parte 10](https://miele.dev.br/tutoriais/map-reduce.html) |
| 11 | [Fallback e Retry](#fallback-and-retry-patterns) | Novas tentativas, modelo reserva e mensagem segura quando tudo falha | `python src/main_fallback_retry.py` | [Parte 11](https://miele.dev.br/tutoriais/fallback-retry.html) |

## Pré-requisitos

- Python 3.12 ou superior
- [Poetry](https://python-poetry.org/)
- Uma chave da API do Gemini ([Google AI Studio](https://aistudio.google.com/apikey))

## Instalação

```bash
git clone https://github.com/MieleSantos/pattern_chain.git
cd pattern_chain
poetry install
```

## Configuração

Copie o arquivo de exemplo e preencha a sua chave:

```bash
cp .env.example .env
```

```env
GOOGLE_API_KEY=sua_chave_aqui
```

Todos os exemplos usam o Gemini (`gemini-2.5-flash` para o chat e `gemini-embedding-001` para os embeddings dos padrões 6, 7 e 8). Cada `main_*.py` carrega o `.env` sozinho.

## Como executar

Rode qualquer exemplo a partir da raiz do projeto, dentro do ambiente do Poetry:

```bash
poetry run python src/main_rag.py
```

Se preferir, ative o ambiente do Poetry uma vez e rode direto `python src/main_<padrão>.py`.

## Estrutura do Projeto

```
pattern_chain/
├── src/
│   ├── main.py                  # 1. Prompt Template
│   ├── main_sequential.py       # 2. Sequential Chain
│   ├── main_structured.py       # 3. Structured Output
│   ├── main_router.py           # 4. Router Chain
│   ├── main_parallel.py         # 5. Parallel Chain
│   ├── main_few_shot.py         # 6. Few-Shot Prompting
│   ├── main_rag.py              # 7. RAG
│   ├── main_memory.py           # 8. Memory
│   ├── main_cot_reflection.py   # 9. Chain-of-Thought e Reflection
│   ├── main_map_reduce.py       # 10. Map-Reduce
│   ├── main_fallback_retry.py   # 11. Fallback e Retry
│   ├── prompt_template/         # prompts.py, chain.py
│   ├── sequential_chain/        # prompts.py, chain.py
│   ├── structured_output/       # schemas.py, prompts.py, chain.py
│   ├── router_chain/            # prompts.py, chain.py
│   ├── parallel_chain/          # prompts.py, chain.py
│   ├── few_shot/                # examples.py, prompts.py, chain.py
│   ├── rag/                     # indexing.py, prompts.py, chain.py
│   ├── memory/                  # prompts.py, graph.py
│   ├── cot_reflection/          # schemas.py, prompts.py, chain.py, graph.py
│   ├── map_reduce/              # schemas.py, prompts.py, chain.py
│   └── fallback_retry/          # prompts.py, chain.py, simulate.py
├── data/
│   ├── nuvem/                   # Base de conhecimento dos padrões 7, 8 e 9 (cobrança, cancelamento, nota fiscal, integrações)
│   └── tickets/                 # Tickets fictícios de uma semana (padrão 10)
├── .env.example
├── pyproject.toml
└── README.md
```

Cada pacote segue a mesma organização: `prompts.py` com os templates, `chain.py` (ou `graph.py`) montando a chain, e um `main_*.py` como ponto de entrada.

## Sobre os exemplos

- Os padrões 3 a 11 usam o mesmo cenário: o suporte da **Nuvem**, uma empresa SaaS fictícia. Os documentos em `data/nuvem/` também são fictícios.
- As funções que montam as chains aceitam o modelo (e, quando há busca, os embeddings ou o retriever) como parâmetro. Assim dá para trocar de provedor ou testar com modelos falsos, sem chamar a API.
- A memória (padrão 8) usa a persistência do LangGraph, porque o `RunnableWithMessageHistory` está obsoleto no LangChain 1.x.
- O padrão 9 não usa embeddings: a base é pequena e vai inteira no prompt.
- O arquivo de tickets do padrão 10 é pequeno de propósito. O exemplo usa um limite baixo por prompt (`max_chars=800`) para forçar vários lotes.
- O padrão 11 simula as falhas (`fallback_retry/simulate.py`), para mostrar cada camada sem depender de uma queda real do provedor.

---

# Prompt Template Pattern

O **Prompt Template Pattern** é um padrão de design utilizado em aplicações de Inteligência Artificial Generativa para criar prompts reutilizáveis e dinâmicos. Ele permite separar a estrutura fixa do prompt das variáveis que serão preenchidas em tempo de execução.

## Conceito

Em vez de escrever prompts como strings fixas, você define um template com placeholders (variáveis) que podem ser substituídos dinamicamente. Isso traz diversos benefícios:

- **Reutilização**: O mesmo template pode ser usado com diferentes valores
- **Manutenção**: Alterações no formato do prompt precisam ser feitas em um único lugar
- **Type Safety**: Possibilidade de validar os parâmetros esperados
- **Composição**: Templates podem ser combinados e aninhados

## Exemplo de Implementação

```python
from langchain_core.prompts import ChatPromptTemplate

# Definindo o template com variáveis entre chaves
system = ("system", "you are an assistant that answers questions in a {style} style")
user = ("user", "{question}")

# Criando o ChatPromptTemplate
chat_prompt = ChatPromptTemplate.from_messages([system, user])

# Formatando com valores específicos
messages = chat_prompt.format_messages(style="funny", question="Who is Alan Turing?")
```

## Usando com LCEL (LangChain Expression Language)

O padrão se integra perfeitamente com a composição de cadeias (chains) da LangChain:

```python
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
parser = StrOutputParser()

chain = chat_prompt | llm | parser

result = chain.invoke(
    {"style": "formal", "question": "What is Chain in Generative AI?"}
)
```

## Benefícios Principais

| Benefício | Descrição |
|-----------|-----------|
| **Flexibilidade** | Altere o tom, contexto ou instruções sem alterar o código |
| **Testabilidade** | Teste diferentes variações de prompts facilmente |
| **Organização** | Mantém prompts complexos legíveis e estruturados |
| **Separação de Concerns** | Separa a lógica do prompt da lógica de negócio |

## Boas Práticas

1. **Nomeie variáveis claramente**: Use nomes descritivos como `{user_question}` ou `{context}`
2. **Documente o template**: Explique o propósito e os valores esperados
3. **Valide inputs**: Garanta que os parâmetros fornecidos são válidos
4. **Use system messages**: Defina o comportamento do assistente de forma clara

## Executando

```bash
python src/main.py
```

---

# Sequential Chain Pattern

O **Sequential Chain Pattern** é um padrão onde múltiplas operações são executadas em sequência, onde a saída de cada etapa torna-se a entrada da próxima. Isso permite criar pipelines de processamento complexos.

## Conceito

Em vez de uma única chamada ao modelo, você encadeia múltiplas operações:
1. A saída da primeira operação alimenta a segunda
2. Cada etapa pode ter seu próprio prompt e lógica
3. O resultado final agrega todas as transformações

## Exemplo de Implementação

```python
from langchain_core.prompts import ChatPromptTemplate

# Prompt para tradução
translate_prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate to {target_language}"),
    ("user", "{text}")
])

# Prompt para resumo
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the following text"),
    ("user", "{text}")
])

# Encadeando as operações
translate_chain = translate_prompt | llm | parser
summary_chain = summary_prompt | llm | parser

def sequential_chain(input_dict):
    translated = translate_chain.invoke({
        "target_language": input_dict["language"],
        "text": input_dict["text"]
    })
    summary = summary_chain.invoke({"text": translated})
    return {"translated": translated, "summary": summary}
```

## Executando

```bash
python src/main_sequential.py
```

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Pipeline Complexo** | Combine múltiplas operações em uma única execução |
| **Reutilização** | Cada etapa pode ser reutilizada independentemente |
| **Debugging** | Possibilidade de inspecionar saída de cada etapa |
| **Flexibilidade** | Adicione ou remova etapas facilmente |

---

# Structured Output Pattern

O **Structured Output Pattern** faz o modelo devolver um objeto com campos e tipos definidos, em vez de texto livre. Você descreve o formato com um modelo Pydantic e recebe uma instância validada, pronta para usar no código ou numa API.

## Conceito

1. O schema (Pydantic) define os campos, os tipos e os valores permitidos
2. A descrição de cada campo é enviada ao modelo e funciona como instrução
3. `with_structured_output` devolve o objeto já validado: não há parser de texto

## Exemplo de Implementação

```python
from typing import Literal
from pydantic import BaseModel, Field


class TicketAnalysis(BaseModel):
    """Triage of a customer support message."""

    category: Literal["billing", "technical", "cancellation", "question"] = Field(
        description="Main subject of the message"
    )
    priority: Literal["low", "medium", "high"] = Field(
        description="high when the customer is blocked or losing money"
    )
    summary: str = Field(description="One-sentence summary of the request, in Portuguese")
    needs_human: bool = Field(
        description="True when the request cannot be solved by an automatic answer"
    )


structured_llm = llm.with_structured_output(TicketAnalysis)
chain = create_ticket_prompt() | structured_llm

ticket = chain.invoke({"message": "Fui cobrado duas vezes na fatura de outubro"})
ticket.category   # "billing"
ticket.priority   # "high"
```

## Tratando saídas inválidas

Com `include_raw=True`, a chain não lança exceção quando a resposta não segue o schema. Ela devolve um dict com `raw` (a mensagem original), `parsed` (o objeto ou `None`) e `parsing_error`:

```python
chain = create_structured_chain(include_raw=True)
result = chain.invoke({"message": "..."})

if result["parsing_error"]:
    ...  # registrar, tentar de novo ou usar um valor padrão
else:
    ticket = result["parsed"]
```

## Executando

```bash
python src/main_structured.py
```

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Contrato claro** | O formato da resposta é definido por código, não por texto no prompt |
| **Validação** | Tipos e valores permitidos são verificados pelo Pydantic |
| **Integração** | O objeto vai direto para regras de negócio, banco de dados ou resposta de API |
| **Base para roteamento** | Campos como `category` permitem decidir o próximo passo do fluxo |

---

# Router Chain Pattern

O **Router Chain Pattern** classifica a entrada e manda cada pedido para a chain especializada naquele assunto. Em vez de um prompt genérico que tenta responder tudo, cada rota tem o seu próprio prompt.

## Conceito

1. Uma etapa de classificação decide o tipo do pedido (aqui, o `TicketAnalysis` do Structured Output)
2. Uma função de roteamento escolhe qual chain executar
3. A chain escolhida responde, e as outras não são executadas

## Exemplo de Implementação

```python
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

routes = create_routes(llm)  # {"billing": ..., "technical": ..., ...}


def route(state):
    ticket = state["ticket"]
    if ticket.priority == "high" and ticket.needs_human:
        return escalate
    return routes.get(ticket.category, routes["question"])


chain = (
    RunnablePassthrough.assign(ticket=classify)
    | RunnablePassthrough.assign(answer=RunnableLambda(route))
)
```

Quando a função passada ao `RunnableLambda` devolve outra chain, o LangChain executa essa chain com a mesma entrada. O pacote também traz `create_branch_router_chain`, o mesmo roteador escrito com `RunnableBranch`, para comparação.

## Executando

```bash
python src/main_router.py
```

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Prompts especializados** | Cada assunto tem instruções próprias, mais curtas e precisas |
| **Custo** | Só a rota escolhida é executada |
| **Regras de negócio** | Casos críticos podem ir para uma rota sem LLM, como o encaminhamento a um atendente |
| **Evolução** | Uma nova categoria vira uma nova rota, sem mexer nas outras |

---

# Parallel Chain Pattern

O **Parallel Chain Pattern** executa ao mesmo tempo etapas que não dependem umas das outras. Todas recebem a mesma entrada, e o resultado é um dicionário com a saída de cada uma.

## Conceito

1. Identifique as etapas que só dependem da mesma entrada
2. Agrupe essas etapas num `RunnableParallel` (ou num dict dentro da chain)
3. O tempo total passa a ser o da etapa mais lenta, não a soma de todas

## Exemplo de Implementação

```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

analyses = RunnableParallel(
    summary=create_summary_prompt() | llm | parser,
    sentiment=create_sentiment_prompt() | llm | parser,
    keywords=create_keywords_prompt() | llm | parser,
)

chain = (
    RunnablePassthrough.assign(translated=translate)
    | RunnablePassthrough.assign(
        analysis={"text": itemgetter("translated")} | analyses
    )
)
```

A tradução continua sequencial, porque as análises dependem dela. Depois disso, resumo, sentimento e palavras-chave rodam juntos.

## Executando

```bash
python src/main_parallel.py
```

Use `config={"max_concurrency": N}` para limitar quantas chamadas rodam ao mesmo tempo, por exemplo para respeitar o rate limit do provedor.

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Latência** | Com um modelo falso de 0,5 s por chamada: 2,0 s em sequência, 1,0 s com as análises em paralelo |
| **Composição** | Combina com etapas sequenciais na mesma chain |
| **Async** | `ainvoke` também executa os ramos em paralelo |
| **Controle** | `max_concurrency` limita as chamadas simultâneas |

---

# Few-Shot Prompting Pattern

O **Few-Shot Prompting Pattern** coloca exemplos de entrada e saída dentro do prompt para mostrar ao modelo o tom, o tamanho e a estrutura esperados. Funciona melhor que descrever o estilo em regras, porque o modelo imita o que vê.

## Conceito

1. Escreva alguns pares de exemplo (mensagem do cliente e a resposta ideal)
2. Os exemplos entram no prompt como turnos de conversa (humano → IA)
3. Com muitos exemplos, um seletor escolhe só os mais parecidos com a mensagem nova

## Exemplo de Implementação

```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

example_prompt = ChatPromptTemplate.from_messages(
    [("human", "{message}"), ("ai", "{reply}")]
)

few_shot = FewShotChatMessagePromptTemplate(
    examples=EXAMPLES,
    example_prompt=example_prompt,
)

prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM), few_shot, ("human", "{message}")]
)
```

## Seleção dinâmica

```python
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

selector = SemanticSimilarityExampleSelector.from_examples(
    EXAMPLES,
    GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),
    InMemoryVectorStore,
    k=2,
    input_keys=["message"],
)

few_shot = FewShotChatMessagePromptTemplate(
    example_selector=selector,
    example_prompt=example_prompt,
    input_variables=["message"],
)
```

## Executando

```bash
python src/main_few_shot.py
```

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Estilo consistente** | O modelo copia tom, tamanho e estrutura dos exemplos |
| **Menos regras no prompt** | Um exemplo substitui vários parágrafos de instrução |
| **Contexto enxuto** | A seleção dinâmica envia só os exemplos relevantes (6 mensagens em vez de 14 no exemplo) |
| **Fácil de evoluir** | Melhorar a resposta é editar um exemplo, não reescrever o prompt |

---

# RAG Pattern

O **RAG (Retrieval-Augmented Generation)** busca os trechos relevantes de uma base de documentos e coloca esses trechos no prompt. O modelo responde com base no que foi encontrado, e não no que "lembra" do treinamento.

## Conceito

**Indexação** (uma vez, ou quando os documentos mudam):
1. Carregar os documentos (`data/nuvem/*.md`)
2. Dividir em trechos, primeiro por cabeçalho e depois por tamanho
3. Gerar embeddings e guardar numa base vetorial

**Consulta** (a cada pergunta):
1. Buscar os `k` trechos mais parecidos com a pergunta
2. Montar o prompt com esses trechos como contexto
3. Gerar a resposta, citando as fontes

## Exemplo de Implementação

```python
retriever = create_retriever(k=3)  # carrega, divide, indexa

chain = (
    RunnablePassthrough.assign(docs=itemgetter("question") | retriever)
    | RunnablePassthrough.assign(answer=to_prompt_input | prompt | llm | parser)
)

result = chain.invoke({"question": "Em quanto tempo recebo o estorno?"})
result["answer"]   # resposta baseada em cobranca.md
result["sources"]  # ["cobranca.md > Cobrança em duplicidade", ...]
```

O prompt instrui o modelo a usar só a documentação e a responder "Não encontrei essa informação na documentação." quando a resposta não estiver lá.

## Executando

```bash
python src/main_rag.py
```

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Respostas atualizadas** | Mudou a política? Atualize o documento, não o prompt nem o modelo |
| **Menos invenção** | O modelo responde a partir de trechos reais e admite quando não sabe |
| **Rastreabilidade** | Cada resposta vem com os trechos usados como contexto |
| **Escala** | Só os trechos relevantes vão para o prompt, não a base inteira |

---

# Memory Pattern

O **Memory Pattern** faz a aplicação lembrar a conversa. A cada mensagem, o histórico daquela conversa volta para o prompt, e o modelo entende perguntas de acompanhamento como "e se eu tiver pago com Pix?".

## Conceito

1. O histórico fica no estado de um grafo do LangGraph (`MessagesState`)
2. Um checkpointer salva o estado depois de cada execução, separado por `thread_id`
3. Só as últimas mensagens vão para o prompt (`trim_messages`), mas o histórico completo continua salvo
4. No RAG, a pergunta de acompanhamento é reescrita como uma pergunta completa antes da busca

> O `RunnableWithMessageHistory` e o `InMemoryChatMessageHistory` estão obsoletos no LangChain 1.x. A recomendação atual é a persistência do LangGraph, usada aqui.

## Exemplo de Implementação

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, END, MessagesState, StateGraph


def respond(state: MessagesState) -> dict:
    history, question = state["messages"][:-1], state["messages"][-1].content
    answer = chain.invoke({"history": trim_history(history), "question": question})
    return {"messages": [AIMessage(answer)]}


graph = StateGraph(MessagesState)
graph.add_node("respond", respond)
graph.add_edge(START, "respond")
graph.add_edge("respond", END)
app = graph.compile(checkpointer=InMemorySaver())

app.invoke(
    {"messages": [HumanMessage("E se eu tiver pago com Pix?")]},
    config={"configurable": {"thread_id": "cliente-1"}},
)
```

O RAG conversacional (`create_conversational_rag_graph`) tem três nós: `condense` (reescreve a pergunta), `retrieve` (busca) e `answer` (responde com documentação + histórico).

## Executando

```bash
python src/main_memory.py
```

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Perguntas de acompanhamento** | "E no Pix?" funciona porque o histórico dá o contexto |
| **Conversas isoladas** | Cada `thread_id` tem o seu histórico |
| **Custo controlado** | Só as últimas mensagens vão para o prompt |
| **Pronto para produção** | Troque o `InMemorySaver` por um checkpointer com banco (como Postgres) sem mudar o grafo |

---

# Chain-of-Thought and Reflection Patterns

Dois padrões para melhorar a qualidade da resposta em perguntas que combinam várias regras. O **Chain-of-Thought** faz o modelo raciocinar antes de responder. O **Reflection** faz uma segunda chamada revisar a resposta e pedir correções.

## Conceito

1. **Chain-of-Thought:** o raciocínio é um campo do structured output, antes da resposta. O código registra o raciocínio e mostra só a resposta
2. **Reflection:** um grafo do LangGraph com três nós: `draft` (rascunho), `review` (revisão contra a documentação) e `revise` (reescrita)
3. Uma aresta condicional volta de `review` para `revise` enquanto houver problemas
4. `max_revisions` limita o ciclo. Se o limite acabar com problemas em aberto, o caso vai para uma pessoa

> Modelos com raciocínio embutido, como o `gemini-2.5-flash`, já pensam antes de responder. O raciocínio no structured output continua útil porque fica registrado e pode ser auditado.

## Exemplo de Implementação

```python
class ReasonedAnswer(BaseModel):
    reasoning: str = Field(description="Step-by-step reasoning ...")  # vem antes
    answer: str = Field(description="Final answer to the customer ...")


cot_chain = create_cot_prompt() | llm.with_structured_output(ReasonedAnswer)
```

```python
def after_review(state: ReflectionState) -> str:
    if state["critique"].approved or state["revisions"] >= max_revisions:
        return END
    return "revise"


graph = StateGraph(ReflectionState)
graph.add_node("draft", draft)
graph.add_node("review", review)
graph.add_node("revise", revise)
graph.add_edge(START, "draft")
graph.add_edge("draft", "review")
graph.add_conditional_edges("review", after_review, ["revise", END])
graph.add_edge("revise", "review")
app = graph.compile()

state = app.invoke({"question": "Contratei o plano anual há 20 dias. Se eu cancelar, recebo reembolso?"})
state["answer"], state["revisions"], state["critique"].approved
```

## Executando

```bash
python src/main_cot_reflection.py
```

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Menos erros em perguntas com várias regras** | O modelo lista os fatos e as regras antes de concluir |
| **Raciocínio auditável** | O `reasoning` fica no log, separado da resposta do cliente |
| **Erros pegos antes do cliente** | O revisor confere cada afirmação com a documentação |
| **Custo previsível** | Com `max_revisions=2`, são no máximo 6 chamadas ao modelo por pergunta |

---

# Map-Reduce Pattern

O **Map-Reduce Pattern** processa um texto que não cabe num prompt só. O texto é dividido em lotes, cada lote é processado separadamente (*map*) e os resultados são combinados numa resposta (*reduce*).

## Conceito

1. **Dividir:** o arquivo vira uma lista de tickets, e os tickets são agrupados em lotes de até `max_chars` caracteres, sem cortar nenhum no meio
2. **Map:** uma chamada por lote, em paralelo (`batch` com `max_concurrency`). A saída é estruturada: uma nota por ticket, com categoria de uma lista fechada
3. **Collapse:** se as notas somadas ainda não cabem num prompt, elas são condensadas em grupos, quantas vezes for preciso
4. **Reduce:** os totais por categoria são contados no código (`Counter`). O modelo só escreve o relatório

## Exemplo de Implementação

```python
batches = group_texts(tickets, max_chars)

map_chain = create_map_prompt() | llm.with_structured_output(BatchNotes)
results = map_chain.batch(
    [{"text": batch} for batch in batches],
    config={"max_concurrency": 4},
)
notes = [note for result in results for note in result.notes]

totals = dict(Counter(note.category for note in notes).most_common())  # conta no código
report = reduce_chain.invoke({"totals": ..., "notes": ...})            # o modelo escreve
```

## Executando

```bash
python src/main_map_reduce.py
```

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Sem limite de tamanho** | O texto é processado em lotes que cabem no prompt |
| **Mais rápido** | Os lotes não dependem uns dos outros e rodam em paralelo |
| **Totais confiáveis** | Contagem feita no código, com categorias de uma lista fechada |
| **Falha isolada** | Um lote com erro pode ser repetido sem refazer os outros |

---

# Fallback and Retry Patterns

Os padrões de **Retry** e **Fallback** mantêm a chain respondendo quando uma chamada ao modelo falha: limite de requisições, timeout ou provedor fora do ar.

## Conceito

Três camadas, de dentro para fora:

1. **Retry:** tentar de novo no mesmo modelo, com espera crescente entre as tentativas (`with_retry`)
2. **Fallback:** trocar de modelo quando as tentativas acabam (`with_fallbacks`)
3. **Mensagem segura:** um texto fixo quando todos os modelos falham, para o cliente nunca receber um erro

> Repita só erros transitórios. Um erro de chave inválida vai falhar em todas as tentativas. Passe em `retry_on` as exceções de limite, timeout e servidor do seu provedor.

## Exemplo de Implementação

```python
def retrying(model):
    return model.with_retry(
        stop_after_attempt=3,
        retry_if_exception_type=retry_on,
        wait_exponential_jitter=True,
    )


model = retrying(primary).with_fallbacks([retrying(fallback)])
chain = create_support_prompt() | model | StrOutputParser()
chain = chain.with_fallbacks([RunnableLambda(lambda _: SAFE_MESSAGE)])
```

Saída estruturada inválida também é falha. `create_validated_ticket_chain` repete a chamada do padrão 3 quando o resultado não passa na validação.

## Executando

```bash
python src/main_fallback_retry.py
```

O exemplo simula quatro cenários: tudo funcionando, modelo principal falhando duas vezes, principal fora do ar e os dois modelos fora do ar.

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Falhas passageiras somem** | Limite de requisições e timeouts se resolvem com uma nova tentativa |
| **Sem ponto único de falha** | Um segundo modelo assume quando o primeiro não volta |
| **O cliente nunca vê um erro** | A mensagem segura é texto fixo e não depende de nenhum modelo |
| **Custo máximo conhecido** | Com 3 tentativas por modelo, são no máximo 6 chamadas por pergunta |
