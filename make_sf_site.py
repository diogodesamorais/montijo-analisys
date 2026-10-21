# -*- coding: utf-8 -*-
"""
make_sf_site.py — gera o site "As pedras da Sagrada Familia".

Entrada : sagrada-familia-geologia/img-manifest.json  (criado por make_sf_images.py)
Saida  : sagrada-familia-geologia/index.html

Uso: python make_sf_site.py
"""
import json, os, sys, html

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "sagrada-familia-geologia")
MANIFEST = os.path.join(SITE, "img-manifest.json")
OUT = os.path.join(SITE, "index.html")

# ===========================================================================
# DADOS — conteudo do trabalho
# ===========================================================================
STONES = [
    dict(
        id="montjuic", nome="Pedra de Montjuïc", familia="sedimentar",
        familia_label="Roca sedimentar",
        rocha="Arenito silicoso (silicificado)",
        classificacao="Gres silício / lit arenito silício",
        idade="Miocénico médio–superior", ma="~15–11 Ma",
        origem="Deltaíco (sistema deltaico do Llobregat), coluvião da rocha de Collserola",
        local="Montjuïc, Barcelona — Catalunya, Espanha",
        coords="41.363° N, 2.165° E", dist="0–6 km do templo",
        textura="Arenita de grão 0,06–2 mm, de marcada heterometria, passando a microconglomerado; grans unidos por compactação e por cimento silício microcristalino, por vezes argiloso-ferruginoso.",
        mineralogia="Quartz (frequentemente >50%), feldspato potássico, plagioclase, fragmentos de rocha (metamórfica e granítica), moscovita, turmalina; acessórios: zircão, apatite.",
        processo="Deposição detrítica num delta miocénico, seguida de silicificação diagénica quase total. É esta silicificação que transforma um arenito friável num grés compacto e muito resistente — a distinção local entre <em>blanquet</em> (duro) e <em>rebuig</em> (macio) é, em essence, uma distinção de grau de silicificação.",
        rho="2,64 g/cm³", rc="978 kg/cm²", mpa="96",
        uso="Façana do Nascimento, Façana da Paixão, as quatro torres (~100 m), colunas hexagonais de Ø 1,05 m, galerias do coro, escadas de acesso.",
        destaque="A pedra-mãe. Explotada desde a época romana até 1957 — a maior pedreira da história da cidade. Alimentou Barcelona desde os romanos até ao Eixample de Cerdà.",
        imgs=["montjuic-lamina", "montjuic-macro", "montjuic-pedreira", "montjuic-aplicacao"],
    ),
    dict(
        id="orrius", nome="Granito de Òrrius — «ull de serp»", familia="igneia",
        familia_label="Roca ígnea plutónica",
        rocha="Granodiorita–tonalita",
        classificacao="Granitoide ácido, plutónico, textura holocristalina fanerítica",
        idade="Variscano tardio / pós-tectónico", ma="~300–270 Ma",
        origem="Batólito da Serra Litoral Catalana (complexo Sant Llorenç del Munt–Òrrius)",
        local="Òrrius i Llinars del Vallès, Vallès Oriental — Catalunya",
        coords="41.550° N, 2.200° E", dist="~25 km do templo",
        textura="Granular, holocristalina, fanerítica; grão de 2–5 mm (médio a grosso), reconhecível à vista desarmada. Feldspatos zonados; biotita inalterada.",
        mineralogia="Quartz, plagioclase, feldspato potássico, biotita, hornblenda; acessório: zircão.",
        processo="Cristalização lenta de um magma ácido a ~1 km de profundidade no miolo da crusta, no fecho da orogénese varisca (colisão Laurásia–Gondwana). A rocha escura de biotita sobre fundo claro dá o «olho de serpente» que lhe dá o nome.",
        rho="2,69 g/cm³", rc="1 559 kg/cm²", mpa="153",
        uso="A maioria das colunas octogonais de Ø 1,40 m da nave central e do transepto, respetivos capitéis, degraus da escada da cripta e 22 colunas da Façana da Glória.",
        destaque="É a rocha mais authenticamente «catalã» do templo: extraída a 25 km, na mesma serra que fornece o granito ao resto do país.",
        imgs=["orrius-lamina", "orrius-macro", "orrius-serra"],
    ),
    dict(
        id="tarn", nome="Granito do Tarn (Sidobre)", familia="igneia",
        familia_label="Roca ígnea plutónica",
        rocha="Granito leucocrático quartzoso",
        classificacao="Granitoide ácido, plutónico, muito rico em quartzo",
        idade="Variscano", ma="~300 Ma",
        origem="Plano do Sidobre, maciço granítico do Tarn",
        local="Sidobre, Tarn — Occitânia, França",
        coords="43.556° N, 2.470° E", dist="~500 km do templo",
        textura="Granular, holocristalina, fanerítica; grão de 2–3 mm. O quartz pode aparecer em cristais individualizáveis; a biotita apresenta-se cloritizada e a plagioclase, sericitizada.",
        mineralogia="Quartz (até 55% em algumas amostras), plagioclase, feldspato potássico, biotita (cloritizada), moscovita.",
        processo="Mesma orogénese varisca. A célula — composição mais leucocrática — dá-lhe o melhor desempenho mecânico de todos os granitos usados no templo, e uma tonalidade mais clara, quase alba.",
        rho="2,66 g/cm³", rc="1 865 kg/cm²", mpa="183",
        uso="Colunas octogonais de Ø 1,40 m em torno do presbitério e os seus capitéis.",
        destaque="«A rocha que anda»: o Roc de l'Oie, bloco granítico que desliza lentamente sobre a superfície do Sidobre, é a imagem mais famosa desta pedra.",
        imgs=["tarn-granito", "tarn-alteracao", "tarn-panorama"],
    ),
    dict(
        id="fraguas", nome="Granito de Fráguas", familia="igneia",
        familia_label="Roca ígnea plutónica",
        rocha="Granito biotítico bicolor",
        classificacao="Granito plutónico, rico em biotita",
        idade="Variscano", ma="~300 Ma",
        origem="Maciço de Fráguas (Serra da Capelada / norte da Galiza)",
        local="Fráguas, Lugo — Galiza, Espanha",
        coords="43.760° N, 7.600° E", dist="~700 km do templo",
        textura="Granular fanerítica, de biotita abundante; o contraste entre a mica escura e o Feldspato claro dá o aspecto mosqueado característico.",
        mineralogia="Quartz, plagioclase, feldspato potássico, biotita, moscovita.",
        processo="Granito variscano da Galiza, intrudido nos metasedimentos paleozoicos do Maciço Central Galego. A mesma história de 300 Ma, noutro ponto da Ibéria.",
        rho="—", rc="—", mpa="—",
        uso="Colunas hexagonais de Ø 1,05 m encostadas às capelas do abside.",
        destaque="Uma das rochas mais antigas do templo a servir uma zona de sombra — a galeria do abside, onde a luz é indireta e a cor escura do granito amplifica a penumbra.",
        imgs=["fraguas-granito"],
    ),
    dict(
        id="branco", nome="Granito branco cristal (Madrid)", familia="igneia",
        familia_label="Roca ígnea plutónica",
        rocha="Granito leucocrático",
        classificacao="Granitoide ácido de grão médio, claro",
        idade="Variscano", ma="~300 Ma",
        origem="Batólito do Sistema Central (bacia de Madrid)",
        local="Região de Madrid — Castela, Espanha",
        coords="40.417° N, 3.703° E", dist="~510 km do templo",
        textura="Granular, holocristalina, fanerítica; grão médio, côr clara e uniforme.",
        mineralogia="Quartz, feldspato potássico, plagioclase, moscovita, biotita escassa.",
        processo="Granito do Sistema Central ibérico, formado no mesmo intervalo variscano. AEscassez de máficos traduz-se na brancura da pedra.",
        rho="—", rc="—", mpa="—",
        uso="Pequenos detalhes da galeria do coro da nave central.",
        destaque="Detalhe de escala mínima: o granito branco entra apenas onde o olhar apanha a luz de cima.",
        imgs=["granito-branco"],
    ),
    dict(
        id="yazd", nome="Pórfiro vermelho de Yazd", familia="igneia",
        familia_label="Roca ígnea piroclástica",
        rocha="Ignimbrita riolítica",
        classificacao="Roca magmática volcânica piroclástica, textura pseudoporfirítica e eutaxítica",
        idade="Paleogénico (Eoceno–Oligoceno)", ma="~50–35 Ma",
        origem="Domo de Yazd, centro-oeste do Irão (Irã central)",
        local="Yazd, Irão",
        coords="31.897° N, 56.315° E", dist="~4 600 km do templo",
        textura="Pseudoporfirítica: fenocristais visíveis à vista desarmada (maios de 2 mm) envoltos numa matriz vítreo-cristalina com bandado de cor e composição diferentes (microestrutura eutaxítica). Na matriz fluidal observam-se cristalizações esferulíticas.",
        mineralogia="Quartz (fenocristais esqueléticos, por corrosão), plagioclase, feldspato potássico, biotita.",
        processo="Deposição de um fluxo piroclástico denso e quente: os cristais achatam-se e alinham-se na direção do fluxo, o que produz a textura eutaxítica. A cor vermelha vem da oxidação do ferro.",
        rho="2,66 g/cm³", rc="1 940 kg/cm²", mpa="190",
        uso="As quatro maiores colunas do templo — dodecaagonais de Ø 2,10 m — no transepto; altar maior e escadas do presbitério projectados.",
        destaque="A rocha mais resistente de todo o templo e a mais distante. A simetria é notável: as colunas que carregam mais são as de rocha mais antiga e mais dura — 190 MPa.",
        imgs=["yazd-porfiro", "yazd-porfiro-2", "yazd-ignimbrita"],
    ),
    dict(
        id="bagnoregio", nome="Basalto de Bagnoregio", familia="igneia",
        familia_label="Roca ígnea efusiva",
        rocha="Basanita com leucita",
        classificacao="Roca magmática vulcânica efusiva, textura microlítica com fenocristais de leucita",
        idade="Quaternário, Pleistoceno", ma="~0,5–1 Ma",
        origem="Campo vulcânico dos Vulsinos (Montefiascone), junto ao lago de Bolsena",
        local="Bagnoregio / Montefiascone, Lázio — Itália",
        coords="42.633° N, 12.300° E", dist="~1 000 km do templo",
        textura="Microlítica, com fenocristais abundantes de feldspatóides (leucita), piroxena (augite), biotita e plagioclase; micróritos de plagioclase em forma de agulha na matriz.",
        mineralogia="Leucita (feldspatóide), augite, biotita, plagioclase.",
        processo="Extrusão de magma básico, muito fluido, que percorreu dezenas de km antes de solidificar. A presença de leucita em vez de plagiooclaseBoundingField ou sóbite exige pressão total elevada — é o que define a basanita.",
        rho="2,23 g/cm³", rc="841 kg/cm²", mpa="83",
        uso="As 8 colunas decagonais de Ø 1,75 m (fustes e capitéis) — cinzento quase negro, em contraste deliberado com o granito e o pórfiro.",
        destaque="A rocha mais leve e mais «recente» do templo, com a densidade mais baixa de todas (2,23 g/cm³). A geologia quaternária da Itália serve de moldura ao cruz.",
        imgs=["bagnoregio-basanita", "bagnoregio-leucita", "bagnoregio-bolsena"],
    ),
    dict(
        id="castellfollit", nome="Basalto de Castellfollit de la Roca", familia="igneia",
        familia_label="Roca ígnea efusiva",
        rocha="Basanita",
        classificacao="Roca magmática vulcânica efusiva, textura porfirítica",
        idade="Quaternário, Pleistoceno", ma="~217 ka e ~192 ka",
        origem="Campo vulcânico da Garrotxa (Zona Volcânica Catalana)",
        local="Castellfollit de la Roca, Garrotxa — Catalunya, Espanha",
        coords="42.070° N, 2.650° E", dist="~95 km do templo",
        textura="Porfirítica, com matriz microlítica e fenocristais de plagioclase, piroxena e olivina.",
        mineralogia="Plagioclase, piroxena, olivina.",
        processo="Duas coladas de lava muito fluida, vindas dos vulcões de Batet e de Begudà, que ocuparam os vales do Fluvià e do Turonell. Entre elas depositou-se um paleosolo com argilas e piroclastos — um intervalo de 25 000 anos de calma. A contração da lava ao arrefecer produziu a disjunção prismática.",
        rho="2,70 g/cm³", rc="1 237 kg/cm²", mpa="121",
        uso="Cornija do pórtico (nártex) da Façana da Paixão.",
        destaque="O basalto catalão mais recente: as duas coladas que formam o rochedo do povoado foram datadas por K-Ar e arqueomagnetismo. A Garrotxa é, hoje, a prova de que a fronteira do fogo ainda não está longe.",
        imgs=["castellfollit-colunas", "castellfollit-rochedo", "castellfollit-cidade", "garrotxa-fageda"],
    ),
    dict(
        id="calafell", nome="Pedra de Calafell (ou de Vilafranca)", familia="sedimentar",
        familia_label="Roca sedimentar",
        rocha="Calcário fossilífero — biomicrita",
        classificacao="Calcário bioclástico com foraminíferos numa matriz micrítica muito porosa",
        idade="Miocénico", ma="~15–10 Ma",
        origem="Molasse do Baix Penedès (bacia do Penedès)",
        local="Calafell / Vilafranca del Penedès — Catalunya",
        coords="41.250° N, 1.380° E", dist="~45 km do templo",
        textura="Matriz micrítica muito porosa com foraminíferos, algas e fragmentos de moluscos.",
        mineralogia="Praticamente calcite pura.",
        processo="Depósito marinho shallow no Miocénico, com uma fauna bentónica abundante que se fossiliza como o clasto da rocha. A porosidade elevada da matriz explica a sua fragilidade.",
        rho="—", rc="72 kg/cm²", mpa="7",
        uso="Apenas interiores e de fino talhamento: claustros, interiores das fachadas, abside, trifório, claustro do Roser.",
        destaque="A mais fraca de todas as pedras do templo — 7 MPa, treze vezes menos que o pórfiro de Yazd. A resistência não determina o uso: é a pedra mais doce de talhar, e por isso esculpe-se nela.",
        imgs=["calafell-biomicrita", "calafell-local"],
    ),
    dict(
        id="floresta", nome="Pedra de la Floresta", familia="sedimentar",
        familia_label="Roca sedimentar",
        rocha="Calc-arenito dolomítico",
        classificacao="Arenito calcário dolomítico",
        idade="Oligocénico", ma="~34–23 Ma",
        origem="Molasse da bacia de les Garrigues (Penedès–Garrigues)",
        local="La Floresta, les Garrigues — Catalunya, Espanha",
        coords="41.670° N, 0.800° E", dist="~80 km do templo",
        textura="Arenito de grão muito fino; mais de 80% de carbonatos sob a forma de agregados micríticos e microesparíticos, calcite espátrica e formas romboédricas de dolomita, com quartzo fino (0,1 mm).",
        mineralogia="Calcite e dolomita (>80%), quartzo equigranular fino, micas.",
        processo="Areia calcária depositada num ambiente deltaico lacustre/marinho oligocénico, com cimento carbonatado. A baixa dureza e a granulometria fina tornam a rocha ideal para a escultura.",
        rho="2,35 g/cm³", rc="548 kg/cm²", mpa="54",
        uso="Obras escultóricas: anjos músicos da Façana do Nascimento (Etzuro Sotoo) e mais de cem figuras da Façana da Paixão (Josep M. Subirachs).",
        destaque="A pedra dos escultores. Gaudí não a escolheu por resistência — escolheu-a porque se talha como madeira. Subirachs voltaria a ela 60 anos depois.",
        imgs=["floresta-calcarenito", "floresta-local"],
    ),
    dict(
        id="figueres", nome="Pedra de Figueres", familia="sedimentar",
        familia_label="Roca sedimentar",
        rocha="Calcário bioclástico recristalizado",
        classificacao="Calcário recristalizado, localmente «mármore de Figueres»",
        idade="Paleogénico–Neogénico", ma="~40–25 Ma",
        origem="Bacia do Alt Empordà",
        local="Figueres, Alt Empordà — Catalunya, Espanha",
        coords="42.267° N, 2.960° E", dist="~140 km do templo",
        textura="Bioclástica, recristalizada, com passagens de calcite bem cristalizada.",
        mineralogia="Calcite, ocasionalmente dolomita.",
        processo="Calcário marinho com fauna bentónica, sujeito a recristalização. Sem explotações atuais conhecidas — a pedra é obtida por demolição.",
        rho="—", rc="—", mpa="—",
        uso="Paramentos da escada da cripta.",
        destaque="Uma pedra de estrutura modesta que só aparece num lugar — a escada da cripta, onde ovisitante entra no templo pelo ponto mais baixo e mais escuro.",
        imgs=["figueres-calcario"],
    ),
    dict(
        id="macael", nome="Mármore de Macael", familia="metamorfica",
        familia_label="Roca metamórfica",
        rocha="Mármore calcítico",
        classificacao="Mármore calcítico, textura mesocristalina homeoblástica, com foliação metamórfica",
        idade="Protólito triásico; metamorfismo alpino", ma="protólito ~230–200 Ma · metamorfismo ~18–15 Ma",
        origem="Formação de Las Casas, Complexo Nevado-Filábride (Cordilheira Bética)",
        local="Macael, Sierra de los Filabres, Almería — Espanha",
        coords="37.100° N, 2.700° E", dist="~520 km do templo",
        textura="Homeoblástica mesocristalina, grão médio de ~600 µm (até 2 mm), com cristais orientados paralelamente à foliação metamórfica. Bandado cinzento por lechos mais ricos em silicatos.",
        mineralogia="Calcite (>99%); secundários: plagioclase, quartz e mica.",
        processo="Um calcário quase puro do Triásico, soterrado e metamorfizado durante a orogénese alpina sob alta pressão e baixa temperatura (P ≈ 1,8 GPa; T ≈ 500–610 °C). A recristalização é total: o que era rocha sedimentar virou mármore.",
        rho="—", rc="—", mpa="—",
        uso="O pelicano e os pombos do cipreste da Façana do Nascimento (Joan Pastor).",
        destaque="A única rocha metamórfica do conjunto e a que tem a história mais longa: 230 Ma de sedimento, 15 Ma de metamorfismo, uma passagem pelos Alpes e a serração em Almería antes de viajar até Barcelona.",
        imgs=["macael-marmore", "macael-marmore-branco", "macael-local", "macael-monumento"],
    ),
    dict(
        id="travertino", nome="Travertino (Bagni di Tivoli)", familia="sedimentar",
        familia_label="Roca sedimentar",
        rocha="Travertino",
        classificacao="Carbonato continental clástico, com laminacao e porosidade",
        idade="Quaternário, Pleistoceno", ma="~125 ka",
        origem="Depósito deEmitter de carbonato, junto às termas de Tivoli",
        local="Bagni di Tivoli, Lácio — Itália",
        coords="41.960° N, 12.797° E", dist="~1 050 km do templo",
        textura="Carbonato com estrutura laminada e porosidade irregular; os vazios correspondem a canais de água e a restos vegetais.",
        mineralogia="Calcite, com poroidade e material vegetal fosilizado.",
        processo="Precipitação de carbonato de cálcio a partir de águas minerais que percolam rochas calcárias, à temperatura ambiente. É uma rocha química, não detrítica — e por isso tão moderna.",
        rho="—", rc="—", mpa="—",
        uso="Elementos escultóricos da Façana da Paixão (Subirachs).",
        destaque="A rocha mais nova do templo: ~125 000 anos. Numa basílica de 145 anos, uma pedra com cem mil anos é simultaneamente a mais antiga em termos relativos de uso — o que confirma que «antigo» é uma questão de escala, não de substance.",
        imgs=["travertino-rocha", "travertino-detalhe", "travertino-tivoli"],
    ),
]

