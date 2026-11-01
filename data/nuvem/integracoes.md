# Integrações e webhooks

## Como os webhooks funcionam

A Nuvem envia um POST para a URL cadastrada a cada evento. O endpoint do
cliente deve responder com status 2xx em até 10 segundos; caso contrário,
a entrega conta como falha.

## Novas tentativas e desativação

Entregas com falha são reenviadas até 5 vezes, com intervalos de 1, 5, 15,
30 e 60 minutos. Depois de 50 falhas seguidas, o webhook é desativado
automaticamente e o responsável técnico recebe um e-mail. Para reativar,
basta corrigir o endpoint e clicar em Reativar em Configurações > Webhooks.

## Limites da API

A API pública aceita 100 requisições por minuto por chave. Acima disso, a
resposta é 429 com o cabeçalho Retry-After indicando quantos segundos
esperar.
