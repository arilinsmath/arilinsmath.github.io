"""Funciones compartidas por las herramientas de notas (ver notas/CONVENCIONES.md)."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTAS = os.path.join(ROOT, "notas")
FUENTE = os.path.join(ROOT, "fuente")
REGISTRO = os.path.join(NOTAS, "notas.json")
CONV = os.path.join(NOTAS, "CONVENCIONES.md")
PLANT = os.path.join(ROOT, "tools", "plantillas")
NOMBRES = {"defn": "Definición", "prop": "Proposición", "teo": "Teorema", "lema": "Lema", "cor": "Corolario"}


def leer(p):
    with open(p, encoding="utf8") as f:
        return f.read()


def escribir(p, s):
    with open(p, "w", encoding="utf8") as f:
        f.write(s)


def sin_comentarios_tex(t):
    return re.sub(r"(?m)(?<!\\)%.*$", "", t)


def cursos():
    """Devuelve {slug_del_curso: {"titulo":..., "unidades":[{"titulo":..., "temas":[{"t":..., "videos":[id,...]}]}]}}
    a partir de fuente/courses.json y de los slugs de fuente/build.py (los mismos de la página)."""
    b = leer(os.path.join(FUENTE, "build.py"))
    ids = dict(re.findall(r"'(\w+)':dict\(slug='([^']+)'", b))
    excluidos = set(re.findall(r"c\['id'\]!='(\w+)'", b))
    titulos = dict(re.findall(r"'(\w+)':'([^']+)'", re.search(r"TITLES=\{([^}]*)\}", b).group(1)))
    out = {}
    for c in json.loads(leer(os.path.join(FUENTE, "courses.json"))):
        if c["id"] in excluidos or c["id"] not in ids:
            continue
        unidades = []
        for u in c["units"]:
            temas = []
            for t in u["topics"]:
                vids = []
                for r in t["res"]:
                    m = re.search(r"youtube\.com/watch\?v=([\w-]{11})", r["u"])
                    if m and r["k"] == "v":
                        vids.append(m.group(1))
                temas.append({"t": t["title"], "videos": vids})
            unidades.append({"titulo": re.sub(r"^Unidad \d+\.\s*", "", u["title"]), "temas": temas})
        out[ids[c["id"]]] = {"titulo": titulos.get(c["id"], c["title"]), "unidades": unidades}
    return out


def registro():
    return json.loads(leer(REGISTRO)) if os.path.exists(REGISTRO) else []


def guardar_registro(r):
    escribir(REGISTRO, json.dumps(r, ensure_ascii=False, indent=1) + "\n")


def datos_nota(curso, slug):
    """(unidad, primer_numero, [tipos de enunciados], texto) de notas/<curso>/<slug>.tex"""
    t = sin_comentarios_tex(leer(os.path.join(NOTAS, curso, slug + ".tex")))
    m = re.search(r"^\\unidad\{(\d+)\}\{(\d+)\}", t, re.M)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), re.findall(r"\\begin\{(defn|prop|teo|lema|cor)\}", t), t


def todas_las_notas():
    """Lista de (curso, slug) de todos los .tex de notas/<curso>/."""
    res = []
    if not os.path.isdir(NOTAS):
        return res
    for curso in sorted(os.listdir(NOTAS)):
        d = os.path.join(NOTAS, curso)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.endswith(".tex"):
                    res.append((curso, f[:-4]))
    return res


def siguiente_libre(curso, unidad, excluir=None):
    n = 1
    for c, s in todas_las_notas():
        if c != curso or s == excluir:
            continue
        d = datos_nota(c, s)
        if d and d[0] == unidad:
            n = max(n, d[1] + len(d[2]))
    return n


def buscar_video(video_id):
    """[(curso, unidad, tema, numero_de_video)] donde aparece el video."""
    res = []
    for cs, c in cursos().items():
        for ui, u in enumerate(c["unidades"], 1):
            for t in u["temas"]:
                if video_id in t["videos"]:
                    res.append((cs, ui, t["t"], t["videos"].index(video_id) + 1))
    return res


def actualizar_tabla():
    """Reescribe la tabla de numeración de CONVENCIONES.md (entre marcadores) a partir de las notas."""
    reg = registro()
    C = cursos()
    filas = {}
    for c, s in todas_las_notas():
        d = datos_nota(c, s)
        if not d:
            continue
        u, n, tipos, _ = d
        e = next((x for x in reg if x["curso"] == c and x["slug"] == s), None)
        estado = ("Video %d" % e["video"]) if e else "borrador"
        rango = ("%d.%d a %d.%d" % (u, n, u, n + len(tipos) - 1) if len(tipos) > 1 else "%d.%d" % (u, n)) if tipos else "sin enunciados"
        filas.setdefault((c, u), []).append((n, "`%s` (%s; %s)" % (s, estado, rango)))
    lineas = ["| Curso | Unidad | Notas (en orden) | Siguiente libre |", "|---|---|---|---|"]
    for (c, u), L in sorted(filas.items()):
        titulo_u = C[c]["unidades"][u - 1]["titulo"] if c in C and u <= len(C[c]["unidades"]) else "?"
        lineas.append("| %s | %d. %s | %s | %d.%d |" % (C.get(c, {}).get("titulo", c), u, titulo_u,
                      ", ".join(x for _, x in sorted(L)), u, siguiente_libre(c, u)))
    if len(lineas) == 2:
        lineas.append("| (aún no hay notas) | | | |")
    t = leer(CONV)
    a, b = "<!-- tabla-numeracion -->", "<!-- /tabla-numeracion -->"
    i, j = t.index(a) + len(a), t.index(b)
    escribir(CONV, t[:i] + "\n" + "\n".join(lineas) + "\n" + t[j:])
