import math, os, urllib.request
from PIL import Image, ImageDraw, ImageFont
BASE = r"C:\Users\diogo\OneDrive\Documentos\Projeto Padrão"
Z = 16
pts = [
 (1,"Cais dos Vapores",38.703022,-8.9768734),
 (2,"Moinho do Cais",38.703562,-8.979547),
 (3,"Bela Vista / Mundet",38.7008029,-8.96927),
 (4,"SAPAC / ex-ramal*",38.701,-8.9665),
 (5,"Rua Jose Mundet",38.7013905,-8.9638016),
 (6,"Forno de cal*",38.6995,-8.968),
 (7,"Lancada 1368",38.6887492,-8.9513752),
]
def F(sz,b=False):
    try: return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf",sz)
    except Exception: return ImageFont.load_default()
def ll2t(lat,lon,z):
    n=2**z
    x=(lon+180)/360*n
    r=math.radians(lat)
    y=(1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*n
    return x,y
# bounds with margin
lats=[p[2] for p in pts]; lons=[p[3] for p in pts]
lat0,lat1=min(lats)-0.004,max(lats)+0.004
lon0,lon1=min(lons)-0.008,max(lons)+0.008
x0f,y0f=ll2t(lat1,lon0,Z)
x1f,y1f=ll2t(lat0,lon1,Z)
import math as m
x0,x1=m.floor(x0f),m.ceil(x1f); y0,y1=m.floor(y0f),m.ceil(y1f)
print("tiles",x0,x1,y0,y1)
tiles={}
for x in range(x0,x1+1):
    for y in range(y0,y1+1):
        url=f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{y}/{x}"
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=30) as r:
                from io import BytesIO
                im=Image.open(BytesIO(r.read())).convert("RGB")
                tiles[(x,y)]=im
                print("ok",x,y)
        except Exception as e:
            print("fail",x,y,e)
W=(x1-x0+1)*256; H=(y1-y0+1)*256
base=Image.new("RGB",(W,H))
for (x,y),im in tiles.items():
    base.paste(im,((x-x0)*256,(y-y0)*256))
def ll2p(lat,lon):
    xf,yf=ll2t(lat,lon,Z)
    return (xf-x0)*256,(yf-y0)*256
d=ImageDraw.Draw(base)
for (i,n,la,lo) in pts:
    px,py=ll2p(la,lo)
    r=26
    d.ellipse([px-r,py-r,px+r,py+r],fill=(31,77,91),outline="yellow",width=4)
    t=str(i)
    tw=d.textlength(t,font=F(30,True))
    d.text((px-tw/2,py-22),t,fill="white",font=F(30,True))
    d.text((px+32,py-14),f"{i} {n}",fill="white",font=F(24,True),stroke_width=3,stroke_fill="black")
# title bar
bar=Image.new("RGB",(W,90),(31,77,91))
db=ImageDraw.Draw(bar)
db.text((20,12),"Montijo — frente ribeirinha sobre satelite (Esri World Imagery) — 7 edificios",fill="white",font=F(30,True))
db.text((20,52),"1 Cais · 2 Moinho do Cais · 3 Bela Vista · 4 SAPAC* · 5 J. Mundet · 6 Forno* · 7 Lancada  (*aprox. verificar)",fill=(220,230,235),font=F(22,False))
out=Image.new("RGB",(W,H+90+60))
out.paste(bar,(0,0)); out.paste(base,(0,90))
df=ImageDraw.Draw(out)
df.text((20,H+98),"Satelite: Esri World Imagery | Geocodificacao Nominatim OSM 07/10/2026 | * fixar com GPS",fill=(90,90,90),font=F(20,False))
p=os.path.join(BASE,"montijo-satelite-edificios.png")
out.save(p)
print("saved",p,out.size)
