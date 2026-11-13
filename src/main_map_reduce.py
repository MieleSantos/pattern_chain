"""
Main entry point for the Map-Reduce Pattern example.
"""

from dotenv import load_dotenv

load_dotenv()

from map_reduce import format_note, load_tickets, summarize_tickets


def main():
    tickets = load_tickets()
    print(f"{len(tickets)} tickets, {sum(len(t) for t in tickets)} caracteres\n")

    # The file is small on purpose. max_chars=800 forces several batches,
    # as if each prompt could only hold a few tickets.
    result = summarize_tickets(tickets, max_chars=800)

    print(f"--- Map: {result['map_calls']} chamadas, {len(result['notes'])} notas")
    for note in result["notes"]:
        print(format_note(note))

    print(f"\n--- Totais (contados no código): {result['totals']}")
    print(f"--- Rodadas de collapse: {result['collapse_rounds']}")

    print("\n--- Relatório")
    print(result["report"])


if __name__ == "__main__":
    main()