FAMILIAS = [
    ("sedimentar", "Rocas sedimentares", "Fragmentos derivados de rochas preexistentes, transportados e depositados por água, vento ou gelo. Compactação e cimento Portland transformam-nos em rocha sedimentar. São rochas de origem mecânica: o seu grão guarda a história do transporte.",
     "#8A6A3D"),
    ("igneia", "Rocas ígneas", "Formadas pelo arrefecimento e solidificação de um magma. Plutónicas quando o magma arrefece em profundidade (granitos, ~300 Ma); efusivas quando irrompe à superfície (basaltos, pórfiros).",
     "#B4552F"),
    ("metamorfica", "Rocas metamórficas", "Rochas preexistentes transformadas por calor, pressão e fluidos no interior da crusta, sem fusão. O mármore de Macael é um calcário triásico recristalizado sob 1,8 GPa.",
     "#5B6B7C"),
]

TEMAS = [
    ("01", "A pedra como recurso finito e a lógica do reciclado",
     "O fecho das pedreiras de Montjuïc em 1957 transformou a cidade num arquivo de pedra: a nova matéria-prima do templo passa a ser o <strong>desmonte de edifícios demolidos</strong>. Em 2018 a Junta Constructora passou a fornecer arenito da pedreira de Withnell (Brinscall, Lancashire). Há aqui um argumento arquitetónico e ético forte — a construção como canibalismo de arquivo urbana."),
    ("02", "A geologia local como paleta",
     "Gaudí não escolheu poryra apologia: o arenito de Montjuïc está em toda a Barcelona românica, gótica, neoclássica e modernista. A matéria-prima do templo é a mesma que construiu a cidade — a basílica é a <strong>última e mais ambiciosa pedreira de Montjuïc</strong>. A geologia da cidade determina a paleta, e a paleta determina a forma."),
    ("03", "Desacoplamento entre resistência mecânica e valor expressivo",
     "A pedra de Calafell tem 7 MPa; o pórfiro de Yazd tem 190 MPa. E no entanto é a mais frágil que esculpe a Paixão, e a mais resistente que sustenta as maiores colunas. <strong>A resistência não determina o uso</strong> — o gesto e a leitura determinam. Em sentido inverso, as colunas mais carregadas do templo são as de rocha mais antiga e mais dura."),
    ("04", "Geopolítica da pedra e a fixação do gosto",
     "As roças que expressam a Catalunha (granito do Vallès, arenito de Montjuïc) e as que a <strong>substituem</strong> por indisponibilidade (pórfiro iraniano, basalto italiano, travertino de Tivoli) revelam como o gosto é fixado enquanto a matéria é renegociada. Em 1998, o estilista Subirachs regressou ao mármore e ao travertino: a linguagem estável, a matéria variável."),
    ("05", "Metamorfismo como metáfora de memória",
     "O mármore de Macael é uma roca que mudou de forma há 15 Ma, sob pressão, e que hoje está num templo de 15 m. Triásico → metamorfismo alpino → extração em Almería → Barcelona: a história da pedra é, em si, uma narrativa de transformação do paisaje."),
]

