# Instrucciones para actualizar la página

- La dueña es Arilín Haro; habla con ella en español.
- Nunca edites `index.html` a mano: edita `fuente/template.html` (textos en español, estilos, JS), agrega la traducción de cada texto nuevo o cambiado en `fuente/tr_en.py` (la clave es el texto exacto de un nodo de texto en español), y ejecuta `cd fuente && python3 build.py`.
- Datos de cursos: `META` y `EN` en `fuente/build.py`; contenido en `fuente/raw/*.txt` → `python3 parse.py`.
- Después de construir, revisa que no queden textos en español dentro de `<main data-lang="en">` y que los `<div>` estén balanceados en ambos `<main>`.
- La página es bilingüe: dos copias de `<main>` (es/en); botón ES|EN en la barra; el idioma se guarda en localStorage.
- Navegación por hash (`#cursos`, `#curso-<id>`, `#curso-<id>-videos`, `#recurso-python`, etc.).
- Mantén `.nojekyll` en la raíz.
- Enlaces de Drive rotos: lista en `fuente/enlaces_rotos.txt`; `build.py` los filtra y renumera ("Notas 1, 2…").
- Notas de los videos de los cursos: `notas/<curso>/<slug>.{tex,pdf,html}`, registro en `notas/notas.json`, reglas en `notas/CONVENCIONES.md`, herramientas en `tools/` (`nueva-nota.py crear|enganchar|buscar|cursos`, `verificar-notas.py --compilar`). `build.py` agrega a cada tema registrado los botones «Notas del video» y «Descargar PDF». Ninguna nota se sube sin la aprobación de Arilín.
