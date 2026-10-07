from PIL import Image, ImageDraw, ImageFont
import os
BASE = r"C:\Users\diogo\OneDrive\Documentos\Projeto Padrão"
def F(sz, bold=False):
    try:
        p = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
        return ImageFont.truetype(p, sz)
    except Exception:
        return ImageFont.load_default()
def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur+" "+w).strip()
        try:
            ok = d.textlength(t, font=fnt) <= maxw
        except Exception:
            ok = len(t) < 40
        if ok:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or [""]
def render(path, title, subtitle, headers, rows, colw, fs=21, merges=None):
    fh, fr, fb = F(fs+3, True), F(fs, False), F(fs, True)
    pad = 12
    lh = int(fs*1.35)
    tmp = Image.new("RGB",(10,10)); d0 = ImageDraw.Draw(tmp)
    head = [wrap(d0, h, fh, colw[j]-2*pad) for j,h in enumerate(headers)]
    data = []
    for r in rows:
        cells = []
        for j,c in enumerate(r):
            f = fb if j in (0,1) else fr
            cells.append(wrap(d0, c, f, colw[j]-2*pad))
        data.append(cells)
    t1 = wrap(d0, title, F(32,True), sum(colw)-40)
    t2 = wrap(d0, subtitle, F(21,False), sum(colw)-40)
    th_title = len(t1)*42 + len(t2)*29 + 36
    th = max(len(h) for h in head)*(lh+4) + 2*pad
    row_h = [max(len(c) for c in cells)*lh + 2*pad + 6 for cells in data]
    W = sum(colw)+2*pad
    H = th_title + th + sum(row_h) + 34
    img = Image.new("RGB",(W,H),"white"); d = ImageDraw.Draw(img)
    y = pad
    for line in t1:
        d.text((pad+10,y), line, fill=(31,77,58), font=F(32,True)); y+=42
    for line in t2:
        d.text((pad+10,y), line, fill=(90,90,90), font=F(21,False)); y+=29
    y+=8
    x=pad
    for j in range(len(headers)):
        d.rectangle([x,y,x+colw[j],y+th], fill=(31,77,58))
        ly=y+8
        for line in head[j]:
            d.text((x+pad,ly), line, fill="white", font=fh); ly+=lh+4
        x+=colw[j]
    y+=th
    ytop = y
    pal = {"s":(238,247,238),"w":(254,243,239),"o":(238,245,250),"t":(255,248,225),"e":(244,250,247)}
    key = ["","", "s","w","o","t","e"]
    yrows = []
    for i,cells in enumerate(data):
        h=row_h[i]; x=pad
        yrows.append(y)
        for j,lines in enumerate(cells):
            bg=(244,250,247) if j==0 else pal.get(key[j],(255,255,255))
            d.rectangle([x,y,x+colw[j],y+h], fill=bg, outline=(175,185,180))
            f = fb if j in (0,1) else fr
            if j==0 and merges:
                x+=colw[j]
                continue
            ly=y+8
            for line in lines:
                d.text((x+pad,ly), line, fill=(25,25,25), font=f); ly+=lh
            x+=colw[j]
        y+=h
    if merges:
        for mi,(a,b,label) in enumerate(merges):
            y0 = yrows[a]; y1 = yrows[b-1]+row_h[b-1]
            x0 = pad; x1 = pad+colw[0]
            fill = (228,242,228)
            d.rectangle([x0,y0,x1,y1], fill=fill, outline=(31,77,58), width=3)
            fbig = F(26,True)
            tw = d.textlength(label, font=fbig)
            th0 = 30
            tmp2 = Image.new("RGBA",(int(tw)+20, th0+10),(0,0,0,0))
            dd = ImageDraw.Draw(tmp2)
            dd.text((10,5), label, fill=(31,77,58), font=fbig)
            rot = tmp2.rotate(90, expand=True)
            rx = x0 + (colw[0]-rot.size[0])//2
            ry = y0 + (y1-y0-rot.size[1])//2
            img.paste(rot,(rx,ry),rot)
    d.text((pad+10,H-22), "Conforto e Eficiência Ambiental | IPMA 91-20 | APA-REA | CNPGB Apartadura | Givoni 1992/Lamberts | PME Portalegre", fill=(120,120,120), font=F(17,False))
    img.save(path)
    print("saved", path, img.size)