CAMPO = [
    ("Museu de Geologia (Parc de la Ciutadella)", "Barcelona",
     "Expõe a <strong>coleção petrografia do Templo</strong> (amostras e lâminas finas, registos 14.366–14.380),Overlap criada para a exposição <em>Pedres del Temple, roques dels Temps</em> (Any Gaudí, 2002). Diante da fachada do Museu Martorell, uma <strong>exposição ao ar livre de 133 blocos</strong> de pedra ornamental catalã (1907–1929): grés de Montjuïc, granito «ull de serp», basalto de Amer.",
     "Inclui"),
    ("Geomuseu da UPC", "Barcelona",
     "Montra com as <strong>10 rochas mais usadas</strong> na Sagrada Família, com lâminas finas iluminadas à mão: pórfir de Yazd, travertino de Tivoli, grés de Sant Vicenç de Castellet, grés de Montjuïc, basalto de Bagnoregio, granito de Òrrius, mármore branco de Macael, grés de la Floresta.",
     "Inclui"),
    ("Les Borges Blanques", "Les Garrigues",
     "Centro logístico da Sagrada Família, onde se armazena o stock de pedra. Liga a geologia da pedreira ao ciclo logístico da obra — e mostra a escala real do consumo: <strong>~150 000 m³ (~345 milhões de kg)</strong> de material.",
     "Exterior"),
    ("Pedreira romana de Montjuïc", "Barcelona",
     "Os vestígios de corte mais antigos da cidade (La Foixarda, Teatre Grec). Observar os cortes do Miocénico e os fósseis — numulites, ourins, algas — que aparecem nos paramentos das fachadas de Barcelona.",
     "Exterior"),
    ("Castellfollit de la Roca", "Garrotxa",
     "O rochedo de duas coladas basálticas (~217 e ~192 ka), com disjunção prismática, e a Fageda d'en Jordà nas proximidades. A melhor observação de campo da Zona Volcânica Catalana.",
     "Exterior"),
    ("Sidobre", "Tarn, França",
     "A planície granítica que forneceu as colunas do presbitério: blocos em bola, o Roc de l'Oie e o Peyro Clabado. Percurso pedonível de 4–8 km.",
     "Exterior"),
    ("Macael", "Almería, Espanha",
     "A pedreira de mármore branco e o Centro de Interpretação do Mármole. Permite observar a passagem de calcário triásico a mármore recristalizado e a bandagem cinzenta do metamorfismo.",
     "Exterior"),
]

METODO = [
    ("Identificação macroscópica", "Cor, grão, brilho, dureza de Mohs,Reaction com ácido (calcite faz efervescência a 10% HCl) e observação das descontinuidades."),
    ("Análise quantitativa", "Densidade por picnómetro, absorção de água por imersão e resistência à compressão uniaxial, comparada com os valores do itinerário petrográfico do Museu de Geologia."),
    ("Petrografia", "Lâmina fina de 30 µm, observada ao microscópio polarizador em luz paralela e em nicols cruzados, para descrever textura e composição mineral."),
    ("Leitura do contexto", "Cartografia geológica (MAGNA, IGME) e correlação estratigráfica: onde a rocha está na coluna, e que isso diz sobre a sua idade."),
]

