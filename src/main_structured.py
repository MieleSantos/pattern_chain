"""
Main entry point for the Structured Output Pattern example.
"""

from dotenv import load_dotenv

load_dotenv()

from structured_output import create_structured_chain


def main():
    chain = create_structured_chain()

    ticket = chain.invoke({
        "message": "Fui cobrado duas vezes na fatura de outubro do plano Pro "
                   "e preciso do estorno urgente, senão meu cartão estoura."
    })

    # ticket is a TicketAnalysis instance, not a string
    print(type(ticket).__name__)
    print(ticket.model_dump_json(indent=2))

    if ticket.priority == "high" and ticket.needs_human:
        print("\n-> Encaminhar para a fila de atendimento humano")


if __name__ == "__main__":
    main()
