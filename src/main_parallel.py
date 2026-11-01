"""
Main entry point for the Parallel Chain Pattern example.
"""

import time

from dotenv import load_dotenv

load_dotenv()

from parallel_chain import create_parallel_analysis_chain


def main():
    chain = create_parallel_analysis_chain()

    start = time.perf_counter()
    result = chain.invoke(
        {
            "text": "A inteligência artificial está transformando o mundo moderno de "
                    "maneiras sem precedentes. Desde assistentes virtuais até sistemas "
                    "de recomendação, a IA está presente em quase todos os aspectos "
                    "da nossa vida cotidiana.",
            "language": "English",
        },
        # Limits how many calls run at the same time (useful for rate limits)
        config={"max_concurrency": 3},
    )
    elapsed = time.perf_counter() - start

    analysis = result["analysis"]
    print("=== Translated ===")
    print(result["translated"])
    print("\n=== Summary ===")
    print(analysis["summary"])
    print("\n=== Sentiment ===")
    print(analysis["sentiment"])
    print("\n=== Keywords ===")
    print(analysis["keywords"])
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
