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
│   ├── main.py              # Entry point
│   └── prompt_template/
│       ├── __init__.py      # Exports públicos
│       ├── prompts.py       # Definição de templates
│       └── chain.py         # Configuração das chains
├── .env.example             # Variáveis de ambiente
├── pyproject.toml           # Configuração Poetry
└── README.md                # Documentação
```

## Instalação e Uso

```bash
# Instalar dependências
poetry install

# Executar
poetry run prompt-template

# Ou diretamente
python src/main.py
```