BIBLIO = [
    ("Masriera, A.; Caminal, A.; Navarro, R.; Planella, V.; Samper, J. A. (2005)",
     "«Les roques del Temple de la Sagrada Família. Un itinerari petrogràfic a través dels seus elements arquitectònics i ornamentals».",
     "Treballs del Museu de Geologia de Barcelona, 13, 5–41. — <strong>Fonte central</strong>: tabela completa de densidade e resistência à compressão."),
    ("Gómez Gras, C. et al. (2020)",
     "«Petrographic Markers for Archaeometric Identification of Montjuïc Sandstone, the Flagship Stone of Barcelona (NE Spain)».",
     "Minerals, 10(2), 154. — silicificação e identificação arqueométrica do arenito de Montjuïc."),
    ("Michard, A. et al. (2020)",
     "«Fracturing and Near-Surface Diagenesis of a Silicified Miocene Deltaic Sequence: The Montjuïc Hill (Barcelona)».",
     "Minerals, 10(2), 135. — o papel da diagénese próxima à superfície na silicificação."),
    ("Roca, S. (2000)",
     "<em>Pedres de Montjuïc. Els Materials de Construcció del Castell de Montjuïc</em>.",
     "Institut d'Estudis Catalans. — a maior PEDreira da história urbana."),
    ("Faura, J. et al. (1999)",
     "<em>El miocè de la muntanya de Montjuïc: estratigrafia, sedimentologia, petrologia i diagènesi</em>.",
     "Tese doctoral, Universitat Autònoma de Barcelona."),
    ("IDAEA-CSIC et al. (2025)",
     "«Las erupciones volcánicas en la Garrotxa son más recientes de lo esperado».",
     "Quaternary Science Advances. — novas datações Ar-Ar das coladas de Castellfollit."),
    ("Junta Constructora del Temple de la Sagrada Família (2025)",
     "«La pedra de Montjuïc: de l'extracció al reciclatge».",
     "Blog oficial da basílica — logística atual, centro de Les Borges Blanques e reciclagem de pedra."),
    ("Construnews (2025)",
     "«De la cantera al reciclaje: la piedra de Montjuïc en la Sagrada Família».",
     "Volumes consumidos, número de pedreiras e tipos de pedra utilizados."),
    ("IGME / MAGNA", "Cartografia geológica de España, escala 1:50 000.",
     "Folhas 257 (Olot), 389 (Tàrrega), 393–394, 421 (Barcelona), 447 (Vilanova i la Geltrú)."),
]

# ===========================================================================
# HTML
# ===========================================================================
CSS = """
:root{
  --verde:#1F4D3A; --verde-2:#2E6B52; --verde-claro:#E8F0EB;
  --areia:#8A6A3D; --terracota:#B4552F; --cinza-azul:#5B6B7C;
  --papel:#FAF8F4; --papel-2:#FFFFFF; --tinta:#1C1A17; --tinta-2:#5A554E;
  --linha:#DFD9CF; --sombra:0 1px 2px rgba(28,26,23,.05),0 8px 24px rgba(28,26,23,.06);
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:"SF Mono",Consolas,"Liberation Mono",Menlo,monospace;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:76px}
body{margin:0;background:var(--papel);color:var(--tinta);font-family:var(--sans);
  font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}

/* ---------- nav ---------- */
.nav{position:sticky;top:0;z-index:60;background:rgba(250,248,244,.93);
  backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid var(--linha)}
.nav-in{max-width:1220px;margin:0 auto;padding:0 24px;display:flex;align-items:center;
  gap:20px;height:60px}
.brand{font-family:var(--serif);font-weight:700;font-size:17px;color:var(--verde);
  text-decoration:none;white-space:nowrap;letter-spacing:-.01em}
.brand small{display:block;font-family:var(--sans);font-weight:400;font-size:11px;
  color:var(--tinta-2);letter-spacing:.04em;text-transform:uppercase}
.nav-links{margin-left:auto;display:flex;gap:2px;overflow-x:auto;scrollbar-width:none}
.nav-links::-webkit-scrollbar{display:none}
.nav-links a{padding:7px 11px;border-radius:6px;font-size:13.5px;color:var(--tinta-2);
  text-decoration:none;white-space:nowrap;transition:.15s}
.nav-links a:hover{background:var(--verde-claro);color:var(--verde)}
.nav-links a.on{background:var(--verde);color:#fff}

/* ---------- hero ---------- */
.hero{background:linear-gradient(168deg,#17382B 0%,#1F4D3A 48%,#2A6149 100%);
  color:#F2EFE8;padding:72px 24px 64px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;inset:0;
  background:radial-gradient(1000px 380px at 88% -10%,rgba(180,85,47,.30),transparent 62%),
             radial-gradient(760px 320px at 8% 110%,rgba(138,106,61,.26),transparent 60%);pointer-events:none}
.hero-in{max-width:1220px;margin:0 auto;position:relative;z-index:1}
.eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;
  color:#9FC4B2;font-weight:600;margin-bottom:18px}
h1{font-family:var(--serif);font-size:clamp(34px,5.4vw,62px);line-height:1.06;
  margin:0 0 20px;font-weight:700;letter-spacing:-.022em}
.hero p.lead{max-width:760px;font-size:19px;line-height:1.62;color:#D6E2DB;margin:0 0 34px}
.stats{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid rgba(255,255,255,.18);
  padding-top:26px;max-width:900px}
.stat{padding:0 30px 0 0;margin-right:30px;border-right:1px solid rgba(255,255,255,.14)}
.stat:last-child{border-right:0;margin-right:0}
.stat b{display:block;font-family:var(--serif);font-size:31px;line-height:1.1;color:#F6E6C8}
.stat span{font-size:12.5px;color:#A9C6B7;letter-spacing:.03em}

/* ---------- layout ---------- */
.wrap{max-width:1220px;margin:0 auto;padding:0 24px}
section{padding:70px 0;border-bottom:1px solid var(--linha)}
section:last-of-type{border-bottom:0}
.sec-head{max-width:820px;margin-bottom:40px}
.kicker{font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--verde-2);
  font-weight:700;margin-bottom:12px}
h2{font-family:var(--serif);font-size:clamp(26px,3.4vw,40px);line-height:1.14;margin:0 0 14px;
  letter-spacing:-.018em}
h3{font-family:var(--serif);font-size:23px;line-height:1.2;margin:0 0 10px;letter-spacing:-.012em}
.lead{font-size:18px;color:var(--tinta-2);margin:0}

/* ---------- boxes ---------- */
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.card{background:var(--papel-2);border:1px solid var(--linha);border-radius:12px;
  padding:24px;box-shadow:var(--sombra)}
.card h3{margin-bottom:8px}
.card p{font-size:15.5px;color:var(--tinta-2);margin:0 0 10px}
.tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;padding:4px 9px;border-radius:5px;margin-bottom:12px}
.pill{display:inline-block;font-size:12px;padding:3px 9px;border-radius:20px;
  background:var(--verde-claro);color:var(--verde);font-weight:600;margin:0 6px 6px 0}

/* ---------- pedra cards ---------- */
.filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:30px}
.fbtn{border:1px solid var(--linha);background:var(--papel-2);border-radius:20px;
  padding:7px 16px;font-size:13.5px;cursor:pointer;color:var(--tinta-2);
  font-family:inherit;transition:.15s}
.fbtn:hover{border-color:var(--verde-2);color:var(--verde)}
.fbtn.on{background:var(--verde);border-color:var(--verde);color:#fff}
.stone{background:var(--papel-2);border:1px solid var(--linha);border-radius:14px;
  overflow:hidden;box-shadow:var(--sombra);margin-bottom:34px;scroll-margin-top:80px}
.stone-head{padding:26px 28px 22px;display:grid;grid-template-columns:1fr auto;gap:20px;
  align-items:start;border-bottom:1px solid var(--linha)}
.stone-head .idx{font-family:var(--mono);font-size:12px;color:var(--tinta-2);
  letter-spacing:.08em;margin-bottom:7px}
.stone-head h3{font-size:26px;margin:0 0 8px}
.stone-head .rocha{font-size:15px;color:var(--tinta-2);margin:0}
.badge{font-size:11.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
  padding:6px 11px;border-radius:6px;white-space:nowrap}
.b-sedimentar{background:#F3EAD9;color:#6E5326}
.b-igneia{background:#F8E3D8;color:#8E3F1F}
.b-metamorfica{background:#E4EAEF;color:#42525F}
.stone-body{padding:26px 28px}
.specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:0;
  border:1px solid var(--linha);border-radius:10px;overflow:hidden;margin-bottom:24px}
.spec{padding:13px 16px;border-right:1px solid var(--linha);border-bottom:1px solid var(--linha);
  background:#FDFCFA}
.spec dt{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--tinta-2);
  font-weight:700;margin-bottom:3px}
.spec dd{margin:0;font-size:15px;line-height:1.45}
.shots{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:14px;margin:0 0 22px}
.shot{margin:0;cursor:zoom-in;border-radius:9px;overflow:hidden;background:#EFEAE1;
  border:1px solid var(--linha);position:relative}
.shot img{width:100%;height:190px;object-fit:cover;transition:transform .5s cubic-bezier(.2,.7,.3,1)}
.shot:hover img{transform:scale(1.045)}
.shot figcaption{font-size:12.2px;line-height:1.45;color:var(--tinta-2);padding:9px 11px;
  background:var(--papel-2)}
.kindtag{position:absolute;top:8px;left:8px;font-size:10px;font-weight:700;
  letter-spacing:.06em;text-transform:uppercase;padding:3px 7px;border-radius:4px;
  background:rgba(28,26,23,.78);color:#fff}
.prose{font-size:15.8px;line-height:1.7;color:var(--tinta-2)}
.prose strong{color:var(--tinta)}
.prose p{margin:0 0 12px}
.minihead{font-size:11.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--verde-2);
  font-weight:700;margin:20px 0 7px}
.usobox{background:var(--verde-claro);border-left:3px solid var(--verde);border-radius:0 8px 8px 0;
  padding:13px 17px;font-size:15.2px;margin-top:18px}

/* ---------- table ---------- */
.tablewrap{overflow-x:auto;border:1px solid var(--linha);border-radius:12px;
  background:var(--papel-2);box-shadow:var(--sombra)}
table{border-collapse:collapse;width:100%;min-width:940px;font-size:14.4px}
th{background:var(--verde);color:#fff;text-align:left;padding:12px 14px;font-size:12px;
  letter-spacing:.07em;text-transform:uppercase;font-weight:700;white-space:nowrap}
td{padding:11px 14px;border-top:1px solid var(--linha);vertical-align:top}
tbody tr:nth-child(even){background:#FBFAF7}
tbody tr:hover{background:var(--verde-claro)}
td b{color:var(--verde)}
.fdot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px;
  vertical-align:middle}

/* ---------- timeline ---------- */
.tl{background:var(--papel-2);border:1px solid var(--linha);border-radius:14px;padding:26px 20px 14px;
  box-shadow:var(--sombra);overflow-x:auto}
.tl svg{display:block;min-width:900px;width:100%;height:auto}

/* ---------- temas ---------- */
.tema{display:grid;grid-template-columns:74px 1fr;gap:24px;padding:26px 0;
  border-top:1px solid var(--linha)}
.tema:first-child{border-top:0}
.tema .n{font-family:var(--serif);font-size:38px;line-height:1;color:#C9D6CE;font-weight:700}
.tema h3{margin-bottom:8px}
.tema p{font-size:15.8px;color:var(--tinta-2);margin:0;line-height:1.68}
.tema p strong{color:var(--tinta)}

/* ---------- campo ---------- */
.campo{display:grid;grid-template-columns:1fr;gap:0;background:var(--papel-2);
  border:1px solid var(--linha);border-radius:12px;overflow:hidden;box-shadow:var(--sombra)}
.campo-item{display:grid;grid-template-columns:230px 1fr 92px;gap:20px;padding:17px 22px;
  border-top:1px solid var(--linha);align-items:baseline}
.campo-item:first-child{border-top:0}
.campo-item .place{font-weight:600;font-size:15.5px;color:var(--verde)}
.campo-item .place span{display:block;font-weight:400;font-size:12.5px;color:var(--tinta-2)}
.campo-item p{margin:0;font-size:14.8px;color:var(--tinta-2);line-height:1.6}
.campo-item p strong{color:var(--tinta)}

/* ---------- bibliografia ---------- */
.biblio{font-size:15.3px;color:var(--tinta-2);line-height:1.66}
.biblio li{margin-bottom:13px;padding-left:4px}
.biblio strong{color:var(--tinta)}
.biblio em{color:var(--verde);font-style:italic}

/* ---------- notas ---------- */
.note{font-size:13.6px;color:var(--tinta-2);line-height:1.62}
.note code{font-family:var(--mono);font-size:12.4px;background:#EFEAE1;padding:2px 6px;
  border-radius:4px;color:var(--verde)}
.warn{background:#FBF3E4;border:1px solid #E9D7B4;border-radius:10px;padding:18px 22px;
  font-size:15px;color:#6E5326;margin-top:22px}
.warn strong{color:#5A3F17}

/* ---------- footer ---------- */
footer{background:#17382B;color:#B7CCC1;padding:52px 24px 64px;font-size:14px}
footer .wrap{max-width:1220px}
footer h4{font-family:var(--serif);color:#F2EFE8;font-size:20px;margin:0 0 12px}
footer a{color:#9FC4B2}
.credits{columns:2;column-gap:36px;font-size:12.6px;line-height:1.6}
.credits div{break-inside:avoid;margin-bottom:7px}

/* ---------- lightbox ---------- */
.lb{position:fixed;inset:0;background:rgba(16,14,12,.93);z-index:200;display:none;
  align-items:center;justify-content:center;padding:32px}
.lb.show{display:flex}
.lb img{max-width:100%;max-height:82vh;border-radius:8px;box-shadow:0 20px 70px rgba(0,0,0,.6)}
.lb .cap{color:#CFC9BF;font-size:13.5px;max-width:820px;margin-top:16px;text-align:center;line-height:1.55}
.lb .cap a{color:#9FC4B2}
.lb .x{position:absolute;top:20px;right:24px;font-size:34px;color:#E8E2D8;cursor:pointer;
  background:none;border:0;line-height:1;font-family:var(--sans)}
.lb .nav2{position:absolute;top:50%;transform:translateY(-50%);font-size:44px;color:#E8E2D8;
  cursor:pointer;background:none;border:0;padding:0 18px;opacity:.65}
.lb .nav2:hover{opacity:1}
.lb .p{position:absolute;left:50%;transform:translateX(-50%);bottom:24px;color:#8F887E;font-size:12.5px}

/* ---------- footer nav ---------- */
.totop{position:fixed;right:22px;bottom:22px;width:44px;height:44px;border-radius:50%;
  background:var(--verde);color:#fff;border:0;cursor:pointer;font-size:19px;
  box-shadow:0 6px 20px rgba(31,77,58,.32);opacity:0;pointer-events:none;transition:.25s;z-index:50}
.totop.show{opacity:1;pointer-events:auto}

@media (max-width:980px){
  .grid-3,.grid-2{grid-template-columns:1fr}
  .campo-item{grid-template-columns:1fr;gap:8px}
  .stone-head{grid-template-columns:1fr}
  .tema{grid-template-columns:1fr;gap:10px}
  .tema .n{font-size:28px}
  .credits{columns:1}
  .stat{padding-right:18px;margin-right:18px}
  .spec{border-right:1px solid var(--linha)}
}
@media print{
  .nav,.totop,.lb{display:none!important}
  body{background:#fff;font-size:12pt}
  .stone{break-inside:avoid;page-break-inside:avoid}
  section{padding:24px 0}
}
"""

