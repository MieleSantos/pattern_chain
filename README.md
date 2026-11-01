# Chain Patterns with LangChain

Este repositório contém implementações de padrões de encadeamento (Chain Patterns) utilizando LangChain para aplicações de Inteligência Artificial Generativa.

## Índice

1. [Prompt Template Pattern](#prompt-template-pattern)
2. [Sequential Chain Pattern](#sequential-chain-pattern)
3. [Structured Output Pattern](#structured-output-pattern)
4. [Router Chain Pattern](#router-chain-pattern)
5. [Parallel Chain Pattern](#parallel-chain-pattern)
6. [Few-Shot Prompting Pattern](#few-shot-prompting-pattern)
7. [RAG Pattern](#rag-pattern)
8. [Memory Pattern](#memory-pattern)

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
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4")
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

## Estrutura do Projeto

```
pattern_chain/
├── src/
│   ├── main.py                  # Entry point - Prompt Template
│   ├── main_sequential.py       # Entry point - Sequential Chain
│   ├── main_structured.py       # Entry point - Structured Output
│   ├── main_router.py           # Entry point - Router Chain
│   ├── main_parallel.py         # Entry point - Parallel Chain
│   ├── main_few_shot.py         # Entry point - Few-Shot Prompting
│   ├── main_rag.py              # Entry point - RAG
│   ├── main_memory.py           # Entry point - Memory
│   ├── prompt_template/         # Prompt Template Pattern
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── chain.py
│   ├── sequential_chain/       # Sequential Chain Pattern
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── chain.py
│   ├── router_chain/           # Router Chain Pattern
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── chain.py
│   ├── parallel_chain/         # Parallel Chain Pattern
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── chain.py
│   ├── few_shot/               # Few-Shot Prompting Pattern
│   │   ├── __init__.py
│   │   ├── examples.py
│   │   ├── prompts.py
│   │   └── chain.py
│   ├── rag/                    # RAG Pattern
│   │   ├── __init__.py
│   │   ├── indexing.py
│   │   ├── prompts.py
│   │   └── chain.py
│   ├── memory/                 # Memory Pattern (LangGraph)
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── graph.py
│   └── structured_output/      # Structured Output Pattern
│       ├── __init__.py
│       ├── schemas.py
│       ├── prompts.py
│       └── chain.py
├── data/
│   └── nuvem/                  # Base de conhecimento usada no RAG
├── .env.example
├── pyproject.toml
└── README.md
```

## Instalação e Uso

```bash
# Instalar dependências
poetry install

# Executar Prompt Template Pattern
python src/main.py

# Executar Sequential Chain Pattern
python src/main_sequential.py
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

## Estrutura do Projeto - Sequential Chain

```
src/
├── main_sequential.py        # Entry point
└── sequential_chain/
    ├── __init__.py          # Exports públicos
    ├── prompts.py           # Definição de templates
    └── chain.py            # Configuração das chains
```

## Instalação e Uso

```bash
# Executar Sequential Chain
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

