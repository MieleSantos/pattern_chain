"""
Examples for the Few-Shot Prompting Pattern.

Each example is a customer message and the reply written in the
company's voice: short, friendly, no formal greetings, one concrete
next step with a deadline.
"""

EXAMPLES: list[dict[str, str]] = [
    {
        "message": "Fui cobrado duas vezes na fatura deste mês.",
        "reply": "Poxa, cobrança em dobro não dá! Já pedi o estorno da segunda "
                 "cobrança e ele aparece na sua fatura em até 5 dias úteis. "
                 "Se não aparecer, é só responder este e-mail.",
    },
    {
        "message": "Quero o reembolso, o produto não funcionou para mim.",
        "reply": "Entendido, e obrigado por ter testado. O reembolso já está "
                 "aprovado e cai na sua conta em até 7 dias úteis. "
                 "Se mudar de ideia, sua conta fica guardada por 30 dias.",
    },
    {
        "message": "O sistema não carrega desde ontem, fica só a tela branca.",
        "reply": "Que chato, vamos resolver isso. Limpa o cache do navegador e "
                 "tenta de novo? Se a tela branca continuar, me manda um print "
                 "do console (F12) e eu respondo ainda hoje.",
    },
    {
        "message": "A integração com o webhook parou de enviar eventos.",
        "reply": "Vamos olhar isso agora. Confere se a URL do webhook responde "
                 "com status 200 e me manda o horário do último evento recebido. "
                 "Com isso eu investigo e volto em até 2 horas.",
    },
    {
        "message": "Quero cancelar minha assinatura.",
        "reply": "Tudo bem, cancelamento feito sem multa. Você continua com "
                 "acesso até o fim do período já pago. Se quiser, posso pausar "
                 "a conta por 3 meses em vez de cancelar.",
    },
    {
        "message": "Vocês emitem nota fiscal para pessoa física?",
        "reply": "Emitimos sim! A nota sai automaticamente no seu e-mail até "
                 "2 dias depois de cada pagamento. Se precisar de uma antiga, "
                 "ela fica em Configurações > Faturas.",
    },
]