JS = """
(function(){
  // scroll spy
  var links=[].slice.call(document.querySelectorAll('.nav-links a'));
  var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'));});
  function spy(){
    var y=window.scrollY+120,cur=0;
    secs.forEach(function(s,i){if(s&&s.offsetTop<=y)cur=i;});
    links.forEach(function(a,i){a.classList.toggle('on',i===cur);});
  }
  window.addEventListener('scroll',spy,{passive:true});spy();

  // filtro de pedras
  var btns=[].slice.call(document.querySelectorAll('.fbtn'));
  btns.forEach(function(b){b.addEventListener('click',function(){
    btns.forEach(function(x){x.classList.remove('on');});
    b.classList.add('on');
    var f=b.dataset.f;
    document.querySelectorAll('.stone').forEach(function(s){
      s.style.display=(f==='all'||s.dataset.fam===f)?'':'none';
    });
  });});

  // lightbox
  var lb=document.getElementById('lb'),lbi=lb.querySelector('img'),
      cap=lb.querySelector('.cap'),pos=lb.querySelector('.p');
  var allShots=[].slice.call(document.querySelectorAll('.shot'));
  var cur=0;
  function visible(){
    return allShots.filter(function(s){
      var st=s.closest('.stone');
      return !st || st.style.display!=='none';
    });
  }
  function open(i){
    var list=visible();
    if(!list.length)return;
    cur=i;var s=list[i],c=s.dataset.cap||'',
        a=s.dataset.author||'',l=s.dataset.lic||'',u=s.dataset.page||'';
    lbi.src=s.dataset.full;lbi.alt=c;
    cap.innerHTML=c+(u?'<br><a href="'+u+'" target="_blank" rel="noopener">'+a+' — '+l+'</a>':(a?'<br>'+a+' — '+l:''));
    pos.textContent=(i+1)+' / '+list.length;
    lb.classList.add('show');document.body.style.overflow='hidden';
  }
  function close(){lb.classList.remove('show');document.body.style.overflow='';}
  allShots.forEach(function(s){
    s.addEventListener('click',function(){
      var list=visible(),i=list.indexOf(s);
      open(i<0?0:i);
    });
  });
  lb.querySelector('.x').addEventListener('click',close);
  lb.addEventListener('click',function(e){if(e.target===lb)close();});
  lb.querySelector('.prev').addEventListener('click',function(e){
    e.stopPropagation();var l=visible();open((cur-1+l.length)%l.length);});
  lb.querySelector('.next').addEventListener('click',function(e){
    e.stopPropagation();var l=visible();open((cur+1)%l.length);});
  document.addEventListener('keydown',function(e){
    if(!lb.classList.contains('show'))return;
    var l=visible();
    if(e.key==='Escape')close();
    if(e.key==='ArrowLeft')open((cur-1+l.length)%l.length);
    if(e.key==='ArrowRight')open((cur+1)%l.length);
  });

  // topo
  var top=document.getElementById('totop');
  window.addEventListener('scroll',function(){top.classList.toggle('show',window.scrollY>700);});
  top.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
})();
"""


def esc(s):
    return html.escape(s, quote=True)


