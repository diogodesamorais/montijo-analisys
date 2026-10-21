# -*- coding: utf-8 -*-
"""Verificacao do site gerado: referencias a imagens, estrutura HTML, SVG."""
import json, os, re, sys
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sagrada-familia-geologia")
HTML = os.path.join(SITE, "index.html")
src = open(HTML, encoding="utf-8").read()

ok = True


def chk(cond, msg):
    global ok
    print(("  OK   " if cond else "  FALHA ") + msg)
    if not cond:
        ok = False


print("=== 1. Referencias a imagens ===")
imgs = sorted(set(re.findall(r'src="(img/[^"]+)"', src)))
missing = [i for i in imgs if not os.path.exists(os.path.join(SITE, i))]
chk(not missing, f"{len(imgs)} imagens referenciadas, {len(missing)} em falta")
for m in missing:
    print("        falta:", m)
used = {i.split("/")[-1] for i in imgs}
ondisk = {f for f in os.listdir(os.path.join(SITE, "img"))}
chk(used == ondisk, f"todas as {len(ondisk)} imagens em disco sao usadas (nao usadas: {sorted(ondisk - used)})")

print("\n=== 2. Estrutura HTML ===")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.tags = {}
        self.ids = set()
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        self.tags[tag] = self.tags.get(tag, 0) + 1
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        if tag == "a" and d.get("href", "").startswith("#"):
            self.anchors.add(d["href"][1:])
        if tag not in ("img", "br", "hr", "meta", "link", "input", "path", "circle", "line",
                       "rect", "stop", "text", "use", "polygon"):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in ("img", "br", "hr", "meta", "link", "input"):
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass


p = P()
p.feed(src)
chk(not p.stack, f"etiquetas HTML balanceadas (por fechar: {p.stack[:5]})")
print(f"        <section>={p.tags.get('section')} <figure>={p.tags.get('figure')} "
      f"<img>={p.tags.get('img')} <table>={p.tags.get('table')} <svg>={p.tags.get('svg')}")

print("\n=== 3. Navegacao interna ===")
missing_a = [a for a in p.anchors if a and a not in p.ids]
chk(not missing_a, f"{len(p.anchors)} links internos, {len(missing_a)} sem destino")
for a in missing_a:
    print("        sem destino:", a)

print("\n=== 4. Conteudo ===")
for name, pat in [
    ("13 cartoes de pedra", r'class="stone"'),
    ("13 ids de pedra", r'id="pedra-'),
    ("filtros de familia", r'class="fbtn'),
    ("lightbox", r'id="lb"'),
    ("grafico de resistencia", r'aria-label="Resistencia'),
    ("linha do tempo", r'aria-label="Linha do tempo'),
    ("tabela comparativa", r'<tbody>'),
    ("bibliografia", r'class="biblio"'),
    ("creditos", r'class="credits"'),
    ("notas metodologicas", r'Sobre este trabalho'),
]:
    n = len(re.findall(pat, src))
    chk(n > 0, f"{name} ({n})")

print("\n=== 5. SVG da linha do tempo ===")
svgs = re.findall(r'<svg.*?</svg>', src, re.S)
chk(len(svgs) >= 2, f"{len(svgs)} SVG gerados")
tl = [s for s in svgs if "Linha do tempo" in s]
if tl:
    s = tl[0]
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
    W, H = int(vb.group(1)), int(vb.group(2))
    xs = [float(x) for x in re.findall(r'<line x1="([\d.]+)"', s)]
    ys = [float(y) for y in re.findall(r'y2="([\d.]+)"', s)]
    chk(max(xs) <= W and min(xs) >= 0, f"coordenadas X dentro da viewBox ({min(xs):.0f}..{max(xs):.0f} de {W})")
    chk(max(ys) <= H, f"coordenadas Y dentro da viewBox (max {max(ys):.0f} de {H})")
    chk(len(re.findall(r'<text', s)) > 20, f"{len(re.findall(r'<text', s))} rotulos")

print("\n=== 6. Atribuicoes ===")
mani = json.load(open(os.path.join(SITE, "img-manifest.json"), encoding="utf-8"))
noauth = [m["id"] for m in mani if not m.get("author")]
nolice = [m["id"] for m in mani if not m.get("license")]
chk(not nolice, f"todas as {len(mani)} imagens tem licenca")
print(f"        sem autor declarado: {noauth}")
kinds = {}
for m in mani:
    kinds[m["kind"]] = kinds.get(m["kind"], 0) + 1
print(f"        exacta={kinds.get('exata',0)}  representativa={kinds.get('representativa',0)}")

print("\n=== 7. Licencas CC BY-SA (exigem indicar a obra) ===")
bysa = [m for m in mani if "BY-SA" in m["license"]]
chk(any("Atribuição" in src or "Atribui" in src for _ in [1]),
    f"{len(bysa)} imagens CC BY-SA — atribuicao presente no rodape")

print("\n" + ("TUDO OK" if ok else "*** H FALHAS ***"))
sys.exit(0 if ok else 1)
