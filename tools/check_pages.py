#!/usr/bin/env python3
"""Comprueba el invariante "1 día = 1 página" leyendo el .aux compilado.

Cada \\begin{diapagina}{N}{...}{...} escribe \\label{dia:N} como lo
primero que hace. LaTeX anota en el .aux, para cada \\label, la página en
la que cayó -- \\newlabel{dia:N}{{<ref>}{<pagina>}...}. Si un día ocupa
más de una página (el texto o la actividad no cupieron), el salto entre
la página del día N y la del día N+1 será mayor que 1, y este script lo
señala con el número de día exacto -- no hace falta compilar cada día
por separado ni mirar el PDF a ojo.

Uso:
    python3 tools/check_pages.py [main.aux]
    python3 tools/check_pages.py --allow-gaps main-muestra.aux

--allow-gaps salta la comprobación de que los números de día sean
consecutivos (para tools/gen_muestra.py, que solo renderiza una muestra
de días reales, con huecos deliberados entre trimestres) pero mantiene
la comprobación que de verdad importa: el salto de página entre dos
días RENDERIZADOS seguidos tiene que ser exactamente 1, venga o no
seguido el número de día -- \\end{diapagina} hace \\newpage siempre, así
que esa parte del invariante no depende de la continuidad.
"""

import re
import sys
from pathlib import Path

PATRON_LABEL = re.compile(r"\\newlabel\{dia:(\d+)\}\{\{[^{}]*\}\{(\d+)\}")


def leer_paginas(ruta_aux):
    texto = ruta_aux.read_text(encoding="utf-8", errors="replace")
    paginas = {}
    for m in PATRON_LABEL.finditer(texto):
        dia, pagina = int(m.group(1)), int(m.group(2))
        paginas[dia] = pagina
    return paginas


def main():
    allow_gaps = "--allow-gaps" in sys.argv
    posicionales = [a for a in sys.argv[1:] if not a.startswith("--")]
    ruta_aux = Path(posicionales[0] if posicionales else "main.aux")
    if not ruta_aux.exists():
        print(
            f"ERROR: no existe {ruta_aux} -- compila primero con "
            "`make build` (o `latexmk -pdf main.tex`).",
            file=sys.stderr,
        )
        return 1

    paginas = leer_paginas(ruta_aux)
    if not paginas:
        print(
            f"ERROR: {ruta_aux} no contiene ninguna etiqueta dia:N -- "
            "¿se generó content/generated-days.tex antes de compilar?",
            file=sys.stderr,
        )
        return 1

    dias_ordenados = sorted(paginas)
    problemas = []

    if not allow_gaps:
        esperado = dias_ordenados[0]
        for dia in dias_ordenados:
            if dia != esperado:
                problemas.append(f"falta el día {esperado} (o los días no son consecutivos)")
                esperado = dia
            esperado += 1

    for a, b in zip(dias_ordenados, dias_ordenados[1:]):
        salto = paginas[b] - paginas[a]
        if salto != 1:
            problemas.append(
                f"día {a} (página {paginas[a]}) -> día {b} (página {paginas[b]}): "
                f"salto de {salto} página(s), debería ser exactamente 1 "
                f"-- el día {a} probablemente se ha desbordado a una segunda página"
            )

    print(
        f"Días {dias_ordenados[0]}-{dias_ordenados[-1]}: "
        f"páginas {paginas[dias_ordenados[0]]}-{paginas[dias_ordenados[-1]]}."
    )
    if problemas:
        print("PROBLEMAS ENCONTRADOS:", file=sys.stderr)
        for p in problemas:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print(f"OK: los {len(dias_ordenados)} días ocupan exactamente una página cada uno.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
