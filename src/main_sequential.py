"""
Main entry point for the Sequential Chain Pattern example.
"""

from dotenv import load_dotenv

load_dotenv()

from sequential_chain import create_analysis_chain


def main():
    chain = create_analysis_chain()
    
    result = chain({
        "text": "A inteligência artificial está transformando o mundo moderno de maneiras sem precedentes. "
                "Desde assistentes virtuais até sistemas de recomendação complexos, a IA está presente "
                "em quase todos os aspectos da nossa vida cotidiana.",
        "language": "English"
    })
    
    print("=== Original Text ===")
    print(result["original_text"])
    print("\n=== Translated ===")
    print(result["translated"])
    print("\n=== Summary ===")
    print(result["summary"])
    print("\n=== Sentiment ===")
    print(result["sentiment"])


if __name__ == "__main__":
    main()
