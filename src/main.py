"""
Main entry point for the Prompt Template Pattern example.
"""

from dotenv import load_dotenv

load_dotenv()

from prompt_template import create_basic_chain


def main():
    chain = create_basic_chain()
    
    result = chain.invoke(
        {"style": "formal", "question": "What is Chain in Generative AI?"}
    )
    print(result)


if __name__ == "__main__":
    main()
