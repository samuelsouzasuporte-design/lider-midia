# Instagram da Líder Baterias e Pneus: rotina diária

Este repositório guarda as artes publicadas no Instagram **@liderbateriasepneus**.
Ele é **público**, porque o Metricool busca as imagens por link direto:
`https://raw.githubusercontent.com/samuelsouzasuporte-design/lider-midia/main/<caminho>`

## Dados da loja (use exatamente assim)
- Nome: Líder Baterias e Pneus
- Endereço: Rua Deolino Barreto, 860 - Centro, Crateús/CE
- WhatsApp: (88) 9.8865-5130
- Instagram: @liderbateriasepneus
- Vende: pneus para carros e motos e baterias automotivas (marcas vistas na loja: Moura, Zetta, Pioneiro, Onbat, Heliar/América, Goodyear, Dunlop, Michelin, Maggion)
- Informações confirmadas nas artes da própria loja (pode usar): **instalação em até 30 minutos**, **atendimento rápido**, **linha pesada: baterias para caminhões**.
- NÃO usar: "10x sem juros" e garantias (aparecem só em banners das marcas, não foram confirmados pela loja).
- Metricool: brandId/blogId **7896220**, fuso **America/Fortaleza**

## Estrutura
- `marca/logo.png`: logo oficial (não alterar)
- `fotos/`: FOTOS DE VERDADE da loja, nítidas (prioridade máxima). O nome já diz a categoria:
  - bateria de carro: `bateria-carro-01.jpg`, `bateria-carro-02.jpg`, `bateria-carro-03-expositor-moura.jpg`, `bateria-carro-04-pioneiro-onbat.jpg` (baterias de CARRO Pioneiro/Onbat; o banner ao fundo é de moto, mas as baterias não são)
  - pneu de carro: `pneu-carro-01.jpg` (pneus no alto, baterias embaixo; use posicao_foto "center 20%"), `pneu-carro-02-estoque.jpg`, `pneu-carro-03.jpg` (pilhas de pneus de carro)
  - pneu de moto: `pneu-moto-01.jpg`, `pneu-moto-02.jpg` (pneus de moto em primeiro plano; use posicao_foto "center 70%")
  - bateria de moto: AINDA SEM FOTO CONFIRMADA. Até o dono mandar, faça a arte de bateria de moto com uma foto da loja (`loja-interior-prateleiras.jpg` ou fachada) e texto genérico ("Bateria para sua moto? Temos!"), sem mostrar baterias de carro como se fossem de moto.
  - loja/interior: `loja-interior-prateleiras.jpg` (interior com expositor Moura e prateleiras)
  - loja/fachada: `loja-fachada-01.jpg`, `loja-fachada-02.jpg` (ótimas para o Story "Loja aberta" e posts institucionais)
