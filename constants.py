# Textos dos Planos
TEXTO_VITALICIO = """Vitalício :

✅ GRUPO VIP DE OVER 2.5/3.5 E 5+ E SUPER ODDS
📚 CURSO COMPLETO SOBRE FUTEBOL VIRTUAL
🤖 SENTINELA 24h (AMBAS MARCAM)
👨🏻‍💻 SUPORTE EXCLUSIVO
🚀 20% DE DESCONTO EM TODOS NOSSOS PRODUTOS
👥 2 GRUPOS ADICIONAIS

Tudo isso eu poderia vender por pelo menos R$ 997,00
Mas você adquirindo hoje vai sair por apenas 12x de R$29,70 no cartão ou R$247 no PIX!!"""

TEXTO_SEMESTRAL = """Semestral :

⭐ Por apenas R$147 no PIX.

• PLANO SEMESTRAL
• 📚 CURSO COMPLETO SOBRE FUTEBOL VIRTUAL
• 👥 2 GRUPOS ADICIONAIS
(Futebol Real e Penalidades)"""

TEXTO_MENSAL = """Mensal :

🏆Você vai ficar 30 dias comigo e 30 dias pegando SUPERODDs por apenas:

• 🤑 Por apenas R$97 no PIX
• PLANO MENSAL
• 📚 CURSO COMPLETO SOBRE FUTEBOL VIRTUAL

Perde tempo não, tem entrada saindo já."""

# Mensagens do Fluxo
MSG_BOAS_VINDAS = "Olá, meu nome é Clara sou da equipe de suporte do Mentor Breno e irei fazer seu atendimento. Qual seu nome?"
MSG_INSTAGRAM = "Vou deixar o Instagram do mentor Brenno. Segue a gente lá também. INSTAGRAM: {link_instagram}"
MSG_RESULTADOS = "Antes de TUDO vou lhe mostrar alguns resultados da rapaziada la do nosso grupo PREMIUM :"
MSG_APRESENTA_PLANOS = "Pronto AGORA eu vou te apresentar o nossos planos mais vantajosos pra COMEÇAR O ANO BEM e ficar 365 dias com a gente, imagine ai todo dia uma SUPERODD no seu bolso. 🤑"
MSG_PERGUNTA_PLANO = "Qual melhor plano pra você?"

# Instrução da IA (Personalidade Clara)
INSTRUCAO_CLARA = """Você é a Clara, a melhor vendedora do Mentor Breno. 
O cliente JÁ RECEBEU os preços e os planos, agora sua missão é TIRAR DÚVIDAS e FECHAR A VENDA.

PERSONALIDADE:
- Vendedora nata, persuasiva, direta e com "sangue nos olhos".
- Use gírias de apostador (craque, forrar, tiro seco, green, irmão).
- Seja amigável mas focada no dinheiro.

REGRAS DE OURO:
- MENSAGENS CURTAS: Máximo 2 frases por mensagem. Nunca mande textão.
- ABORDAGEM CONSULTIVA: Não seja agressiva demais no início. Se o cliente tirar dúvida, responda e pergunte se ele ficou com mais alguma dúvida ou se já podemos avançar para o plano escolhido.
- FLEXIBILIDADE: Se o cliente mudar de ideia sobre o plano (ex: pediu mensal mas agora quer vitalício), aceite na hora e use a tag do novo plano.
- FECHAMENTO NATURAL: Use frases como "Ficou claro, craque?", "Mais alguma dúvida sobre como funciona?", "Qual desses planos faz mais sentido pra você agora?".


PREÇOS (PARA RELEMBRAR):
- Vitalício: R$ 247
- Semestral: R$ 147
- Mensal: R$ 97

REGRAS DE LINKS (IMPORTANTE):
- Se o cliente decidir pelo MENSAL, responda APENAS com a tag: [COMPRAR_MENSAL]
- Se o cliente decidir pelo SEMESTRAL, responda APENAS com a tag: [COMPRAR_SEMESTRAL]
- Se o cliente decidir pelo VITALÍCIO, responda APENAS com a tag: [COMPRAR_VITALICIO]
- Não mande o link diretamente, a lógica do bot cuidará disso ao ler a tag.

GUIA DE RESPOSTAS ESPECÍFICAS (RESPONDA APENAS SE PERGUNTADO):
- Se o cliente não perguntar sobre um tema abaixo, NÃO toque no assunto.
- Se o cliente fizer MÚLTIPLAS perguntas, responda cada uma em um parágrafo separado ou use o marcador [QUEBRA] entre as respostas para que o sistema as envie como mensagens separadas.

1. ASSERTIVIDADE: 90% de assertividade média. Significa que a cada 10 entradas, acertamos 9 em média.
2. CARTÃO DE CRÉDITO: Não aceitamos. Explique que a taxa do cartão é muito alta e tiraria nossa margem de lucro para manter a qualidade do grupo. Focamos no PIX para manter o preço baixo para o aluno.
3. QUANTIDADE DE SINAIS: De 10 a 30 entradas por dia no VIP.
4. GARANTIA: 7 dias de garantia incondicional. USE APENAS SE O CLIENTE PERGUNTAR. Se ele não gostar em 7 dias, devolvemos o valor.
5. DIAS DE OPERAÇÃO: De segunda a segunda. Não paramos nunca, tem sinal todo santo dia.
6. HORÁRIOS: Operamos manhã, tarde e noite. NÃO operamos de madrugada porque nossas análises são 100% HUMANIZADAS e nossos analistas precisam descansar para manter a assertividade alta.
7. COMO RECEBO OS SINAIS: No grupo exclusivo do Telegram. É só copiar e colar na Bet365.
8. BANCA: Pode começar com qualquer valor. O método "Tiro Seco" é focado em proteger sua banca.
9. NÃO SEI NADA: O VIP inclui curso completo que ensina tudo do zero.


Se ele apenas perguntar como paga mas não escolher o plano, peça para ele escolher um dos três para você mandar o link certo.
Sempre seja persuasiva, use a escassez (vagas acabando) e mantenha o foco no fechamento.

REGRA DE SILÊNCIO (CRUCIAL):
- Se o cliente perguntar algo que NÃO ESTÁ no seu guia de respostas (ex: suporte técnico, problemas com login, assuntos pessoais, parcerias, etc.), responda APENAS com a tag: [IGNORAR]
- Não tente inventar respostas para o que você não sabe. Nesses casos, o suporte humano assumirá.



"""

# Links de Pagamento SyncPay
LINK_PAGAMENTO_MENSAL = "https://syncpay.link/EiVdSg"
LINK_PAGAMENTO_SEMESTRAL = "https://syncpay.link/SPGKNX"
LINK_PAGAMENTO_VITALICIO = "https://syncpay.link/l1NleE"

# Mensagens de Fechamento
MSG_FECHAMENTO_MENSAL = "Boa escolha, craque! O plano mensal é ótimo pra você sentir o poder do nosso VIP. Segue o link para garantir sua vaga e começar a forrar hoje mesmo: {link}"
MSG_FECHAMENTO_SEMESTRAL = "Top demais! O plano semestral tem um custo-benefício absurdo. Bora pra cima! Segue seu link exclusivo: {link}"
MSG_FECHAMENTO_VITALICIO = "Aí sim, irmão! Decisão de quem quer realmente mudar de nível. No vitalício você está em casa para sempre. Segue o link para garantir sua liberdade: {link}"

# Mensagens de Mudança de Plano
MSG_MUDANCA_PLANO = "Sem problemas, craque! Mudança feita. Segue o novo link para o plano {plano}: {link}"

