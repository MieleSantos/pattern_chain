"""
Chain configuration for Prompt Template Pattern.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model


def create_chain(prompt: ChatPromptTemplate, model_name: str = "gemini-2.5-flash", model_provider: str = "google_genai"):
    """Create a LCEL chain with prompt, model and parser."""
    llm = init_chat_model(model=model_name, model_provider=model_provider)
    parser = StrOutputParser()
    return prompt | llm | parser


def create_basic_chain():
    """Create a basic chain using the default QA prompt."""
    from prompt_template.prompts import create_qa_prompt
    
    prompt = create_qa_prompt()
    return create_chain(prompt)
