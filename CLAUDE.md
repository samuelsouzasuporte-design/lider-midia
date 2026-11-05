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

## Rotina diária (a tarefa roda às 5h37; tudo é agendado para o MESMO dia)

Por dia são 3 Stories às **07:00** e 1 post no feed às **10:00**.

### Stories das 07:00 (pedido do dono da loja)
1. **"Loja aberta"**, todo dia, sempre igual no formato: selo "BOM DIA!", chamada "BOM DIA, CRATEÚS", linha1 "Loja", linha2 "aberta", subtítulo variando um pouco (ex.: "Pneus e baterias esperando por você.", "Passa aqui hoje!", "Chama no WhatsApp e garanta o seu."). Foto: alterne entre `fachada-lider.jpg`, `loja-interior.jpg` e `loja-baterias.jpg`. Domingo: use "Bom domingo!" no selo e não diga "loja aberta" (o horário de domingo não foi confirmado); use linha1 "Bom", linha2 "domingo" e subtítulo "Segunda estamos te esperando!".
2. **Duas artes de produto**, revezando em dois pares:
   - **Dia A:** BATERIA (de carro) + PNEU DE CARRO
   - **Dia B:** PNEU DE MOTO + BATERIA DE MOTO
   Alterne A/B: veja em `historico.md` qual par foi usado por último e use o outro.
   Sugestões de foto (olhe a foto antes para confirmar): baterias de carro → `expositor-moura.jpg`, `baterias-pallet.jpg`, `baterias-zetta.jpg`, `promo-moura.jpg`, `estoque-pneus-baterias.jpg`; pneu de carro → `pneus-goodyear.jpg`, `pneus-carro.jpg`, `parede-pneus.jpg`; pneu de moto → `pneus-e-baterias.jpg`, `parede-pneus.jpg` (pilhas de pneus finos); bateria de moto → `prateleiras-baterias.jpg`, `loja-baterias.jpg` (baterias pequenas nas prateleiras). Se não achar foto boa para uma categoria, use a mais próxima e não afirme modelos específicos.
   Textos de exemplo: chamada "PARA SEU CARRO" / linha1 "Bateria" / linha2 "nova"; chamada "PARA SUA MOTO" / linha1 "Pneu de" / linha2 "moto"; chamada "PARA SUA MOTO" / linha1 "Bateria" / linha2 "de moto"; chamada "PARA SEU CARRO" / linha1 "Pneus" / linha2 "de carro". Selo: "PRONTA ENTREGA" ou "CONFIRA". Varie o subtítulo.

### Post do feed às 10:00
Um por dia, seguindo o rodízio de temas abaixo.

### Passo a passo
1. Leia `historico.md` (tema do feed, par A/B e fotos usadas recentemente). Olhe cada foto (Read) antes de usar e evite repetir a mesma foto em dias seguidos.
2. Para cada arte, crie um JSON em `posts/<data>/` (`aberta.json`, `produto1.json`, `produto2.json`, `feed.json`) e rode:
   `python3 ferramentas/gerar_arte.py posts/<data>/<nome>.json posts/<data>/<nome>`
   (gera `feed.jpg` e `story.jpg` dentro da pasta `<nome>`; para os Stories use o `story.jpg`, para o feed use o `feed.jpg` de `feed/`).
   Regras de texto: `linha1` com 1 ou 2 palavras curtas; `linha2` com até ~9 letras; `subtitulo` com até ~45 caracteres; `selo` com até 16 caracteres.
3. Olhe as imagens geradas (Read). Se o texto estourar ou ficar ilegível, ajuste e gere de novo.
4. Escreva `posts/<data>/legenda.txt` para o feed: gancho na 1ª linha, 2 a 3 linhas de conteúdo, endereço, WhatsApp, "Vem pra Líder! 💛" e 5 a 8 hashtags (#LiderBateriasEPneus #Crateús sempre).
5. Commit e push (`git add -A && git commit -m "post <data>" && git push origin main`). Confirme com `git ls-remote origin` que o commit chegou.
6. Agende no Metricool (createScheduledPost, blogId 7896220, autoPublish true, fuso America/Fortaleza). Antes, rode getScheduledPosts do dia e não duplique o que já existir:
   - **07:00** Story "Loja aberta", depois **07:01** Story produto 1 e **07:02** Story produto 2 (instagramData.type "STORY", sem text).
   - **10:00** Post no feed (instagramData.type "POST", text = legenda).
   - media = `https://raw.githubusercontent.com/samuelsouzasuporte-design/lider-midia/main/posts/<data>/<nome>/<story|feed>.jpg`
   - Se algum horário já passou, agende 5 minutos à frente do horário atual.
7. Acrescente uma linha em `historico.md` com: data, tema do feed, par de Stories (A ou B), fotos usadas. Commit e push.

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
