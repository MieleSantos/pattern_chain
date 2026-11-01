"""
Main entry point for the Router Chain Pattern example.
"""

from dotenv import load_dotenv

load_dotenv()

from router_chain import create_router_chain


MESSAGES = [
    "A integração com o webhook parou de enviar eventos desde ontem às 18h.",
    "Quero cancelar minha assinatura no fim do mês.",
    "Vocês emitem nota fiscal para pessoa física?",
]


def main():
    chain = create_router_chain()

    results = chain.batch([{"message": m} for m in MESSAGES])

    for result in results:
        ticket = result["ticket"]
        print(f"=== [{ticket.category} / {ticket.priority}] {result['message']}")
        print(result["answer"], end="\n\n")


if __name__ == "__main__":
    main()