H = ["Áreas","Tópicos","Pontos Fortes","Pontos Fracos","Oportunidades","Ameaças","Estratégias"]
CW = [150,170,330,330,330,330,330]
macro = [
["MACROESTRUTURA Natural","Topografia","Relevo serra >800 m, patamar 400-500 m, peneplanície 300-400 m. N fresco/húmido, S quente. Amplitude 14°C em julho.","Cabeço exposto ao vento. Taludes e escarpas com aluimentos (PME).","Ganho solar a S, proteção a N, corta-vento sem fechar brisa de verão.","Taludes instáveis no chuvoso jan-fev. Sem carta distrital pública.","Implantar no patamar/cabeço drenado. Travar taludes. Estar a S, fechar a N."],
["","Fauna e Flora","Montado sobro+azinho 50-100/ha. Galeria ripícola arrefece. PNSSM 55 mil ha, 800+ espécies. Cortiça isolante.","Esteval combustível. Regeneração <40-50% em risco. Pressão humana.","Nativas para sombra: sobreiro perene + negral caduco (sol de inverno).","70% do montado ameaçado por calor + solo seco. Eucaliptal aumenta fogo.","Mapear e preservar nativas. Faixa PMDFCI. Sem esteval colado à casa."],
["","Dinâmica da água e Solo","Divisor Tejo/Guadiana. Barragens Caia 203, Maranhão 205, Apartadura 7,5 hm³. Regadios Caia/Sorraia.","Verão colapsa a sul do Tejo. Maciço Antigo débil. Solo descoberto. Sem erosão distrital.","Zonas permeáveis, cisterna, gota-a-gota. Crato PRR + adução Nisa-Caia.","Torrencialidade 80 m³/s em 8,4 km². Compactação reduz infiltração.","Preservar vegetação e galeria. Nada no leito de cheia (REN)."],
["","Fenómenos de risco","PME lista riscos. PMDFCI existe. Precedente Apartadura e 80 M€.","Fogo 809/20938 ha 08-25 pico jul-ago. Cheia jan-fev. 79% sem antissísmica.","Cintar/travar, elevar, faixa, evaporativo contra vento/fogo/cheia/sismo.","8 concelhos em alto/muito alto. Calor no PME. Sismo máx 4,1 Évora 98.","Casa fora da cheia e do talude. Vegetação + obra reduzem vento e fogo."],
["","Singularidades e Marcos","Cristas quartzíticas, patamar de Portalegre, galerias e nascentes.","Encosta N com menos sol de inverno.","Enquadrar serra a N e abrir estar a S: vista + sol.","Expansão pode tapar cristas e corredores frescos.","Vãos S para ganho, vãos N controlados para vista e cruzada."],
["Construída","Estruturas edificadas","Núcleo em cabeço, baixos caiados, granito/taipa. Pouco impacto.","Expansão no vale em cheia. Adobe vulnerável ao sismo.","Reabilitar sem tapar vista. Isolar cobertura a cortiça.","Construir demais no vale = cheia + sem ventilação.","Posição e altura integradas. Consolidar antes de expandir."],
["","Usos e funções","Ambiente tranquilo de monte/herdade. Vivência dentro-fora.","Pouca variedade de usos.","Pátio privado, sombra e silêncio como programa.","Lote muito aberto = exposição e isolamento.","Pátio, sombra e água com privacidade."],
["","Acessibilidades","Caminhos rurais e EN para vilas e barragens (confirmar no local).","Transporte e serviços escassos no disperso (verificar).","Acesso direto permite faixa, drenagem e obra.","Acesso limitado atrasa socorro em fogo/cheia.","Levantar acessos, larguras e água de defesa antes do projeto."],
["","Singularidades e Marcos","Privacidade com pouca vizinhança. Muros, socalcos, lagares.","Afastamento do centro e de recursos (verificar).","Vegetação para privacidade + vãos para natureza + cruzada.","Programa sem apoio próximo se não levantado.","Privacidade e vegetação para ventilar e sombrear."],
]
perc = [
["ESTRUTURA PERCETIVA","Microclimática","Altitude 400-600 m. N fresco/húmido, S quente/seco. Amplitude 14°C. Bom sol a sul.","Vento no cabeço e a norte. N com pouco sol de inverno. 31°C no verão.","Sol para aquecer no inverno, inércia para arrefecer no verão.","Vento norte e calor seco (HR 47%) pedem vãos estratégicos.","Abrigar a N, abrir a S/SE. Corta-vento permeável + pátio/água."],
["","Vistas endógenas","Montado, olival, galeria e cristas. Sombra e identidade no lote.","Esteval denso fecha vista e traz fogo.","Verde qualificado com nativas (sombro + caduco).","—","Enquadrar montado e serra. Faixa limpa junto à casa."],
["","Vistas exógenas","Vista serra-planície sem invasões. Horizonte de cabeço.","Poente/sul pode perder privacidade no vale.","Cortina vegetal para privacidade e valor.","Futuras obras podem fechar vista e privacidade.","Cortina densa a poente. Aberturas altas para vista livre."],
["","Paleta e material","Granito/quartzito + taipa/adobe + cal + cortiça + verde/ocre.","Só reboco industrial cansa e destoa.","Materiais locais pelo desempenho térmico e cor.","Sol/chuva desgastam. Obra descaracterizada.","Gestão ambiental e materiais naturais."],
]
clima = [
["CLIMA Bioclimática","Percurso solar","Muito sol. Sul ganha no inverno, norte fresco no verão.","Norte com vista mas sem radiação. Sul sem pala sobreaquece.","Sul para inverno, norte fresco para quartos no verão.","Frio (mín 5,8; extr. -4,5) se o sul for pequeno.","Vãos S/SE com pala/portada. Poucos a N."],
["","Sombreamento","Inverno quer sol dentro, verão quer sombra total.","Sem controlo sobreaquece (31°C) ou perde sol de inverno.","Palas, pérgola caduca e portadas sazonais.","Desconforto sem sombrear S/SO.","Pala a sul + caduca. Estore fora, não vidro escuro."],
["","Temperatura","Amena quase todo o ano. Mai/out em conforto. Noites a 17,8 em ago.","Picos 31-42°C de dia, 6°C à noite no inverno.","Sol + massa no inverno. Massa + noite no verão.","Fora do conforto nos picos de verão e inverno.","Taipa/granito + cruzada/noturna. Cortiça na cobertura."],
["","Humidade relativa","Frio com 75-79% guarda água no solo. Seco com 47-48% dá evaporativo.","Seco demais no verão. Condensa no inverno sem ventilar.","Água/pátio/vegetação no verão. Ventilar seca no inverno.","Sem renovação há bolores no inverno.","Ventilação permanente + verde para equilibrar."],
["","Precipitação","838 mm out-jan (105-125 mm) enchem cisterna e solo.","Seca jun-ago (5-18 mm). Torrencial com erosão.","Cobertura para rega e autoclismo. Solo permeável.","Cheias rápidas em solo nu.","Cisterna + permeável + gota-a-gota."],
["","Nebulosidade","Verão limpo dá sol e fotovoltaico. Nuvem de inverno guarda humidade.","Menos sol de inverno para captar.","Vãos S/E e claraboias controladas para luz natural.","Mais luz artificial no fundo do inverno.","Abrir a S/E sem sobreaquecer. Proteger a O."],
["","Regime de ventos","Brisa atlântica + fresco noturno descarregam a massa.","Cabeço exposto. Sem velocidade verificada.","Cruzada excelente na meia-estação.","Vãos grandes a N arrefecem demais no inverno.","Cruzada S-N com controlo. Cortina a barlavento."],
["","Psicrométrico (Givoni)","Ventilação + massa + evaporativo quase todo o ano. Mai/out dentro.","Mais meses fora que dentro (frio húmido / calor seco).","Passivo: sol+massa no inverno, noite+sombra+água no verão.","Humidade dentro sem renovação.","Pouco ativo, só reforço. Aproveitar o natural."],
]
render(os.path.join(BASE,"portalegre-macroestrutura.png"), "Portalegre — Macroestrutura (9 tópicos)", "Fortes, Fracos, Oportunidades, Ameaças e Estratégias — só Portalegre", H, macro, CW, merges=[(0,5,"MACROESTRUTURA — Natural"),(5,9,"MACROESTRUTURA — Construída")])
render(os.path.join(BASE,"portalegre-perceptiva.png"), "Portalegre — Estrutura Percetiva (4 tópicos)", "Microclima, vistas e paleta — só Portalegre", H, perc, CW, merges=[(0,4,"ESTRUTURA PERCETIVA")])
render(os.path.join(BASE,"portalegre-clima.png"), "Portalegre — Clima / Bioclimática (8 tópicos)", "IPMA 1991-2020: 15,9°C / 838 mm — só Portalegre", H, clima, CW, merges=[(0,8,"CLIMA Bioclimática")])
