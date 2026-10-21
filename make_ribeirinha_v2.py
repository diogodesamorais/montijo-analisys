import math, os, urllib.request
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\diogo\OneDrive\Documentos\Projeto Padrão"
Z = 16

ABANDONADOS = [
 (1, "Cais dos Vapores", 38.703022, -8.9768734),
 (2, "Mundet Bela Vista 1923", 38.7008029, -8.96927),
 (3, "Chamine/Caldeiras* Mundet", 38.7005, -8.9698),
 (4, "SAPAC/ex-ramal*", 38.701, -8.9665),
 (5, "Rua Jose Mundet ruina", 38.7013905, -8.9638016),
 (6, "Forno de cal*", 38.6995, -8.968),
 (7, "Antiga Estacao/ramal*", 38.7023, -8.9718),
 (8, "Leste + Lancada 1368", 38.6887492, -8.9513752),
]

MUDANCA = [
 ("M1", "Moinho do Cais>museu", 38.703562, -8.979547),
 ("M2", "Casa Mora>museu", 38.7066666, -8.9761698),
 ("M3", "Mercado reabilitado", 38.7062083, -8.9762356),
 ("M4", "Cinema-Teatro J.Almeida", 38.7058789, -8.9703657),
 ("M5", "Cais Vapores> lazer*", 38.703022, -8.9768734),
 ("M6", "Armazens M.Pais reab.", 38.7038091, -8.9756346),
 ("M7", "Ramal>Ecopista*", 38.7023, -8.9718),
 ("M8", "Caldeiras>exposicao*", 38.7005, -8.9698),
]

def F(sz, b=False):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", sz)
    except Exception:
        return ImageFont.load_default()

def ll2t(lat, lon, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    r = math.radians(lat)
    y = (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * n
    return x, y

def build(pts, title, subtitle, outname, color=(31, 77, 91)):
    lats = [p[2] for p in pts]; lons = [p[3] for p in pts]
    lat0, lat1 = min(lats) - 0.004, max(lats) + 0.004
    lon0, lon1 = min(lons) - 0.008, max(lons) + 0.008
    x0f, y0f = ll2t(lat1, lon0, Z)
    x1f, y1f = ll2t(lat0, lon1, Z)
    x0, x1 = math.floor(x0f), math.ceil(x1f)
    y0, y1 = math.floor(y0f), math.ceil(y1f)
    print(outname, "tiles", x0, x1, y0, y1)
    tiles = {}
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{y}/{x}"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    im = Image.open(BytesIO(r.read())).convert("RGB")
                    tiles[(x, y)] = im
                    print(" ok", x, y)
            except Exception as e:
                print(" fail", x, y, e)
    W = (x1 - x0 + 1) * 256; H = (y1 - y0 + 1) * 256
    base = Image.new("RGB", (W, H))
    for (x, y), im in tiles.items():
        base.paste(im, ((x - x0) * 256, (y - y0) * 256))

    def ll2p(lat, lon):
        xf, yf = ll2t(lat, lon, Z)
        return (xf - x0) * 256, (yf - y0) * 256

    d = ImageDraw.Draw(base)
    for (lab, nome, la, lo) in pts:
        px, py = ll2p(la, lo)
        r = 26
        d.ellipse([px - r, py - r, px + r, py + r], fill=color, outline="yellow", width=4)
        t = str(lab)
        tw = d.textlength(t, font=F(26, True))
        d.text((px - tw / 2, py - 20), t, fill="white", font=F(26, True))
        d.text((px + 32, py - 14), f"{lab} {nome}", fill="white", font=F(22, True), stroke_width=3, stroke_fill="black")
    bar = Image.new("RGB", (W, 90), color)
    db = ImageDraw.Draw(bar)
    db.text((20, 12), title, fill="white", font=F(28, True))
    db.text((20, 52), subtitle, fill=(220, 230, 235), font=F(20, False))
    out = Image.new("RGB", (W, H + 90 + 60))
    out.paste(bar, (0, 0)); out.paste(base, (0, 90))
    df = ImageDraw.Draw(out)
    df.text((20, H + 98), "Satelite: Esri World Imagery | Geocodificacao Nominatim OSM 07/10/2026 | * fixar com GPS no local", fill=(90, 90, 90), font=F(19, False))
    p = os.path.join(BASE, outname)
    out.save(p)
    print("saved", p, out.size)

build(ABANDONADOS, "Montijo ribeirinha — 8 abandonados sobre satelite (Esri)", "1 Cais · 2 Bela Vista · 3 Chamine* · 4 SAPAC* · 5 J.Mundet · 6 Forno* · 7 Estacao* · 8 Lancada (*aprox.)", "montijo-satelite-abandonados-v2.png", (31, 77, 91))
build(MUDANCA, "Montijo ribeirinha — 8 mudancas de funcao sobre satelite (Esri)", "M1 Moinho>museu · M2 Casa Mora>museu · M3 Mercado · M4 Cinema · M5 Cais · M6 Armazens · M7 Ecopista* · M8 Caldeiras*", "montijo-satelite-mudanca-funcao.png", (88, 52, 28))
