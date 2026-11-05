# Instagram da Líder Baterias e Pneus: rotina diária

Este repositório guarda as artes publicadas no Instagram **@liderbateriasepneus**.
Ele é **público**, porque o Metricool busca as imagens por link direto:
`https://raw.githubusercontent.com/samuelsouzasuporte-design/lider-midia/main/<caminho>`

## Dados da loja (use exatamente assim)
- Nome: Líder Baterias e Pneus
- Endereço: Rua Deolino Barreto, 860 - Centro, Crateús/CE
- WhatsApp: (88) 9.8865-5130
- Instagram: @liderbateriasepneus
- Vende: pneus para carros e motos e baterias automotivas (marcas vistas na loja: Moura, Zetta, Pioneiro, Heliar, Goodyear, Dunlop)
- Metricool: brandId/blogId **7896220**, fuso **America/Fortaleza**

## Estrutura
- `marca/logo.png`: logo oficial (não alterar)
- `fotos/`: fotos reais da loja (use só essas; nunca invente nem use banco de imagens)
- `ferramentas/gerar_arte.py`: gera `feed.jpg` (1080x1350) e `story.jpg` (1080x1920) no padrão visual da marca (preto #0E0F12 + amarelo #FFB800, Exo 2 itálico)
- `posts/AAAA-MM-DD/`: artes e `legenda.txt` de cada dia
- `historico.md`: um registro por dia (tema, foto usada, título). Leia antes de escolher o tema, para não repetir.

## Rotina diária
1. Leia `historico.md`. Escolha o tema do dia seguindo o rodízio abaixo e uma foto de `fotos/` que não tenha sido usada nos últimos 5 dias. Olhe a foto (Read) antes de usar.
2. Crie `posts/<data>/arte.json` e rode:
   `python3 ferramentas/gerar_arte.py posts/<data>/arte.json posts/<data>`
   Regras de texto: `linha1` com 1 ou 2 palavras curtas; `linha2` com 1 palavra de até ~9 letras; `subtitulo` com até ~45 caracteres; `selo` com até 16 caracteres.
3. Olhe `feed.jpg` e `story.jpg` (Read). Se o texto estourar ou ficar ilegível, ajuste e gere de novo.
4. Escreva `posts/<data>/legenda.txt`: gancho na 1ª linha, 2 a 3 linhas de conteúdo, endereço, WhatsApp, "Vem pra Líder! 💛" e 5 a 8 hashtags (#LiderBateriasEPneus #Crateús sempre).
5. Faça commit e push (`git add -A && git commit -m "post <data>" && git push origin main`).
6. Agende no Metricool (createScheduledPost, blogId 7896220, autoPublish true):
   - **Post no feed às 10:00** (melhor horário): instagramData.type "POST", media = URL raw do feed.jpg, text = legenda.
   - **Story às 18:00**: instagramData.type "STORY", media = URL raw do story.jpg, sem text.
   - Se o horário de hoje já passou, agende para o próximo horário disponível ainda hoje (ou para amanhã, se não houver).
7. Acrescente uma linha em `historico.md`, faça commit e push.

## Rodízio de temas (um por dia)
1. Estoque / pronta entrega de pneus
2. Baterias: marcas e garantia (sem inventar prazos ou preços)
3. Dica: sinais de bateria fraca (carro demorando a pegar, luzes fracas)
4. Pneus de moto
5. Dica: calibragem e quando trocar o pneu (indicador TWI de 1,6 mm)
6. Institucional: venha conhecer a loja / fachada
7. Chamada para o WhatsApp: "faça seu orçamento"

## Proibido
- Inventar preços, promoções, prazos de garantia, parcelamento ou serviços que a loja não confirmou.
- Usar foto que não seja da pasta `fotos/`.
- Mudar endereço, telefone ou logo.
