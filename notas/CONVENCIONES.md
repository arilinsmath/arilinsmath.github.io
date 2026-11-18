# Convenciones de las notas de los videos

Notas escritas de los videos de los cursos de Arilín Haro que aparecen en su página personal (https://arilinsmath.github.io/#cursos): Álgebra Superior I y II, Álgebra para Física, Geometría Analítica I, Teoría de grupos y LaTeX en Overleaf. Este archivo es la referencia para que todas las notas sean consistentes; léelo, y lee las notas ya hechas del mismo curso, antes de escribir una nueva.

## Archivos de cada nota

Cada nota vive en `notas/<curso>/`, donde `<curso>` es el identificador del curso en la página (`algebra-superior-1`, `algebra-superior-2`, `algebra-fisica`, `geometria-analitica-1`, `teoria-de-grupos`, `latex-en-overleaf`; `python3 tools/nueva-nota.py cursos` los lista con sus unidades, temas y videos). Todos los archivos de una nota comparten el nombre base (el *slug*: minúsculas, sin acentos, con guiones):

- `<slug>.tex`: fuente en LaTeX. Empieza con `\documentclass[11pt]{article}`, define `\videoid{...}` (identificador del video de YouTube), hace `\input{../preambulo}` y declara `\curso{<curso>}` y `\unidad{u}{n}`.
- `<slug>.pdf`: PDF compilado con LuaLaTeX (`latexmk -lualatex <slug>.tex`, desde `notas/<curso>/`).
- `<slug>.html`: fragmento HTML que la página carga al desplegar las notas.
- Si un tema tiene varios videos con notas, el segundo lleva el sufijo `-2`, el tercero `-3`, etc.
- `notas/preambulo.tex`: paquetes, colores, entornos de enunciados (`defn`, `prop`, `teo`, `lema`, `cor`, `ejem`) y entorno `erratas`, compartidos por todas las notas. Un cambio de estilo se hace ahí, una sola vez.

Un mismo video puede aparecer en dos cursos (por ejemplo, Álgebra Superior I y Álgebra para Física comparten videos). La nota se escribe una vez, en el curso donde se pidió; si se quiere también en el otro, se copia a la otra carpeta con su propia numeración.

## Cómo se engancha una nota a la página

La página se genera con `fuente/build.py` a partir de `fuente/courses.json`. Las notas publicadas se registran en `notas/notas.json`:

```
{"curso": "algebra-superior-1", "unidad": 1, "tema": "Proposiciones, conectores y cuantificadores.", "video": 1, "slug": "proposiciones"}
```

`tema` es el título exacto del tema en el curso y `video` el número del video dentro del tema (en el orden de los botones de video). `build.py` agrega al tema el botón desplegable «Notas del video» con la etiqueta del video correspondiente y el botón «PDF». Las fórmulas del fragmento HTML usan `\( ... \)` y `\[ ... \]` y se dibujan con KaTeX al abrir las notas. `tools/nueva-nota.py enganchar` hace todo esto (deduce el tema y el número de video a partir del `\videoid`) y reconstruye `index.html`.

## Pasos para una nota nueva

1. Leer este archivo y las notas ya hechas del curso (`.tex`) para reutilizar notación y estilo.
2. Obtener del video la transcripción y capturas de lo que se escribe o dibuja en pantalla. `python3 tools/nueva-nota.py buscar --video-id ID` dice en qué curso, unidad y tema está.
3. `python3 tools/nueva-nota.py crear --curso ... --slug ... --titulo ... --video-id ...` crea el `.tex` y el `.html` desde `tools/plantillas/` con el número de enunciado que toca. Si el video no es de Arilín, usar `--credito "video de Nombre Apellido, "`.
4. Escribir el contenido del `.tex` y del `.html` (las figuras en TikZ y en SVG) y compilar el PDF con LuaLaTeX.
5. `python3 tools/verificar-notas.py --compilar` debe terminar sin errores.
6. **Borrador:** mostrar a Arilín el PDF y una captura de cómo se ve en la página, y esperar su aprobación. Nada se sube a `main` antes.
7. Con la aprobación: `python3 tools/nueva-nota.py enganchar --curso ... --slug ...`, verificar de nuevo, subir a `main` y comprobar la página en línea.

## Numeración de enunciados por unidad

Definiciones, proposiciones, teoremas, lemas y corolarios comparten **un solo contador por curso y unidad** (1.1, 1.2, ...), para poder hacer referencias cruzadas. La unidad es la del curso en la página (Unidad 1, 2, ... en el orden en que aparecen). `crear` calcula el primer número libre; las notas de una unidad deben escribirse en el orden del curso, y si se escribe una nota intermedia después, hay que renumerar las que le siguen. Los ejemplos (`ejem`) no usan este contador.

Tabla generada por `crear` y `enganchar` (no editar a mano; las notas sin enganchar aparecen como «borrador»):

<!-- tabla-numeracion -->
| Curso | Unidad | Notas (en orden) | Siguiente libre |
|---|---|---|---|
| (aún no hay notas) | | | |
<!-- /tabla-numeracion -->

## Notación

- Conjuntos de números: \(\mathbb{N}\) (naturales, empezando en 0 o en 1 según lo diga el video; aclararlo en la nota), \(\mathbb{Z}\), \(\mathbb{Q}\), \(\mathbb{R}\), \(\mathbb{C}\).
- Lógica: conectores \(\neg\), \(\wedge\), \(\vee\), \(\Rightarrow\), \(\Leftrightarrow\); cuantificadores \(\forall\), \(\exists\).
- Conjuntos: complemento \(A^c\), diferencia \(A\setminus B\), conjunto potencia \(\mathcal{P}(A)\), producto cartesiano \(A\times B\).
- Funciones: \(f\colon A\to B\); imagen \(f(A)\), preimagen \(f^{-1}(B)\); composición \(g\circ f\).
- Congruencias: \(a\equiv b \pmod n\); enteros módulo \(n\): \(\mathbb{Z}_n\).
- Geometría analítica: vectores en negrita en el PDF (\(\mathbf{v}\)) y en el HTML; producto punto \(\mathbf{u}\cdot\mathbf{v}\), producto cruz \(\mathbf{u}\times\mathbf{v}\).
- Se usa la notación del video. Cuando una nota introduzca notación nueva, agregarla aquí.

## Estilo

- Las notas siguen el video: no agregan resultados ni demostraciones que no estén en él. Si se agrega un comentario propio, se marca como «Comentario» (`\paragraph{Comentario.}` en el `.tex`, `<p class="com"><b>Comentario.</b> ...</p>` en el `.html`).
- Enunciados numerados: en el `.tex` con `defn`, `prop`, `teo`, `lema`, `cor` (se numeran solos, `u.n`; se pueden etiquetar con `\label` y citar con `\ref`). En el `.html` la etiqueta se escribe a mano: `<div class="def"><b>Definición 1.5 (nombre).</b> ...</div>` y `<div class="thm"><b>Proposición 1.6.</b> <i>enunciado</i></div>`. Tipos y números deben coincidir en PDF y HTML. Las demostraciones usan `proof` en el `.tex` y `<p><i>Demostración.</i> ... ∎</p>` en el `.html`.
- Ejemplos: `\begin{ejem}` en el `.tex` y `<div class="ej"><b>Ejemplo.</b> ...</div>` en el `.html`.
- Figuras: TikZ en el PDF y SVG en el HTML, con los mismos colores de la página: `tinta`, `oro`, `verdeazul` y `rosa` (en SVG, clases `s-...` para trazos y `t-...` para texto o relleno).
- En el `.tex`, el signo ¿ se escribe con la ligadura `?``, y las comillas latinas con `\guillemotleft{}` y `\guillemotright{}` (escritos directamente salen mal en el PDF). En el `.html` se escriben ¿ « » normales.
- `verificar-notas.py --compilar` compila en una copia aparte y **no** actualiza el `.pdf` del repositorio: después de cualquier cambio al `.tex` hay que recompilar el PDF (`latexmk -lualatex <slug>.tex` en `notas/<curso>/`) antes de subirlo.
- Las notas están en español (también en la versión en inglés de la página).

## Observaciones y erratas del video

La sección «Observaciones y erratas del video» **solo aparece si hay algún error que señalar**; si no hay, no se agrega nada ni se deja el título vacío.

- La transcripción automática de YouTube se equivoca con los términos matemáticos. Lo que parezca un error de la explicación se confirma con Arilín antes de publicarlo como errata.
- En LaTeX:

  ```
  \begin{erratas}
    \errata{203}{3:23}{Se dice ..., pero debe decir ...}
  \end{erratas}
  ```

  El primer argumento son los segundos (el enlace lleva al minuto exacto del video), el segundo es la marca visible y el tercero es el texto.
- En HTML, al final del fragmento:

  ```
  <div class="erratas"><h4>Observaciones y erratas del video</h4><ul>
    <li><a href="https://www.youtube.com/watch?v=ID&amp;t=203" target="_blank" rel="noopener">3:23</a> Se dice ..., pero debe decir ...</li>
  </ul></div>
  ```
