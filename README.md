# Chain Patterns with LangChain

Este repositório contém implementações de padrões de encadeamento (Chain Patterns) utilizando LangChain para aplicações de Inteligência Artificial Generativa.

## Índice

1. [Prompt Template Pattern](#prompt-template-pattern)
2. [Sequential Chain Pattern](#sequential-chain-pattern)

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
│   ├── prompt_template/         # Prompt Template Pattern
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── chain.py
│   └── sequential_chain/       # Sequential Chain Pattern
│       ├── __init__.py
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
