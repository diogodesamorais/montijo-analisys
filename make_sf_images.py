# -*- coding: utf-8 -*-
"""
make_sf_images.py — descarrega as imagens do site "As pedras da Sagrada Familia"
da Wikimedia Commons, guarda a atribuicao/licenca de cada uma e escreve um
manifesto JSON consumido pelo HTML.

Tipos de imagem:
  exata        -> fotografia do proprio local/material de origem
  representativa -> fotografia do TIPO de rocha (legenda indica-o)

Uso:  python make_sf_images.py
"""
import json, os, re, sys, time, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(BASE, "sagrada-familia-geologia", "img")
MANIFEST = os.path.join(BASE, "sagrada-familia-geologia", "img-manifest.json")

API = "https://commons.wikimedia.org/w/api.php"
UA = "SagradaFamiliaGeologia/1.0 (educational coursework for architecture; python-urllib)"
WIDTH = 1024

SLOTS = [
    # ---------------- Enquadramento ----------------
    dict(id="ctx-mapa-variscano", kind="exata", group="Contexto",
         cap="Distribuicao dos orogenos variscanos na Europa. Os granitos catalanies crystallizaram neste evento.",
         titles=["Distribution of varisican orogenies.png"]),
    dict(id="ctx-orogenia", kind="representativa", group="Contexto",
         cap="Reconstrucao da Europa ha ~237 Ma, no fecho da orogenese varisca (Carboniferico-Permico).",
         titles=["237 Ma orogenies reconstruction.jpg", "237 Ma plate tectonic reconstruction.jpg"]),
    dict(id="ctx-collserola", kind="exata", group="Contexto",
         cap="Collserola: o substrato paleozoico e granitico que forneceu os granitos do templo.",
         titles=["Carretera de les Aigües P1230333.JPG", "Serra de Vilana P1230317.JPG"]),
    dict(id="ctx-montjuic-pedreira", kind="exata", group="Contexto",
         cap="Pedreira romana de Montjuïc. As paredes em arco sao vestigios do corte: a mesma rocha alimentou Roma, o Gotico, o Eixample e o templo.",
         titles=["Pedrera romana de Montjuïc 1.jpg", "Pedrera romana de Montjuïc 2.JPG"]),
    dict(id="ctx-montjuic-vista", kind="exata", group="Contexto",
         cap="Montjuïc. A montanha e um bloco tectonico inclinado de arenitos e conglomerados miocenicos.",
         titles=["Spain.Catalonia.Barcelona.Vista.Panoramica.Montjuic.jpg"]),

    # ---------------- O templo ----------------
    dict(id="tmpl-nascimento", kind="exata", group="Templo",
         cap="Faca do Nascimento, construida inteiramente em pedra de Montjuïc.",
         titles=["Barcelona - La Sagrada Família - Nativity Façade IV.jpg",
                 "Sagrada Familia, Nativity facade (2) (30477190154).jpg"]),
    dict(id="tmpl-nascimento-cc0", kind="exata", group="Templo",
         cap="Faca do Nascimento vista do chao. Imagem CC0 (dominio publico).",
         titles=["Sagrada Família Nativity Façade from Ground, Barcelona, 2023.jpg"]),
    dict(id="tmpl-coluna-evangelista", kind="exata", group="Templo",
         cap="Coluna dos Evangelistas. As quatro maiores (Ø 2,10 m) sao de porfiro vermelho de Yazd.",
         titles=["One of the evangelists' columns - Interior of Sagrada Família - Barcelona.jpg",
                 "Sagrada familia interior columna 00001.jpg"]),
    dict(id="tmpl-colunas", kind="exata", group="Templo",
         cap="Nave central: colunas ramificadas e inclinadas, como arvores.",
         titles=["Sagrada Familia columns.jpg"]),
    dict(id="tmpl-interior", kind="exata", group="Templo",
         cap="Interior do templo. A luz entra filtrada pelas vidracoes.",
         titles=["Barcelona Sagrada Familia interior 01.jpg", "Sagrada Familia interior 1.jpg"]),
    dict(id="tmpl-nau", kind="exata", group="Templo",
         cap="A nave vista do transsepte.",
         titles=["Sagrada Família. Interior nau.jpg"]),
    dict(id="tmpl-paixao", kind="exata", group="Templo",
         cap="Detalhe da Porta da Caridade, na Faca do Nascimento.",
         titles=["Detalle da Fachada da Caridade. Sagrada Familia. Barcelona B41.jpg",
                 "Detalle da Sagrada Familia. Barcelona B22.jpg"]),

    # ---------------- Pedra de Montjuïc ----------------
    dict(id="montjuic-lamina", kind="representativa", group="Pedra",
         cap="Arenito em lamina fina (luz polarizada). Cimento silicoso microcristalino a unir os graos de quartzo — e esta silicificacao que torna a pedra compacta.",
         titles=["200708-1 qtzarem silicacemt 50x PPL.jpg",
                 "180507-2 qtzaren silicacem dustrim 50x XPL.jpg",
                 "210509-2 qtz feld lith aren 50x XPL.jpg"]),
    dict(id="montjuic-macro", kind="representativa", group="Pedra",
         cap="Arenito em superficie natural: textura silicosa compacta, cinzenta a rosada.",
         titles=["2010 08 04 Prebischtor Felsentor DSCI0644.JPG",
                 "Sandstone homoaxial cement.jpg",
                 "150627053448 Snow Canyon.jpg"]),
    dict(id="montjuic-pedreira", kind="exata", group="Pedra",
         cap="Pedreira romana de Montjuïc — a mesma materia-prima do templo.",
         titles=["Pedrera romana de Montjuïc 1.jpg", "Pedrera romana de Montjuïc 2.JPG"]),
    dict(id="montjuic-aplicacao", kind="exata", group="Pedra",
         cap="A aplicacao mais visivel do arenito de Montjuïc: as torres e as fachadas.",
         titles=["Sagrada Familia March 2015-14a.jpg"]),

    # ---------------- Granitos ----------------
    dict(id="orrius-lamina", kind="representativa", group="Pedra",
         cap="Granodiorita-tonalita em lamina fina. Feldspato zonado, biotita e hornblenda — o 'ull de serp'.",
         titles=["Granodiorite (55185004332).jpg", "Granodiorit (RK 2206 P1890188).jpg",
                 "Flickr - brewbooks - Granite and Granodiorite roadcut, above Ross Lake.jpg"]),
    dict(id="orrius-macro", kind="representativa", group="Pedra",
         cap="Granito biotitico de dois muscovitas, com cristais visiveis a olho nu (2–5 mm).",
         titles=["380 Granite porphiroïde gris Plounévez-Quintin.JPG",
                 "Granodiorite (Barre Pluton, Devonian, ~380 Ma; Rock of Ages Quarry, Graniteville, Vermont, USA) 4.jpg"]),
    dict(id="orrius-serra", kind="exata", group="Pedra",
         cap="Serra Litoral Catalana, onde se abrem as pedreiras de granito do Vallès Oriental.",
         titles=["Serra de Vilana P1230317.JPG", "Carretera de les Aigües P1230333.JPG"]),

    dict(id="tarn-granito", kind="exata", group="Pedra",
         cap="Blocos de granito do Sidobre (Tarn, Franca). Quartzoso ate 55% — a rocha mais resistente dos granitos do templo.",
         titles=["Le Roc de l'Oie.jpg", "Sidobre Roc Oie.jpg",
                 "Rocher dans le Sidobre, Tarn (5471165102).jpg"]),
    dict(id="tarn-alteracao", kind="exata", group="Pedra",
         cap="Alteracao esferoidal no granito do Sidobre: 'o chapeu de Napoleao', bloco com descamamento concentrico.",
         titles=["Le chapeau de Napoléon - Sidobre.JPG",
                 "Peyro Clabado.jpg",
                 "Roca de l'oca a Sidobre.jpg",
                 "Bloc granitique, le chapeau, Sidobre, 14 mai 1882 (8634780084).jpg"]),
    dict(id="tarn-panorama", kind="exata", group="Pedra",
         cap="Sidobre, Roc de l'Oie — o bloco granitico que 'anda' sobre a superficie.",
         titles=["Les trois fromages - Sidobre.JPG", "81128-Lacrouzette-ZNIEFF1.jpg"]),

    dict(id="fraguas-granito", kind="representativa", group="Pedra",
         cap="Granito biotitico escuro da Galiza, com pintas claras de micas.",
         titles=["2017 San Vicente do Mar. O Grove. Galiza-3.jpg"]),
    dict(id="granito-branco", kind="representativa", group="Pedra",
         cap="Granito claro, leuocratico, do tipo do 'granito branco cristal' do Sistema Central.",
         titles=["Granodiorite (55186050453).jpg", "Granodiorite (55185896171).jpg"]),

    # ---------------- Pórfiro de Yazd ----------------
    dict(id="yazd-porfiro", kind="representativa", group="Pedra",
         cap="Porfiro vermelho: fenocristais de >2 mm numa matriz mais fina. O do templo e uma ignimbrita riolitica.",
         titles=["Bagolino - Sito Romanterra - Porfido.jpg",
                 "Rochlitzer Porphyr im Steinbruch auf der Pappelhöhe bei Rochlitz, Sachsen 2BG1A6601WI.jpg"]),
    dict(id="yazd-porfiro-2", kind="representativa", group="Pedra",
         cap="Porfiro vermelho em afloramento, com cimento silicoso a contrastar com a massa rosada.",
         titles=["Porphyrlehrpfad - Eiche deren Wurzeln um das rote Porphyrgestein gewachsen sind - Geopark Porphyrland - Sachsen.jpg",
                 "Porphyrfelsen am Porphyrlehrpfad - Rochlitzer Berg - Geotop - Sachsen.jpg"]),
    dict(id="yazd-ignimbrita", kind="representativa", group="Pedra",
         cap="Fiammes numa ignimbrita: as 'chamas' achatadas pelo fluxo piroclastico — a assinatura da textura eutaxitica.",
         titles=["Fiamme in Ignimbrite at Side Pike in Cumbria.jpg",
                 "10-PK 13 Sèrie ignimbrítica-4.JPG"]),

    # ---------------- Basalto de Bagnoregio ----------------
    dict(id="bagnoregio-basanita", kind="representativa", group="Pedra",
         cap="Basanita em superficie de quebra. Rochas vulcanicas efusivas basicas, com feldespatoides.",
         titles=["Basanite in Geopark on Albertov.JPG", "Qapf basanite.jpg",
                 "Poustevník 03 (bazanit-tefrit).jpg"]),
    dict(id="bagnoregio-leucita", kind="representativa", group="Pedra",
         cap="Leucita em lamina fina (nicols cruzados): o mineral que identifica a basanita com leucita de Bagnoregio.",
         titles=["Leucit XPL.jpg", "Leucit LPL.jpg",
                 "Leucite - Roccamonfina, Lazio, Italia 01.jpg"]),
    dict(id="bagnoregio-bolsena", kind="exata", group="Pedra",
         cap="O lago de Bolsena, junto a Montefiascone: o vulcanismo cuaternario que forneceu o basalto das 8 colunas decagonais.",
         titles=["Lago di Bolsena.jpg"]),

    # ---------------- Basalto da Garrotxa ----------------
    dict(id="castellfollit-colunas", kind="exata", group="Pedra",
         cap="As duas coladas basalticas de Castellfollit de la Roca (~217 ka e ~192 ka) e a sua disjuncao columnar.",
         titles=["Castellfollit Castle and Geologic Formation.jpg", "Castellfollit roca.JPG"]),
    dict(id="castellfollit-rochedo", kind="exata", group="Pedra",
         cap="Rochedo de basalto de Castellfollit de la Roca, com as colunas prismaticas visiveis.",
         titles=["Roques de Castellfollit de la Roca.jpeg",
                 "Roques de Castellfollit de la Roca (Restored).jpg"]),
    dict(id="castellfollit-cidade", kind="exata", group="Pedra",
         cap="O pueblo assenta sobre o rochedo de basalto; a torre da igreja marca o topo.",
         titles=["Castellfollit de la Roca La Garrotxa.jpg",
                 "Castellfollit de la Roca 01.jpg"]),
    dict(id="garrotxa-fageda", kind="exata", group="Pedra",
         cap="La Fageda d'en Jordà: a 'fogueira' de basalto com colunas hexagonais, no coracao da Garrotxa.",
         titles=["Tossol Fageda.jpg", "Vora Tosca Cat 20071230 003.jpg"]),

    # ---------------- Pedra de Calafell ----------------
    dict(id="calafell-biomicrita", kind="representativa", group="Pedra",
         cap="Calcario bioclastico: grao e matriz com fragments de conchas e foraminiferos.",
         titles=["Affleurement miocène, Vernet-les-Bains.jpg",
                 "Caliza de crinoides.2 - Fosil.JPG",
                 "Pietra di Rapolano CONTROFALDA.jpg"]),
    dict(id="calafell-local", kind="exata", group="Pedra",
         cap="Calafell, no Baix Penedès, de onde vem a pedra usada nos interiores do templo.",
         titles=["Estació de Segur de Calafell.JPG"]),

    # ---------------- Pedra de la Floresta ----------------
    dict(id="floresta-calcarenito", kind="representativa", group="Pedra",
         cap="Calc-arenito fossilifero: grao fino, rico em carbonatos, facil de esculpir — a pedra dos anjos e das figuras da Paixao.",
         titles=["Calcarenita fosilífera.jpg",
                 "Calcarenite MiddleBeach LordHoweIsland 5June2011.jpg",
                 "Pietra di Rapolano INFALDA.jpg"]),
    dict(id="floresta-local", kind="representativa", group="Pedra",
         cap="Les Garrigues: comarca de la pedra de Floresta, entre el Segre i el Llobregat.",
         titles=["Tàrrega.jpg", "Segarra.jpg", "Garrigues.jpg", "Canal de Segarra.jpg",
                 "Les Garrigues.jpg"],
         allow_search=True, query="Tàrrega Garrigues", kw=("garrigues", "tàrrega", "tarrega", "segarra")),

    # ---------------- Mármore de Macael ----------------
    dict(id="macael-marmore", kind="exata", group="Pedra",
         cap="Marmore de Macael nas cores branco, amarelo e cinzento. A rocha e >99% calcite, com foliacao metamorfica.",
         titles=["Focuspiedrapremiosmacael.jpg",
                 "Macael verano del dos mil dieciseis 01.jpg",
                 "Monumento a la entrada de Macael. Realizado con blanco, amarillo y gris Macael..JPG"]),
    dict(id="macael-marmore-branco", kind="exata", group="Pedra",
         cap="O marmore branco de Macael, tal como se apresenta nas pedreiras.",
         titles=["Macael1.jpg"]),
    dict(id="macael-local", kind="exata", group="Pedra",
         cap="Macael, na vertente norte da Sierra de los Filabres (Almeria).",
         titles=["Macael, en Almería (España).jpg", "Macael verano del dos mil dieciseis 02.jpg"]),
    dict(id="macael-monumento", kind="exata", group="Pedra",
         cap="Monumento em marmore de Macael, com o veio cinzento do bandamento metamorfico visivel.",
         titles=["Monumento a la Virgen del Rosario, Patrona y Alcaldesa Perpétua y Honorífica de Macael.jpg"]),

    # ---------------- Travertino ----------------
    dict(id="travertino-rocha", kind="representativa", group="Pedra",
         cap="Travertino: carbonato continental com laminacao e porosidade, formado por aguas minerais.",
         titles=["Affioramento di travertino 01.jpg", "Travertine 01.jpg",
                 "150 Molsa regalimant, travertí en formació als cingles vora Sant Miquel del Fai.JPG"]),
    dict(id="travertino-detalhe", kind="representativa", group="Pedra",
         cap="Detalhe do travertino junto a cascata — a estrutura laminada e os poros dao-lhe o aspecto caracteristico.",
         titles=["251 Detall del travertí vora el salt d'aigua del Tenes, Sant Miquel del Fai.JPG",
                 "098 Sant Miquel del Fai, formació del travertí a la cinglera.JPG"]),
    dict(id="travertino-tivoli", kind="exata", group="Pedra",
         cap="Bagni di Tivoli, as termas romanas cuja pedra foi usada na Faca da Paixao.",
         titles=["Tivoli terme.jpg", "Bagni di Tivoli terme.jpg", "Villa d'Este Tivoli.jpg",
                 "Tivoli 01.jpg"]),

    # ---------------- Pedra de Figueres ----------------
    dict(id="figueres-calcario", kind="representativa", group="Pedra",
         cap="Calcario bioclastico recristalizado, do tipo do 'marmore de Figueres' (Alt Emporda).",
         titles=["Caliza de crinoides.2 - Fosil.JPG",
                 "Calcarenita fosilífera.jpg",
                 "Pietra di Rapolano CONTROFALDA.jpg"]),
]


