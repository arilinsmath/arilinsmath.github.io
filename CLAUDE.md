# Instrucciones para actualizar la página

- La dueña es Arilín Haro; habla con ella en español.
- Nunca edites `index.html` a mano: edita `fuente/template.html` (textos en español, estilos, JS), agrega la traducción de cada texto nuevo o cambiado en `fuente/tr_en.py` (la clave es el texto exacto de un nodo de texto en español), y ejecuta `cd fuente && python3 build.py`.
- Datos de cursos: `META` y `EN` en `fuente/build.py`; contenido en `fuente/raw/*.txt` → `python3 parse.py`.
- Después de construir, revisa que no queden textos en español dentro de `<main data-lang="en">` y que los `<div>` estén balanceados en ambos `<main>`.
- La página es bilingüe: dos copias de `<main>` (es/en); botón ES|EN en la barra; el idioma se guarda en localStorage.
- Navegación por hash (`#cursos`, `#curso-<id>`, `#curso-<id>-videos`, `#recurso-python`, etc.).
- Mantén `.nojekyll` en la raíz.
