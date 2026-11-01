# Chain Patterns with LangChain

Este repositório contém implementações de padrões de encadeamento (Chain Patterns) utilizando LangChain para aplicações de Inteligência Artificial Generativa.

## Índice

1. [Prompt Template Pattern](#prompt-template-pattern)
2. [Sequential Chain Pattern](#sequential-chain-pattern)
3. [Structured Output Pattern](#structured-output-pattern)

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
│   ├── prompt_template/         # Prompt Template Pattern
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── chain.py
│   ├── sequential_chain/       # Sequential Chain Pattern
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── chain.py
│   └── structured_output/      # Structured Output Pattern
│       ├── __init__.py
│       ├── schemas.py
│       ├── prompts.py
│       └── chain.py
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

