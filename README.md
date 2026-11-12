# Arilín Haro · Página personal

Página personal de la Dra. Arilín Haro: matemática, docente y divulgadora.
Publicada con GitHub Pages en **https://arilinsmath.github.io**.

## Qué hay en este repositorio

| Ruta | Qué es |
|---|---|
| `index.html` | La página completa (bilingüe español/inglés, un solo archivo). **Es lo que se publica.** |
| `favicon.ico` | Ícono de la pestaña del navegador. |
| `logo/` | Logotipo en PNG y SVG (horizontal, cuadrado, ícono). |
| `fuente/` | Archivos de trabajo para regenerar `index.html`. |

## Cómo se actualiza

`index.html` se genera desde `fuente/`; no se edita a mano.

- `fuente/template.html`: estructura, estilos, textos en español y código de la página.
- `fuente/tr_en.py`: traducciones al inglés de los textos de `template.html`.
- `fuente/build.py`: datos e información de cada curso (español e inglés). Genera `../index.html`.
- `fuente/raw/*.txt` + `fuente/parse.py`: material de los cursos (videos, notas, cuestionarios) tal como está en Arilín's Math World; `parse.py` lo convierte en `courses.json`.
- `fuente/retrato.webp`: foto de perfil.
- `fuente/logo.py`: genera el logotipo.

Para regenerar la página:

```bash
cd fuente
python3 parse.py   # solo si cambió algo en raw/
python3 build.py   # escribe ../index.html
```
