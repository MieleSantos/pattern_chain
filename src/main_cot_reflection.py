"""
Main entry point for the Chain-of-Thought and Reflection Patterns example.
"""

from dotenv import load_dotenv

load_dotenv()

from cot_reflection import (
    create_cot_chain,
    create_direct_chain,
    create_reflection_graph,
    load_policy,
)

# Each question needs more than one rule of the documentation
QUESTIONS = [
    "Contratei o plano anual há 20 dias, parcelado em 12x no cartão. Se eu cancelar "
    "hoje, recebo algum reembolso, pago multa e até quando consigo usar?",
    # "primeira contratação": the 14 days do not start again for a returning customer
    "Fui cliente em 2024, cancelei e voltei a assinar há 5 dias. Não gostei e quero "
    "cancelar de novo. Recebo o dinheiro de volta?",
    "Paguei o boleto ontem à tarde e a conta continua bloqueada. Já posso mandar o "
    "comprovante pelo chat?",
]


def compare_direct_and_cot(context: str):
    question = QUESTIONS[0]
    print(f"=== {question}\n")

    print("--- Resposta direta")
    print(create_direct_chain().invoke({"question": question, "context": context}), end="\n\n")

    result = create_cot_chain().invoke({"question": question, "context": context})
    print("--- Chain-of-Thought: raciocínio (fica no log)")
    print(result.reasoning, end="\n\n")
    print("--- Chain-of-Thought: resposta (vai para o cliente)")
    print(result.answer, end="\n\n")


def run_reflection(context: str):
    graph = create_reflection_graph(context=context)

    for question in QUESTIONS:
        print(f"=== {question}")
        state = {}
        # stream_mode="updates" yields what each node returned, in order
        for update in graph.stream({"question": question}, stream_mode="updates"):
            for node, values in update.items():
                state.update(values)
                if node == "review":
                    critique = values["critique"]
                    print("[review] aprovado" if critique.approved else "[review] reprovado")
                    for issue in critique.issues:
                        print(f"   - {issue}")
                else:
                    print(f"[{node}] {values['answer']}")

        if not state["critique"].approved:
            print("-> Limite de revisões atingido: encaminhar para atendimento humano")
        print(f"(revisões: {state['revisions']})", end="\n\n")


def main():
    context = load_policy()
    compare_direct_and_cot(context)
    run_reflection(context)


if __name__ == "__main__":
    main()