def build_timeline():
    """Linha do tempo geologica em SVG.
    Eixo com quebra: linear de 300 a 1 Ma, logaritmico de 1 Ma a 1 ka.
    Distribuicao de faixas com colisao resolvida por largura estimada do rotulo."""
    W = 1180
    x0, x1 = 60, W - 40
    xbrk = x0 + int((x1 - x0) * 0.74)      # fim do segmento linear
    y = 78
    A_MIN, A_MAX = 1.0, 310.0               # segmento linear (Ma)
    LOG_MAX = 3.0                          # 1 Ma -> 1 ka em escala log
    FONT = 12.3
    CHARW = 6.15
    PAD = 14

    def X(ma):
        if ma >= 1:
            return x0 + (A_MAX - ma) / (A_MAX - A_MIN) * (xbrk - x0)
        import math
        t = min(LOG_MAX, math.log10(1.0 / ma)) if ma > 0 else LOG_MAX
        return xbrk + t / LOG_MAX * (x1 - xbrk)

    marks = [
        ("Granitos variscanos", 285, "#7A3E2E"),
        ("Marmore de Macael (protolito)", 215, "#5B6B7C"),
        ("Porfiro vermelho de Yazd", 44, "#B4552F"),
        ("Pedra de la Floresta", 29, "#8A6A3D"),
        ("Metamorfismo alpino (Macael)", 16, "#5B6B7C"),
        ("Pedra de Montjuic", 13, "#8A6A3D"),
        ("Pedra de Calafell", 12, "#8A6A3D"),
        ("Basalto de Bagnoregio", 0.7, "#B4552F"),
        ("Basalto de Castellfollit", 0.21, "#B4552F"),
        ("Travertino de Tivoli", 0.125, "#8A6A3D"),
    ]
    marks.sort(key=lambda m: -m[1])

    lanes = []
    placed = []
    for label, ma, col in marks:
        x = X(ma)
        w = len(label) * CHARW
        if x > W - 230:
            left, right = x - w - PAD, x + PAD
        elif x < x0 + 180:
            left, right = x - PAD, x + w + PAD
        else:
            left, right = x - w / 2 - PAD, x + w / 2 + PAD
        lane = None
        for i, occ in enumerate(lanes):
            if all(right < o0 - 8 or left > o1 + 8 for o0, o1 in occ):
                lane = i
                break
        if lane is None:
            lanes.append([])
            lane = len(lanes) - 1
        lanes[lane].append((left, right))
        placed.append((label, ma, col, x, lane))

    nlanes = max(1, len(lanes))
    H = y + 52 + nlanes * 23 + 50

    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Linha do tempo geologica das pedras da Sagrada Familia">']
    s.append('<defs><linearGradient id="tlg" x1="0" x2="1">'
             '<stop offset="0" stop-color="#B4552F"/><stop offset="0.42" stop-color="#8A6A3D"/>'
             '<stop offset="1" stop-color="#1F4D3A"/></linearGradient>'
             '<linearGradient id="tlg2" x1="0" x2="1">'
             '<stop offset="0" stop-color="#1F4D3A"/><stop offset="1" stop-color="#6FAE8F"/>'
             '</linearGradient></defs>')
    # eixo: segmento linear
    s.append(f'<line x1="{x0}" y1="{y}" x2="{xbrk-7}" y2="{y}" stroke="url(#tlg)" stroke-width="3"/>')
    # eixo: segmento logaritmico
    s.append(f'<line x1="{xbrk+7}" y1="{y}" x2="{x1}" y2="{y}" stroke="url(#tlg2)" stroke-width="3"/>')
    # quebra de eixo
    s.append(f'<path d="M{xbrk-7},{y-6} l7,6 l-7,6 l7,6 l-7,6" fill="none" stroke="#9C9488" stroke-width="1.5"/>')

    for ma in (300, 250, 200, 150, 100, 50, 25, 10, 5, 1):
        x = X(ma)
        s.append(f'<line x1="{x:.1f}" y1="{y-5}" x2="{x:.1f}" y2="{y+5}" stroke="#B9B2A6" stroke-width="1.4"/>')
        s.append(f'<text x="{x:.1f}" y="{y+22}" font-size="11" fill="#8A8378" '
                 f'text-anchor="middle" font-family="system-ui,sans-serif">{ma} Ma</text>')
    for ma, lbl in ((1, "1 Ma"), (0.1, "100 ka"), (0.01, "10 ka")):
        x = X(ma)
        s.append(f'<line x1="{x:.1f}" y1="{y-5}" x2="{x:.1f}" y2="{y+5}" stroke="#B9B2A6" stroke-width="1.4"/>')
        s.append(f'<text x="{x:.1f}" y="{y+22}" font-size="11" fill="#8A8378" '
                 f'text-anchor="middle" font-family="system-ui,sans-serif">{lbl}</text>')
    s.append(f'<text x="{x1}" y="{y+22}" font-size="11" fill="#8A8378" '
             f'text-anchor="end" font-family="system-ui,sans-serif">hoje</text>')
    s.append(f'<text x="{x0-14}" y="{y+4}" font-size="11" fill="#8A8378" text-anchor="end" '
             f'font-family="system-ui,sans-serif">Ma</text>')

    for label, ma, col, x, lane in placed:
        ly = y + 52 + lane * 23
        s.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{ly-10:.1f}" stroke="{col}" '
                 f'stroke-width="1.2" stroke-dasharray="2 3" opacity=".6"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y}" r="5.5" fill="{col}" stroke="#FAF8F4" stroke-width="1.8"/>')
        anchor = "end" if x > W - 230 else ("start" if x < x0 + 180 else "middle")
        dx = {"end": -8, "start": 8, "middle": 0}[anchor]
        s.append(f'<text x="{x+dx:.1f}" y="{ly:.1f}" font-size="{FONT}" fill="#33302B" '
                 f'text-anchor="{anchor}" font-family="system-ui,sans-serif">{esc(label)}</text>')
        age = f"~{ma} Ma" if ma >= 1 else f"~{int(ma*1000)} ka"
        s.append(f'<text x="{x+dx:.1f}" y="{ly+13:.1f}" font-size="10.6" fill="#8A8378" '
                 f'text-anchor="{anchor}" font-family="system-ui,sans-serif">{age}</text>')
    s.append(f'<text x="{x0}" y="{H-12}" font-size="11.5" fill="#8A8378" '
             f'font-family="system-ui,sans-serif">Escala com quebra: linear de 300 a 1 Ma; '
             f'logaritmica (de 1 Ma a 1 ka) no segmento final, onde se concentram as rochas '
             f'vulcanicas mais recentes. As pedras do templo cobrem quase 300 000 000 de anos.</text>')
    s.append("</svg>")
    return "".join(s)


def build_resistance_chart():
    """Barras horizontais da resistencia a compressao (MPa)."""
    data = [(s["nome"].split(" (")[0], float(s["mpa"]), s["familia"]) for s in STONES if s["mpa"] != "—"]
    data.sort(key=lambda r: r[1])
    if not data:
        return ""
    col = {"sedimentar": "#8A6A3D", "igneia": "#B4552F", "metamorfica": "#5B6B7C"}
    W = 1180
    rowh = 34
    H = 46 + rowh * len(data) + 26
    maxv = 200.0
    x0, x1 = 300, W - 90
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Resistencia a compressao das pedras do templo">']
    for g in (0, 50, 100, 150, 200):
        x = x0 + g / maxv * (x1 - x0)
        s.append(f'<line x1="{x:.1f}" y1="30" x2="{x:.1f}" y2="{H-26:.1f}" stroke="#E7E1D7" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="20" font-size="10.5" fill="#8A8378" text-anchor="middle" '
                 f'font-family="system-ui,sans-serif">{g}</text>')
    s.append(f'<text x="{x1}" y="20" font-size="10.5" fill="#8A8378" text-anchor="end" '
             f'font-family="system-ui,sans-serif">MPa</text>')
    for i, (name, v, fam) in enumerate(data):
        y = 38 + i * rowh
        w = v / maxv * (x1 - x0)
        s.append(f'<text x="{x0-12}" y="{y+14}" font-size="13" fill="#33302B" text-anchor="end" '
                 f'font-family="system-ui,sans-serif">{esc(name)}</text>')
        s.append(f'<rect x="{x0}" y="{y}" width="{w:.1f}" height="19" rx="3" fill="{col[fam]}" opacity=".88"/>')
        s.append(f'<text x="{x0+w+8:.1f}" y="{y+14}" font-size="12" fill="#5A554E" '
                 f'font-family="system-ui,sans-serif">{v:g} MPa</text>')
    s.append(f'<text x="{x0}" y="{H-8}" font-size="11.5" fill="#8A8378" '
             f'font-family="system-ui,sans-serif">Resistencia a compressao uniaxial '
             f'(kg/cm2 convertidos a MPa). Fonte: itinerario petrografico do Museu de Geologia de Barcelona (2005).</text>')
    s.append("</svg>")
    return "".join(s)


