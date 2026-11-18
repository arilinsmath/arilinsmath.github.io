#!/usr/bin/env python3
"""Verifica la consistencia de las notas de los videos (ver notas/CONVENCIONES.md).

  python3 tools/verificar-notas.py [--compilar]

Para cada nota notas/<curso>/<slug>.tex revisa:
  - que existan .tex, .html y .pdf, que el .tex declare \\videoid, \\curso{<curso>} y \\unidad{u}{n};
  - que no tenga ¿ « » escritos directamente en el .tex (salen mal en el PDF);
  - que los enunciados numerados (un solo contador por unidad) coincidan en tipo y número en .tex y .html;
  - que la sección de erratas esté en los dos o en ninguno;
  - que dentro de cada curso y unidad la numeración sea continua (sin huecos ni solapes);
  - que cada entrada de notas/notas.json apunte a una nota existente, a un tema que exista en esa unidad
    y a un número de video válido, y que el video de la nota sea ese video del tema;
  - que la tabla de CONVENCIONES.md esté al día.
Con --compilar, además compila cada .tex con LuaLaTeX en una carpeta temporal (no toca los PDF).
Sale con código 1 si hay errores.
"""
import glob, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from notas_comun import *

errores = []
C = cursos()
notas = {}
for curso, slug in todas_las_notas():
    base = os.path.join(NOTAS, curso, slug)
    nom = "%s/%s" % (curso, slug)
    if curso not in C:
        errores.append("%s: la carpeta %s no corresponde a ningún curso de la página" % (nom, curso))
    for ext in ("html", "pdf"):
        if not os.path.exists(base + "." + ext):
            errores.append("%s: falta %s.%s" % (nom, slug, ext))
    t = sin_comentarios_tex(leer(base + ".tex"))
    for ch, macro in (("«", "\\guillemotleft{}"), ("»", "\\guillemotright{}"), ("¿", "?`")):
        if ch in t:
            errores.append("%s.tex: contiene %s escrito directamente; usar %s" % (nom, ch, macro))
    mv = re.search(r"\\newcommand\{\\videoid\}\{([\w-]+)\}", t)
    if not mv:
        errores.append("%s.tex: no define \\videoid" % nom)
    mc = re.search(r"\\curso\{([\w-]+)\}", t)
    if not mc or mc.group(1) != curso:
        errores.append("%s.tex: debe declarar \\curso{%s}" % (nom, curso))
    d = datos_nota(curso, slug)
    if not d:
        errores.append("%s.tex: no declara \\unidad{u}{n}" % nom)
        continue
    u, n, tipos, _ = d
    esperadas = [(NOMBRES[x], "%d.%d" % (u, n + i)) for i, x in enumerate(tipos)]
    if os.path.exists(base + ".html"):
        hs = re.sub(r"<!--.*?-->", "", leer(base + ".html"), flags=re.S)
        etiquetas = re.findall(r'<div class="(?:def|thm)"><b>(Definición|Proposición|Teorema|Lema|Corolario) (\d+\.\d+)', hs)
        if etiquetas != esperadas:
            errores.append("%s: enunciados del .tex %s no coinciden con los del .html %s" % (nom, esperadas, etiquetas))
        if ("\\begin{erratas}" in t) != ('class="erratas"' in hs):
            errores.append("%s: la sección de erratas está en un formato y no en el otro" % nom)
    notas[(curso, slug)] = (u, n, len(tipos), mv.group(1) if mv else None)

# continuidad por curso y unidad
grupos = {}
for (c, s), (u, n, k, _) in notas.items():
    grupos.setdefault((c, u), []).append((n, k, s))
for (c, u), L in grupos.items():
    sig = 1
    for n, k, s in sorted(L):
        if n != sig and not (k == 0 and n <= sig):
            errores.append("%s, unidad %d: %s empieza en %d.%d pero se esperaba %d.%d (hueco o solape)" % (c, u, s, u, n, u, sig))
        sig = max(sig, n + k)

# registro
for e in registro():
    key = (e["curso"], e["slug"])
    if key not in notas:
        errores.append("notas.json: %s/%s no existe" % key)
        continue
    u, n, k, vid = notas[key]
    if e["unidad"] != u:
        errores.append("notas.json: %s/%s registrada en la unidad %d pero declara la %d" % (key + (e["unidad"], u)))
    if e["curso"] not in C:
        continue
    us = C[e["curso"]]["unidades"]
    temas = [t for t in us[u - 1]["temas"] if t["t"] == e["tema"]] if u <= len(us) else []
    if len(temas) != 1:
        errores.append("notas.json: el tema %r no está (o está repetido) en la unidad %d de %s" % (e["tema"], u, e["curso"]))
        continue
    vids = temas[0]["videos"]
    if not (1 <= e["video"] <= max(1, len(vids))):
        errores.append("notas.json: %s/%s apunta al video %d pero el tema tiene %d" % (key + (e["video"], len(vids))))
    elif vids and vid and vids[e["video"] - 1] != vid:
        errores.append("notas.json: %s/%s tiene \\videoid %s pero el video %d del tema es %s" % (key + (vid, e["video"], vids[e["video"] - 1])))

# tabla de CONVENCIONES.md
antes = leer(CONV)
actualizar_tabla()
despues = leer(CONV)
if antes != despues:
    escribir(CONV, antes)
    errores.append("CONVENCIONES.md: la tabla de numeración no está al día (se actualiza con nueva-nota.py crear o enganchar)")

if "--compilar" in sys.argv:
    for (curso, slug) in notas:
        tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(tmp, curso))
        shutil.copy(os.path.join(NOTAS, "preambulo.tex"), tmp)
        for f in glob.glob(os.path.join(NOTAS, curso, "*.tex")):
            shutil.copy(f, os.path.join(tmp, curso))
        r = subprocess.run(["latexmk", "-lualatex", "-interaction=nonstopmode", "-halt-on-error", slug + ".tex"],
                           cwd=os.path.join(tmp, curso), capture_output=True, text=True)
        if r.returncode != 0:
            errores.append("%s/%s.tex: no compila (revisar %s/%s/%s.log)" % (curso, slug, tmp, curso, slug))
        else:
            shutil.rmtree(tmp, ignore_errors=True)

for e in errores:
    print("ERROR:", e)
print("%d nota(s) revisada(s); %d error(es)" % (len(notas), len(errores)))
sys.exit(1 if errores else 0)