def api(params, tries=5):
    params = dict(params, action="query", format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    delay = 4.0
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and t < tries - 1:
                print(f"    [429] {delay:.0f}s", flush=True)
                time.sleep(delay); delay *= 1.7
                continue
            raise
    return {}


def strip_html(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def resolve(titles):
    out = {}
    for i in range(0, len(titles), 20):
        chunk = ["File:" + t if not t.startswith(("File:", "Category:")) else t
                 for t in titles[i:i + 20]]
        try:
            d = api({"titles": "|".join(chunk), "prop": "imageinfo",
                     "iiprop": "url|size|extmetadata", "iiurlwidth": str(WIDTH)})
        except Exception as e:
            print("    ERRO chunk:", e)
            continue
        for p in d.get("query", {}).get("pages", []):
            if p.get("missing"):
                continue
            ii = (p.get("imageinfo") or [{}])[0]
            if not ii.get("thumburl"):
                continue
            em = ii.get("extmetadata", {})
            thumb = ii["thumburl"].split("?")[0]   # remove tracking params (rate-limit)
            out[p["title"][5:] if p["title"].startswith("File:") else p["title"]] = {
                "thumb": thumb, "page": ii.get("descriptionurl", ""),
                "orig": (ii.get("url") or "").split("?")[0],
                "origbytes": ii.get("size"),
                "lic": strip_html((em.get("LicenseShortName", {}) or {}).get("value", "")),
                "licurl": (em.get("LicenseUrl", {}) or {}).get("value", ""),
                "author": strip_html((em.get("Artist", {}) or {}).get("value", "")),
                "w": ii.get("thumbwidth"), "h": ii.get("thumbheight"),
            }
        time.sleep(1.2)
    return out


def fetch(url, tries=3):
    delay = 4.0
    last = None
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(delay); delay *= 1.7
    raise last


def download(url, path, tries=5):
    """Descarrega a thumbnail; se a API de thumbs bloquear, usa o original
    (upload.wikimedia.org) e redimensiona localmente."""
    delay = 4.0
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            with open(path, "wb") as f:
                f.write(data)
            return len(data)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and t < tries - 1:
                print(f"    [dl {e.code}] {delay:.0f}s", flush=True)
                time.sleep(delay); delay *= 1.6
                continue
            raise
        except Exception:
            if t < tries - 1:
                time.sleep(delay); delay *= 1.6
                continue
            raise
    return 0


def download_original(info, path, maxw=WIDTH):
    """Fallback: descarrega o ficheiro original e redimensiona com PIL."""
    from PIL import Image
    import io
    data = fetch(info["orig"])
    im = Image.open(io.BytesIO(data))
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    if im.width > maxw:
        h = int(im.height * maxw / im.width)
        im = im.resize((maxw, h), Image.LANCZOS)
    if path.lower().endswith(".png"):
        im.save(path, "PNG", optimize=True)
    else:
        im.save(path, "JPEG", quality=86, optimize=True, progressive=True)
    return os.path.getsize(path)


def search_images(query, kw, limit=25):
    """Pesquisa ficheiros de imagem cujo nome contenha uma das palavras-chave."""
    d = api({"generator": "search", "gsrsearch": query, "gsrnamespace": "6",
             "gsrlimit": str(limit), "prop": "imageinfo",
             "iiprop": "url|size|extmetadata", "iiurlwidth": str(WIDTH)})
    out = []
    for p in d.get("query", {}).get("pages", []):
        t = p.get("title", "")
        if not t.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        if not any(k in t.lower() for k in kw):
            continue
        if not (p.get("imageinfo") or [{}])[0].get("thumburl"):
            continue
        out.append(t[5:])
    time.sleep(1.2)
    return out


MIN_W, MIN_H = 420, 240     # resolucao minima aceitavel para o site


def image_ok(path):
    """Aceita imagens normais ou panoramicas (relacao de aspecto >= 3)."""
    try:
        from PIL import Image
        im = Image.open(path)
        im.load()
        w, h = im.size
        ok = w >= MIN_W and (h >= MIN_H or w >= 3 * h)
        return ok, (w, h)
    except Exception:
        return False, (0, 0)


def main():
    os.makedirs(DEST, exist_ok=True)
    all_titles = sorted({t for s in SLOTS for t in s["titles"]})
    print(f"Resolver {len(all_titles)} titulos...")
    info = resolve(all_titles)
    print(f"  {len(info)} resolvidos\n")

    manifest = []
    for s in SLOTS:
        # --- candidatos ja existentes em disco (reutilizar) ---
        chosen = None
        for t in s["titles"]:
            if t not in info:
                continue
            ext = ".png" if t.lower().endswith(".png") else ".jpg"
            path = os.path.join(DEST, s["id"] + ext)
            if os.path.exists(path):
                good, _ = image_ok(path)
                if good:
                    chosen = t
                    break

        # --- descarregar ate encontrar resolucao aceitavel ---
        if not chosen:
            for t in s["titles"]:
                if t not in info:
                    continue
                ext = ".png" if t.lower().endswith(".png") else ".jpg"
                path = os.path.join(DEST, s["id"] + ext)
                try:
                    download(info[t]["thumb"], path)
                except Exception:
                    try:
                        download_original(info[t], path)
                    except Exception as e:
                        print(f"  !! falhou {s['id']} <- {t}: {e}")
                        continue
                good, size = image_ok(path)
                if good:
                    chosen = t
                    print(f"  OK {s['id']:<26} {t[5:56]:<58} {size[0]}x{size[1]}")
                    break
                print(f"  ~ {s['id']:<26} {t[5:40]:<42} pequena {size[0]}x{size[1]} -> proximo")
                try:
                    os.remove(path)
                except OSError:
                    pass
                time.sleep(0.5)

        if not chosen:
            # ultima tentativa: pesquisa com filtro
            if s.get("allow_search"):
                print(f"  pesquisa: {s['id']}")
                try:
                    for t in search_images(s["query"], s.get("kw", ())):
                        if t not in info:
                            info.update(resolve([t]))
                        if t in info:
                            chosen = t
                            break
                except Exception as e:
                    print("    ERRO search:", e)
            if not chosen:
                print(f"  !! sem imagem: {s['id']}")
                continue

        i = info[chosen]
        ext = ".png" if chosen.lower().endswith(".png") else ".jpg"
        fn = s["id"] + ext
        path = os.path.join(DEST, fn)
        if not os.path.exists(path):
            try:
                download(i["thumb"], path)
            except Exception:
                try:
                    download_original(i, path)
                except Exception as e:
                    print(f"  !! download falhou {s['id']}: {e}")
                    continue
        n = os.path.getsize(path)

        manifest.append({
            "id": s["id"], "file": "img/" + fn, "group": s["group"], "kind": s["kind"],
            "caption": s["cap"], "title": chosen[5:], "author": i["author"],
            "license": i["lic"], "license_url": i["licurl"], "page": i["page"],
            "w": i["w"], "h": i["h"], "bytes": n,
        })
        time.sleep(0.8)

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\n{len(manifest)}/{len(SLOTS)} imagens -> {DEST}")
    print(f"manifesto -> {MANIFEST}")


if __name__ == "__main__":
    main()