def build_site(manifest):
    byid = {m["id"]: m for m in manifest}

    # --------- cartoes de pedra ---------
    stones_html = []
    for n, st in enumerate(STONES, 1):
        specs = [
            ("Classificação", st["classificacao"]),
            ("Idade", f'{st["idade"]} · <b>{st["ma"]}</b>'),
            ("Ambiente de origem", st["origem"]),
            ("Pedreira / local", st["local"]),
            ("Coordenadas", st["coords"]),
            ("Distância ao templo", st["dist"]),
            ("Densidade", st["rho"]),
            ("Resistência à compressão", st["rc"] + (f' · {st["mpa"]} MPa' if st["mpa"] != "—" else "")),
        ]
        spec_html = "".join(
            f'<div class="spec"><dt>{esc(k)}</dt><dd>{v}</dd></div>' for k, v in specs)
        stones_html.append(f"""
<article class="stone" id="pedra-{st['id']}" data-fam="{st['familia']}">
  <div class="stone-head">
    <div>
      <div class="idx">PEDRA {n:02d} / {len(STONES):02d}</div>
      <h3>{esc(st['nome'])}</h3>
      <p class="rocha">{esc(st['rocha'])} — {esc(st['classificacao'])}</p>
    </div>
    <span class="badge b-{st['familia']}">{esc(st['familia_label'])}</span>
  </div>
  <div class="stone-body">
    <dl class="specs">{spec_html}</dl>
    <div class="shots">{''.join(shots_html_for(st, byid))}</div>
    <div class="prose">
      <div class="minihead">Textura</div><p>{st['textura']}</p>
      <div class="minihead">Composição mineralógica</div><p>{st['mineralogia']}</p>
      <div class="minihead">Processo geológico</div><p>{st['processo']}</p>
      <div class="minihead">Aplicação no templo</div><p>{st['uso']}</p>
      <div class="usobox"><strong>Em resumo —</strong> {st['destaque']}</div>
    </div>
  </div>
</article>""")

    # --------- tabela-sintese ---------
    famcol = {"sedimentar": "#8A6A3D", "igneia": "#B4552F", "metamorfica": "#5B6B7C"}
    rows = []
    for st in STONES:
        rows.append(
            f'<tr><td><span class="fdot" style="background:{famcol[st["familia"]]}"></span>'
            f'<b>{esc(st["nome"])}</b></td>'
            f'<td>{esc(st["rocha"])}</td><td>{esc(st["ma"])}</td>'
            f'<td>{esc(st["local"])}</td><td>{esc(st["dist"])}</td>'
            f'<td>{esc(st["rc"])}</td></tr>')

    # --------- contexto galeria ---------
    ctx_ids = ["ctx-mapa-variscano", "ctx-orogenia", "ctx-collserola",
               "ctx-montjuic-pedreira", "ctx-montjuic-vista"]
    ctx_html = "".join(
        f'<figure class="shot" data-full="{byid[i]["file"]}" data-cap="{esc(byid[i]["caption"])}" '
        f'data-author="{esc(byid[i]["author"])}" data-lic="{esc(byid[i]["license"])}" data-page="{byid[i]["page"]}">'
        f'<img src="{byid[i]["file"]}" alt="{esc(byid[i]["caption"][:90])}" loading="lazy">'
        f'<figcaption>{esc(byid[i]["caption"])}</figcaption></figure>'
        for i in ctx_ids if i in byid)

    tmpl_ids = ["tmpl-nascimento", "tmpl-nascimento-cc0", "tmpl-coluna-evangelista",
                "tmpl-colunas", "tmpl-interior", "tmpl-nau", "tmpl-paixao"]
    tmpl_html = "".join(
        f'<figure class="shot" data-full="{byid[i]["file"]}" data-cap="{esc(byid[i]["caption"])}" '
        f'data-author="{esc(byid[i]["author"])}" data-lic="{esc(byid[i]["license"])}" data-page="{byid[i]["page"]}">'
        f'<img src="{byid[i]["file"]}" alt="{esc(byid[i]["caption"][:90])}" loading="lazy">'
        f'<figcaption>{esc(byid[i]["caption"])}</figcaption></figure>'
        for i in tmpl_ids if i in byid)

    # --------- familias ---------
    fam_html = ""
    for key, title, txt, c in FAMILIAS:
        names = [s["nome"].split(" (")[0] for s in STONES if s["familia"] == key]
        pills = "".join(f'<span class="pill">{esc(n)}</span>' for n in names)
        fam_html += f'<div class="card"><span class="tag" style="background:{c}1A;color:{c}">{esc(title)}</span>'
        fam_html += f'<p>{txt}</p><div>{pills}</div></div>'

    # --------- temas ---------
    temas_html = "".join(
        f'<div class="tema"><div class="n">{n}</div><div><h3>{esc(t)}</h3><p>{p}</p></div></div>'
        for n, t, p in TEMAS)

    # --------- campo ---------
    campo_html = "".join(
        f'<div class="campo-item"><div class="place">{esc(n)}<span>{esc(loc)}</span></div>'
        f'<p>{d}</p><div><span class="pill">{esc(k)}</span></div></div>'
        for n, loc, d, k in CAMPO)

    # --------- metodo / biblio ---------
    metodo_html = "".join(
        f'<div class="campo-item"><div class="place">{esc(t)}</div><p>{d}</p><div></div></div>'
        for t, d in METODO)
    biblio_html = "".join(
        f'<li><strong>{a}</strong> {t} <em>{c}</em></li>' for a, t, c in BIBLIO)

    # --------- creditos ---------
    seen = set()
    cred = []
    for m in manifest:
        key = (m["title"], m["license"])
        if key in seen:
            continue
        seen.add(key)
        a = m["author"] or "Autoria não identificada"
        if len(a) > 90:
            a = a[:87] + "…"
        lic = m["license"]
        if m.get("license_url"):
            lic = f'<a href="{m["license_url"]}" target="_blank" rel="noopener">{esc(lic)}</a>'
        else:
            lic = esc(lic)
        cred.append(f'<div><a href="{m["page"]}" target="_blank" rel="noopener">'
                    f'{esc(m["title"][:64])}</a> — {esc(a)}, {lic}</div>')

    fam_tabs = "".join(
        f'<button class="fbtn{" on" if k=="all" else ""}" data-f="{k}">{lbl}</button>'
        for k, lbl in [("all", "Todas as pedras"), ("sedimentar", "Sedimentares"),
                       ("igneia", "Ígneas"), ("metamorfica", "Metamórficas")])

    return f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>As pedras da Sagrada Família — geologia, idades e proveniências</title>
<meta name="description" content="Trabalho de geologia sobre os tipos de pedra, idades e pedreiras de origem utilizados na construção da Sagrada Família de Barcelona.">
<style>{CSS}</style>
</head>
<body>

<nav class="nav">
  <div class="nav-in">
    <a class="brand" href="#topo">Sagrada Família<small>geologia das pedras</small></a>
    <div class="nav-links">
      <a href="#contexto">Contexto</a>
      <a href="#templo">O templo</a>
      <a href="#familias">Famílias</a>
      <a href="#pedras">As pedras</a>
      <a href="#tempo">Linha do tempo</a>
      <a href="#tabela">Tabela</a>
      <a href="#resistencia">Resistência</a>
      <a href="#temas">Leitura crítica</a>
      <a href="#campo">Campo</a>
      <a href="#metodo">Método</a>
      <a href="#biblio">Bibliografia</a>
    </div>
  </div>
</nav>

<header class="hero" id="topo">
  <div class="hero-in">
    <div class="eyebrow">Trabalho de geologia · Curso de Arquitetura</div>
    <h1>As pedras<br>da Sagrada Família</h1>
    <p class="lead">Que rochas construíram a basílica, com que idade e de que pedreira saíram?
      Do granito de 285 milhões de anos do Vallès ao travertino de 125 mil anos de Tivoli:
      uma geologia de materiais que atravessa 300 milhões de anos e quatro continentes.</p>
    <div class="stats">
      <div class="stat"><b>{len(STONES)}</b><span>pedras distintas</span></div>
      <div class="stat"><b>~40</b><span>pedreiras</span></div>
      <div class="stat"><b>300 Ma</b><span>de amplitude temporal</span></div>
      <div class="stat"><b>150 000 m³</b><span>de material</span></div>
      <div class="stat"><b>~60</b><span>tipos de pedra</span></div>
    </div>
  </div>
</header>

<section id="contexto">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">01 · Enquadramento</div>
      <h2>Barcelona é um menu de matérias-primas</h2>
      <p class="lead">O templo assenta sobre três afloramentos rochosos distintos dentro da cidade
        — e cada um deles fornece uma família de pedras diferente.</p>
    </div>
    <div class="grid-3" style="margin-bottom:28px">
      <div class="card"><span class="tag" style="background:#1F4D3A1A;color:#1F4D3A">Collserola (NW)</span>
        <p>Substrato paleozoico (filites e xistos do Ordovício–Carbonífero) metamorfizado na orogénese
          varisca, e granitoides tardivariscanos. <strong>Daqui saem os granitos</strong> — Òrrius,
          «ull de serp».</p></div>
      <div class="card"><span class="tag" style="background:#8A6A3D1A;color:#8A6A3D">Montjuïc (S)</span>
        <p>Bloco tectónico inclinado de sedimentos deltaícos miocénicos (~15–11 Ma), silicificados.
          <strong>Daqui sai o arenito</strong> — a pedra-mãe do templo, explorada desde Roma até 1957.</p></div>
      <div class="card"><span class="tag" style="background:#B4552F1A;color:#B4552F">Pla de Barcelona</span>
        <p>Semiencavamento preenchido por sedimentos pliocénicos e quaternários (deltas do Llobregat
          e do Besòs). Substrato mole — e <strong>as rochas vulcânicas da Garrotxa</strong> fornecem
          o basalto, a 95 km.</p></div>
    </div>
    <div class="shots">{ctx_html}</div>
    <div class="warn" style="margin-top:26px">
      <strong>Nota importante sobre o basalto de Collserola.</strong> A pedra de Sant Martí de Sarroca
      (Collserola) étightly associada a Gaudí, mas é usada no <strong>Park Güell</strong> (átrio,
      colunas, portal da Finca Güell) e em Bellesguard — <strong>não</strong> na Sagrada Família.
      No templo, o basalto é <strong>italiano</strong> (Bagnoregio) e <strong>catalão da Garrotxa</strong>
      (Castellfollit de la Roca).
    </div>
  </div>
