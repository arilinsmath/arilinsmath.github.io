# Herramientas de las notas de los videos

Ver `notas/CONVENCIONES.md`. Resumen:

    python3 tools/nueva-nota.py cursos                     # cursos, unidades, temas y videos
    python3 tools/nueva-nota.py buscar --video-id ID       # dónde está un video
    python3 tools/nueva-nota.py crear --curso C --slug S --titulo T --video-id ID
    python3 tools/verificar-notas.py --compilar            # debe dar 0 errores
    python3 tools/nueva-nota.py enganchar --curso C --slug S   # solo tras la aprobación de Arilín
