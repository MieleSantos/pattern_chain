"""
Main entry point for the Few-Shot Prompting Pattern example.
"""

from dotenv import load_dotenv

load_dotenv()

from few_shot import create_dynamic_few_shot_chain, create_fixed_few_shot_chain

MESSAGE = "Paguei o boleto mas o sistema ainda mostra a conta como bloqueada."


def main():
    print("=== Fixed examples (all 6) ===")
    print(create_fixed_few_shot_chain().invoke({"message": MESSAGE}))

    print("\n=== Dynamic examples (2 most similar) ===")
    print(create_dynamic_few_shot_chain(k=2).invoke({"message": MESSAGE}))


if __name__ == "__main__":
    main()