</section>

<section id="templo">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">02 · O templo</div>
      <h2>Onde cada pedra se vê</h2>
      <p class="lead">A pedra não é um material neutro: a escolha da cor, do grão e da resistência
        organiza o efeito do edifício. A fachada do Nascimento é uma parede de arenito; o interior
        é um bosque de colunas de cinco rochas diferentes.</p>
    </div>
    <div class="shots">{tmpl_html}</div>
  </div>
</section>

<section id="familias">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">03 · Classificação</div>
      <h2>Três famílias de rochas</h2>
      <p class="lead">O critério não é geográfico nem decorativo: é o processo que formou a rocha.
        É essa a chave de leitura de todo o conjunto.</p>
    </div>
    <div class="grid-3">{fam_html}</div>
  </div>
</section>

<section id="pedras">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">04 · As pedras</div>
      <h2>Treze pedras, treze histórias geológicas</h2>
      <p class="lead">Cada pedra é apresentada com a sua ficha técnica, a sua petrografia,
        o processo que a formou e o lugar exacto onde entra na obra.
        <strong>Clique numa imagem</strong> para a ver em tamanho completo.</p>
    </div>
    <div class="filters">{fam_tabs}</div>
    {''.join(stones_html)}
  </div>
</section>

<section id="tempo">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">05 · Tempo</div>
      <h2>Uma linha do tempo geológica</h2>
      <p class="lead">A escala geológica é o que a tabela esconde. Colocando as pedras na mesma
        régua temporal, o templo deixa de ser um edifício e passa a ser um corte geológico.</p>
    </div>
    <div class="tl">{build_timeline()}</div>
  </div>
</section>

<section id="tabela">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">06 · Síntese</div>
      <h2>Tabela comparativa</h2>
      <p class="lead">Ordenada como no itinerário petrográfico do Museu de Geologia de Barcelona (2005).</p>
    </div>
    <div class="tablewrap">
      <table>
        <thead><tr><th>Pedra</th><th>Rochas</th><th>Idade</th><th>Procedência</th>
          <th>Distância</th><th>Resistência</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
  </div>
</section>

<section id="resistencia">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">07 · Comportamento mecânico</div>
      <h2>Resistência à compressão</h2>
      <p class="lead">O gráfico mostra a dispersão: de 7 MPa (pedra de Calafell, a mais frágil)
        a 190 MPa (pórfiro de Yazd, a mais resistente). <strong>E mostra que a resistência
        não determina o uso.</strong></p>
    </div>
    <div class="tl">{build_resistance_chart()}</div>
  </div>
</section>

<section id="temas">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">08 · Leitura crítica</div>
      <h2>Cinco temas para desenvolver</h2>
      <p class="lead">A descrição é o ponto de partida. O trabalho ganha corpo na leitura
        crítica — na pergunta sobre <em>porquê</em> e <em>para quê</em>.</p>
    </div>
    {temas_html}
  </div>
</section>

<section id="campo">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">09 · Trabalho de campo</div>
      <h2>Onde ir ver isto</h2>
      <p class="lead">Sete destinos que cobrem rochas, petrografia e logística da obra —
        todos acessíveis e todos com conteúdo geológico demonstrável.</p>
    </div>
    <div class="campo">{campo_html}</div>
  </div>
</section>

<section id="metodo">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">10 · Método</div>
      <h2>Como se estuda uma pedra de construção</h2>
      <p class="lead">Protocolo de campo e de laboratório aplicável a qualquer das pedras
        deste conjunto.</p>
    </div>
    <div class="campo">{metodo_html}</div>

    <div class="sec-head" style="margin-top:56px">
      <div class="kicker">11 · Notas e limitações</div>
      <h2>Sobre este trabalho</h2>
    </div>
    <div class="card prose">
      <p><strong>Fontes das imagens.</strong> Todas as fotografias provêm da Wikimedia Commons
        e são reproduzidas sob as licenças indicadas em cada legenda (CC BY, CC BY-SA, CC0 ou
        domínio público). A atribuição completa consta na secção de créditos, no rodapé.</p>
      <p><strong>Fotografia exacta versus fotografia representativa.</strong> Quando existe
        fotografia do local de extracção ou da rocha na obra, a legenda está assinalada
        <em>«Local de origem»</em>. Quando só foi possível obter uma fotografia do
        <strong>tipo de rocha</strong> — por não haver imagens do material comercial específico
        em regime de direitos livres — a legenda está assinalada <em>«Tipo de rocha»</em>,
        e o texto da mesma explica a equivalência petrográfica. Os dados de densidade e
        resistência provêm do itinerário petrográfico do Museu de Geologia de Barcelona (2005);
        as idades absolutas, de fontes geocronológicas regionais (veja bibliografia).</p>
      <p><strong>Dados de campo.</strong> As coordenadas e as distâncias ao templo são
        aproximadas, calculadas a partir da pedreira de referência de cada pedra e do
        centro do templo (41.4036° N, 2.1744° E).</p>
      <p><strong>Limites.</strong> As datações radiométricas das rochas vulcânicas da
        Garrotxa foram revistas em 2025 e reviram a ordem de grandeza do vulcanismo.
        As idades das rochas sedimentares referem-se ao protólito e não preservam
        a alteração diagenética posterior.</p>      <p><strong>Reprodução.</strong> As imagens podem ser obtidas de novo com
        <code>python make_sf_images.py</code>; o site com <code>python make_sf_site.py</code>.</p>
    </div>
  </div>
</section>

<section id="biblio">
  <div class="wrap">
    <div class="sec-head">
      <div class="kicker">12 · Bibliografia</div>
      <h2>Fontes</h2>
    </div>
    <ul class="biblio">{biblio_html}</ul>
  </div>
</section>

<footer>
  <div class="wrap">
    <h4>As pedras da Sagrada Família</h4>
    <p style="max-width:640px;margin:0 0 26px;color:#C3D5CB">
      Trabalho de geologia para o curso de Arquitetura. Conteúdo redigido em português europeu,
      a partir da bibliografia científica indicada. Imagens da Wikimedia Commons, sob as
      licenças assinaladas em cada legenda.
    </p>
    <p style="font-size:12.5px;color:#8FAE9F;margin:0 0 12px">
      <strong style="color:#C3D5CB">Atribuição das imagens</strong> — autor, licença (com ligação)
      e endereço original de cada ficheiro. Todas as fotografias foram redimensionadas
      para 1024 px de largura, o que constitui a única alteração efetuada.
    </p>
    <div class="credits">{''.join(cred)}</div>
    <p style="font-size:12.5px;color:#7E9D8E;margin:26px 0 0;border-top:1px solid rgba(255,255,255,.14);padding-top:18px">
      Geometria dos dados: Museu de Geologia de Barcelona · IGME/MAGNA · IDAEA-CSIC (2025) ·
      Junta Constructora del Temple de la Sagrada Família. Gerado a 2026-10-21.<br><br>
      <strong style="color:#C3D5CB">Licença deste site</strong> — <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pt" target="_blank" rel="noopener">CC BY-SA 4.0</a>.
      Uma vez que incorpora imagens sob licenças CC BY-SA, esta obra é disponibilizada
      sob a mesma licença.
    </p>
  </div>
</footer>

<button class="totop" id="totop" aria-label="Voltar ao topo">&uarr;</button>

<div class="lb" id="lb">
  <button class="x" aria-label="Fechar">&times;</button>
  <button class="nav2 prev" aria-label="Anterior">&#8249;</button>
  <button class="nav2 next" aria-label="Seguinte">&#8250;</button>
  <div style="max-width:100%">
    <img src="" alt="">
    <div class="cap"></div>
  </div>
  <div class="p"></div>
</div>

<script>{JS}</script>
</body>
</html>
"""


def shots_html_for(st, byid):
    out = []
    for iid in st["imgs"]:
        m = byid.get(iid)
        if not m:
            continue
        kindtag = ('<span class="kindtag">Local de origem</span>' if m["kind"] == "exata"
                   else '<span class="kindtag">Tipo de rocha</span>')
        out.append(
            f'<figure class="shot" data-full="{m["file"]}" data-cap="{esc(m["caption"])}" '
            f'data-author="{esc(m["author"])}" data-lic="{esc(m["license"])}" data-page="{m["page"]}">'
            f'{kindtag}<img src="{m["file"]}" alt="{esc(m["caption"][:90])}" loading="lazy">'
            f'<figcaption>{esc(m["caption"])}</figcaption></figure>')
    return "".join(out)


def main():
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    out = build_site(manifest)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"OK -> {OUT}  ({len(out)/1024:.1f} KB, {len(manifest)} imagens referenciadas)")


if __name__ == "__main__":
    main()
