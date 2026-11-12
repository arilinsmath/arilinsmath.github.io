import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
LM='/usr/share/texmf/fonts/opentype/public/lm/'
def text_path(fontfile,text,size,x,y,tracking=0):
    f=TTFont(fontfile);gs=f.getGlyphSet();cmap=f.getBestCmap();upm=f['head'].unitsPerEm;hm=f['hmtx']
    s=size/upm;out=[];cx=0
    for ch in text:
        g=cmap[ord(ch)];pen=SVGPathPen(gs);gs[g].draw(pen)
        d=pen.getCommands()
        if d: out.append(f'<path transform="translate({x+cx*s:.2f},{y:.2f}) scale({s:.5f},{-s:.5f})" d="{d}"/>')
        cx+=hm[g][0]+tracking
    return ''.join(out), cx*s
GOLD=(217,164,65); ROSE=(196,86,106); TEAL=(44,133,124); INK='#1c1a27'
def mix(px,py,size):
    # barycentric-ish: top gold, bottom-left teal, bottom-right rose
    h=size*math.sqrt(3)/2
    v=py/h; u=px/size
    wt=1-v; wl=v*(1-u); wr=v*u
    c=[int(GOLD[i]*wt+TEAL[i]*wl+ROSE[i]*wr) for i in range(3)]
    return '#%02x%02x%02x'%tuple(c)
PAL={0:[(240,178,50),(232,150,40),(247,196,90)],1:[(28,160,143),(20,120,140),(60,182,160)],2:[(222,74,110),(178,62,140),(236,110,120)]}
def shade(c,k):
    return '#%02x%02x%02x'%tuple(max(0,min(255,int(v*k))) for v in c)
def sier(x,y,s,n,S,out,path=()):
    h=s*math.sqrt(3)/2
    if n==0:
        g=path[0] if path else 0; sub=path[1] if len(path)>1 else 0
        c=PAL[g][sub]
        k=1.0-0.06*(path[2] if len(path)>2 else 0)
        out.append(f'<path d="M{x:.2f} {y+h:.2f}L{x+s/2:.2f} {y:.2f}L{x+s:.2f} {y+h:.2f}Z" fill="{shade(c,k)}"/>');return
    sier(x+s/4,y,s/2,n-1,S,out,path+(0,));sier(x,y+h/2,s/2,n-1,S,out,path+(1,));sier(x+s/2,y+h/2,s/2,n-1,S,out,path+(2,))
def mark(level,S=100,ox=0,oy=0,gap=0):
    out=[];sier(0,0,S,level,S,out)
    return f'<g transform="translate({ox},{oy})">'+''.join(out)+'</g>'
H=lambda S:S*math.sqrt(3)/2
# 1) mark only (square, for favicon) level 3
def svg_mark(level,size=512,pad=40,bg=None,radius=96):
    S=size-2*pad; h=H(S); oy=(size-h)/2
    bgs=f'<rect width="{size}" height="{size}" rx="{radius}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">{bgs}<g transform="translate({pad},{oy}) scale({S/100})">{mark(level)}</g></svg>'
# 2) monogram mark: sierpinski with AH in central hole (level 4)
def mono(size=512,bg=None,pad=36):
    S=size-2*pad;h=H(S);oy=(size-h)/2+10
    body=f'<g transform="translate({pad},{oy}) scale({S/100})">{mark(4)}</g>'
    bgs=f'<rect width="{size}" height="{size}" rx="96" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{bgs}{body}</svg>'
# 3) horizontal logo: mark + name + tagline
def horiz(dark=False):
    ink='#fbf8f2' if dark else INK; muted='#c9bfa8' if dark else '#6a6377'
    W,Hh=1200,360
    S=260;h=H(S);mx,my=50,(Hh-h)/2
    m=f'<g transform="translate({mx},{my}) scale({S/100})">{mark(4)}</g>'
    p1,w1=text_path(LM+'lmroman10-regular.otf','Arilín Haro',118,360,200)
    p2,w2=text_path('/usr/share/fonts/opentype/inter/Inter-Medium.otf' if False else '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf','MATEMÁTICAS · EDUCACIÓN · DIVULGACIÓN',25,364,262,tracking=180)
    W=int(360+max(w1,w2)+50)
    bg=f'<rect width="{W}" height="{Hh}" fill="{"#1c1a27" if dark else "none"}"/>' if dark else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}">{bg}{m}<g fill="{ink}">{p1}</g><g fill="{muted}">{p2}</g></svg>'
# 4) stacked/square badge for QR center & social
def badge(size=800):
    S=430;h=H(S);mx=(size-S)/2;my=110
    m=f'<g transform="translate({mx},{my}) scale({S/100})">{mark(4)}</g>'
    p1,w1=text_path(LM+'lmroman10-regular.otf','Arilín Haro',96,0,0)
    x1=(size-w1)/2
    p1,_=text_path(LM+'lmroman10-regular.otf','Arilín Haro',96,x1,my+h+110)
    p2,w2=text_path('/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf','MATEMÁTICAS · EDUCACIÓN · DIVULGACIÓN',21,0,0,tracking=180)
    p2,_=text_path('/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf','MATEMÁTICAS · EDUCACIÓN · DIVULGACIÓN',21,(size-w2)/2,my+h+165,tracking=180)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"><rect width="{size}" height="{size}" rx="120" fill="#fbf8f2"/>{m}<g fill="{INK}">{p1}</g><g fill="#6a6377">{p2}</g></svg>'
files={
 'arilin-logo-horizontal.svg':horiz(),
 'arilin-logo-horizontal-fondo-oscuro.svg':horiz(True),
 'arilin-logo-cuadrado.svg':badge(),
 'arilin-icono.svg':svg_mark(4,512,28),
 'arilin-icono-fondo.svg':svg_mark(4,512,70,'#fbf8f2',110),
 'favicon.svg':svg_mark(2,64,2),
 'favicon-fondo.svg':svg_mark(2,64,7,'#1c1a27',14),
}
for k,v in files.items(): open(k,'w').write(v)
print('ok')
