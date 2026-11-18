#!/usr/bin/env python3
"""Herramienta para las notas de los videos de los cursos (ver notas/CONVENCIONES.md).

  python3 tools/nueva-nota.py cursos
      Lista los cursos (slug), sus unidades y temas, con sus videos.

  python3 tools/nueva-nota.py buscar --video-id ID
      Dice en qué curso, unidad y tema está el video, y qué número de video es dentro del tema.

  python3 tools/nueva-nota.py crear --curso C --slug S --titulo T --video-id ID [--unidad U]
          [--titulo-video TV] [--resumen R] [--credito "video de Luis Jorge Sánchez Saldaña, "]
      Crea notas/C/S.tex y S.html desde tools/plantillas/. Si no se da --unidad, se toma la del
      video. El primer número de enunciado sale de las notas existentes de esa unidad. No toca la página.

  python3 tools/nueva-nota.py enganchar --curso C --slug S [--tema "Título exacto"] [--video N]
      Agrega la nota a notas/notas.json (queda visible en la página tras reconstruirla), actualiza la
      tabla de CONVENCIONES.md y reconstruye index.html. Si no se dan --tema/--video, se deducen del
      \\videoid de la nota. Usar SOLO después de que Arilín apruebe el borrador.
"""
import argparse, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from notas_comun import *


def cmd_cursos(a):
    for cs, c in cursos().items():
        print("\n%s  —  %s" % (cs, c["titulo"]))
        for ui, u in enumerate(c["unidades"], 1):
            print("  Unidad %d. %s" % (ui, u["titulo"]))
            for t in u["temas"]:
                print("     - %s  [%d video(s): %s]" % (t["t"], len(t["videos"]), " ".join(t["videos"])))


def cmd_buscar(a):
    r = buscar_video(a.video_id)
    if not r:
        sys.exit("El video %s no aparece en ningún curso de la página." % a.video_id)
    for cs, u, t, n in r:
        print("curso=%s  unidad=%d  tema=%r  video=%d" % (cs, u, t, n))


def cmd_crear(a):
    C = cursos()
    if a.curso not in C:
        sys.exit("Curso desconocido %r. Cursos: %s" % (a.curso, ", ".join(C)))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a.slug):
        sys.exit("El slug debe ir en minúsculas, sin acentos, con guiones")
    u = a.unidad
    if u is None:
        r = [x for x in buscar_video(a.video_id) if x[0] == a.curso]
        if not r:
            sys.exit("El video no está en el curso %s; da --unidad a mano" % a.curso)
        u = r[0][1]
    n = siguiente_libre(a.curso, u)
    d = os.path.join(NOTAS, a.curso)
    os.makedirs(d, exist_ok=True)
    sub = {"@SLUG@": a.slug, "@CURSO@": a.curso, "@UNIDAD@": str(u), "@N@": str(n), "@TITULO@": a.titulo,
           "@VIDEOID@": a.video_id, "@TITULOVIDEO@": a.titulo_video or a.titulo,
           "@NOMBRECURSO@": C[a.curso]["titulo"], "@CREDITO@": a.credito or "",
           "@RESUMEN@": a.resumen or "Preparan ..."}
    for ext in ("tex", "html"):
        dest = os.path.join(d, a.slug + "." + ext)
        if os.path.exists(dest):
            sys.exit("Ya existe " + dest)
        s = leer(os.path.join(PLANT, "nota." + ext))
        for k, v in sub.items():
            s = s.replace(k, v)
        escribir(dest, s)
        print("creado", os.path.relpath(dest, ROOT))
    actualizar_tabla()
    print("Unidad %d (%s); primer enunciado numerado: %d.%d" % (u, C[a.curso]["unidades"][u - 1]["titulo"], u, n))


def cmd_enganchar(a):
    C = cursos()
    if a.curso not in C:
        sys.exit("Curso desconocido %r" % a.curso)
    base = os.path.join(NOTAS, a.curso, a.slug)
    for ext in ("tex", "html", "pdf"):
        if not os.path.exists(base + "." + ext):
            sys.exit("Falta notas/%s/%s.%s" % (a.curso, a.slug, ext))
    d = datos_nota(a.curso, a.slug)
    if not d:
        sys.exit("El .tex no declara \\unidad{u}{n}")
    u = d[0]
    vid = re.search(r"\\newcommand\{\\videoid\}\{([\w-]+)\}", d[3]).group(1)
    tema, video = a.tema, a.video
    if not tema:
        r = [x for x in buscar_video(vid) if x[0] == a.curso]
        if len(r) != 1:
            sys.exit("No pude deducir el tema del video %s en %s (%d coincidencias); da --tema y --video" % (vid, a.curso, len(r)))
        _, ui, tema, video = r[0]
    temas = [(ui, t) for ui, un in enumerate(C[a.curso]["unidades"], 1) for t in un["temas"] if t["t"] == tema]
    if len(temas) != 1:
        sys.exit("El tema %r aparece %d veces en el curso (debe ser 1)" % (tema, len(temas)))
    ui, t = temas[0]
    if ui != u:
        sys.exit("El tema está en la unidad %d pero la nota declara la unidad %d" % (ui, u))
    video = video or 1
    if video < 1 or video > max(1, len(t["videos"])):
        sys.exit("El tema tiene %d video(s); --video fuera de rango" % len(t["videos"]))
    reg = [x for x in registro() if not (x["curso"] == a.curso and x["slug"] == a.slug)]
    reg = [x for x in reg if not (x["curso"] == a.curso and x["tema"] == tema and x["video"] == video)]
    reg.append({"curso": a.curso, "unidad": u, "tema": tema, "video": video, "slug": a.slug})
    guardar_registro(reg)
    actualizar_tabla()
    subprocess.run([sys.executable, os.path.join(FUENTE, "build.py")], check=True)
    print("enganchada: %s -> %s, unidad %d, tema %r, video %d" % (a.slug, a.curso, u, tema, video))


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sp = p.add_subparsers(dest="cmd", required=True)
sp.add_parser("cursos").set_defaults(f=cmd_cursos)
b = sp.add_parser("buscar"); b.set_defaults(f=cmd_buscar); b.add_argument("--video-id", required=True)
c = sp.add_parser("crear"); c.set_defaults(f=cmd_crear)
c.add_argument("--curso", required=True); c.add_argument("--slug", required=True)
c.add_argument("--titulo", required=True); c.add_argument("--video-id", required=True)
c.add_argument("--unidad", type=int); c.add_argument("--titulo-video"); c.add_argument("--resumen")
c.add_argument("--credito", help='p. ej. "video de Luis Jorge Sánchez Saldaña, " cuando el video no es de Arilín')
e = sp.add_parser("enganchar"); e.set_defaults(f=cmd_enganchar)
e.add_argument("--curso", required=True); e.add_argument("--slug", required=True)
e.add_argument("--tema"); e.add_argument("--video", type=int)
a = p.parse_args()
a.f(a)
