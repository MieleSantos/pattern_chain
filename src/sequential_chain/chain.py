"""
Sequential Chain configuration.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model


def create_sequential_chain(
    prompt: ChatPromptTemplate,
    model_name: str = "gemini-2.5-flash",
    model_provider: str = "google_genai"
):
    """Create a simple chain with prompt, model and parser."""
    llm = init_chat_model(model=model_name, model_provider=model_provider)
    parser = StrOutputParser()
    return prompt | llm | parser


def create_translate_summary_chain():
    """Create a chain that translates then summarizes."""
    from sequential_chain.prompts import create_translation_prompt, create_summary_prompt
    
    translate_prompt = create_translation_prompt()
    summary_prompt = create_summary_prompt()
    
    translate_llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
    summary_llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
    
    parser = StrOutputParser()
    
    translate_chain = translate_prompt | translate_llm | parser
    summary_chain = summary_prompt | summary_llm | parser
    
    def combined_chain(input_dict):
        translated = translate_chain.invoke({
            "target_language": input_dict.get("language", "English"),
            "text": input_dict["text"]
        })
        summary = summary_chain.invoke({"text": translated})
        return {"translated": translated, "summary": summary}
    
    return combined_chain


def create_analysis_chain():
    """Create a chain that performs: translate -> summarize -> sentiment analysis."""
    from sequential_chain.prompts import create_translation_prompt, create_summary_prompt, create_sentiment_prompt
    
    translate_prompt = create_translation_prompt()
    summary_prompt = create_summary_prompt()
    sentiment_prompt = create_sentiment_prompt()
    
    llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
    parser = StrOutputParser()
    
    translate_chain = translate_prompt | llm | parser
    summary_chain = summary_prompt | llm | parser
    sentiment_chain = sentiment_prompt | llm | parser
    
    def combined_chain(input_dict):
        translated = translate_chain.invoke({
            "target_language": input_dict.get("language", "English"),
            "text": input_dict["text"]
        })
        summary = summary_chain.invoke({"text": translated})
        sentiment = sentiment_chain.invoke({"text": summary})
        
        return {
            "original_text": input_dict["text"],
            "translated": translated,
            "summary": summary,
            "sentiment": sentiment
        }
    
    return combined_chain