- `artes-prontas/`: artes que a própria loja já fez (`linha-pesada-caminhoes.jpg`, `quando-precisar.jpg`, formato 9:16). Podem ser republicadas como Story no máximo 1 vez por semana cada, nos horários de produto, sem alterar.
- `fotos/de-video/`: quadros tirados de vídeos, menos nítidos. Use só se não houver foto boa da categoria em `fotos/`.
- Nunca invente imagens nem use banco de imagens.
- `ferramentas/gerar_arte.py`: gera `feed.jpg` (1080x1350) e `story.jpg` (1080x1920) no padrão visual da marca (preto #0E0F12 + amarelo #FFB800, Exo 2 itálico)
- `posts/AAAA-MM-DD/`: artes e `legenda.txt` de cada dia
- `historico.md`: um registro por dia (tema, foto usada, título). Leia antes de escolher o tema, para não repetir.

## Rotina diária (a tarefa roda às 5h37; tudo é agendado para o MESMO dia)

Por dia são 3 Stories às **07:00** e 4 posts no feed: **10:00, 12:30, 14:00 e 15:45** (horários pedidos pelo dono da loja).

### Stories das 07:00 (pedido do dono da loja)
1. **"Loja aberta"**, todo dia, sempre igual no formato: selo "BOM DIA!", chamada "BOM DIA, CRATEÚS", linha1 "Loja", linha2 "aberta", subtítulo variando um pouco (ex.: "Pneus e baterias esperando por você.", "Passa aqui hoje!", "Chama no WhatsApp e garanta o seu."). Foto: alterne entre `loja-fachada-01.jpg`, `loja-fachada-02.jpg` e `bateria-carro-03-expositor-moura.jpg`. Domingo: use "Bom domingo!" no selo e não diga "loja aberta" (o horário de domingo não foi confirmado); use linha1 "Bom", linha2 "domingo" e subtítulo "Segunda estamos te esperando!".
2. **Duas artes de produto**, revezando em dois pares:
   - **Dia A:** BATERIA (de carro) + PNEU DE CARRO
   - **Dia B:** PNEU DE MOTO + BATERIA DE MOTO
   Alterne A/B: veja em `historico.md` qual par foi usado por último e use o outro.
   Use as fotos de `fotos/` da categoria certa (lista acima). `fotos/de-video/` só como reserva. Não afirme modelos específicos.
   Textos de exemplo: chamada "PARA SEU CARRO" / linha1 "Bateria" / linha2 "nova"; chamada "PARA SUA MOTO" / linha1 "Pneu de" / linha2 "moto"; chamada "PARA SUA MOTO" / linha1 "Bateria" / linha2 "de moto"; chamada "PARA SEU CARRO" / linha1 "Pneus" / linha2 "de carro". Selo: "PRONTA ENTREGA" ou "CONFIRA". Varie o subtítulo.

### Posts do feed (4 por dia, cada um com tema diferente)
- **10:00**: tema do dia, seguindo o "Rodízio de temas" abaixo.
- **12:30**: produto, revezando BATERIA DE CARRO → PNEU DE CARRO → PNEU DE MOTO → BATERIA DE MOTO (pegue o próximo depois do último registrado em `historico.md`).
- **14:00**: o produto seguinte nesse mesmo rodízio (diferente do das 12:30).
- **15:45**: chamada para ação, alternando: "Faça seu orçamento no WhatsApp" / "Instalação em até 30 minutos" / "Venha conhecer a loja" / "Linha pesada: baterias para caminhões".
Use fotos diferentes nos 4 posts do mesmo dia sempre que possível. Se houver poucas fotos, troque ao menos o enquadramento (`posicao_foto`) e os textos. Cada post tem a sua legenda (curta, com gancho diferente), sempre com endereço, WhatsApp e hashtags.

### Passo a passo
1. Leia `historico.md` (tema do feed, par A/B e fotos usadas recentemente). Olhe cada foto (Read) antes de usar e evite repetir a mesma foto em dias seguidos.
2. Para cada arte, crie um JSON em `posts/<data>/` (`aberta.json`, `produto1.json`, `produto2.json`, `feed1000.json`, `feed1230.json`, `feed1400.json`, `feed1545.json`) e rode:
   `python3 ferramentas/gerar_arte.py posts/<data>/<nome>.json posts/<data>/<nome>`
   (gera `feed.jpg` e `story.jpg` dentro da pasta `<nome>`; para os Stories use o `story.jpg`, para o feed use o `feed.jpg` das pastas `feedHHMM/`).
   Regras de texto: `linha1` com 1 ou 2 palavras curtas; `linha2` com até ~9 letras; `subtitulo` com até ~45 caracteres; `selo` com até 16 caracteres.
3. Olhe as imagens geradas (Read). Se o texto estourar ou ficar ilegível, ajuste e gere de novo.
4. Escreva uma legenda por post do feed (`posts/<data>/legenda1000.txt`, `legenda1230.txt`, `legenda1400.txt`, `legenda1545.txt`): gancho na 1ª linha, 2 a 3 linhas de conteúdo, endereço, WhatsApp, "Vem pra Líder! 💛" e 5 a 8 hashtags (#LiderBateriasEPneus #Crateús sempre).
5. Commit e push (`git add -A && git commit -m "post <data>" && git push origin main`). Confirme com `git ls-remote origin` que o commit chegou.
6. Agende no Metricool (createScheduledPost, blogId 7896220, autoPublish true, fuso America/Fortaleza). Antes, rode getScheduledPosts do dia e não duplique o que já existir:
   - **07:00** Story "Loja aberta", depois **07:01** Story produto 1 e **07:02** Story produto 2 (instagramData.type "STORY", sem text).
   - **10:00, 12:30, 14:00 e 15:45** Posts no feed (instagramData.type "POST", text = legenda correspondente, media = `feedHHMM/feed.jpg`).
   - media = `https://raw.githubusercontent.com/samuelsouzasuporte-design/lider-midia/main/posts/<data>/<nome>/<story|feed>.jpg`
   - Se algum horário já passou, agende 5 minutos à frente do horário atual.
7. Acrescente uma linha em `historico.md` com: data, tema das 10h, produtos das 12:30 e 14h, chamada das 15:45, par de Stories (A ou B), fotos usadas. Commit e push.

## Rodízio de temas (post das 10:00, um por dia)
1. Estoque / pronta entrega de pneus
2. Baterias: marcas e garantia (sem inventar prazos ou preços)
3. Dica: sinais de bateria fraca (carro demorando a pegar, luzes fracas)
4. Pneus de moto
5. Dica: calibragem e quando trocar o pneu (indicador TWI de 1,6 mm)
6. Institucional: venha conhecer a loja / fachada
7. Chamada para o WhatsApp: "faça seu orçamento"

## Proibido
- Inventar preços, promoções, prazos de garantia, parcelamento ou serviços que a loja não confirmou.
- Usar foto que não seja das pastas `fotos/` ou `fotos/de-video/`.
- Mudar endereço, telefone ou logo.
