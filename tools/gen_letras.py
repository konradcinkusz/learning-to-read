#!/usr/bin/env python3
"""Genera content/generated-letras.tex (las páginas de trazo, una por
letra del alfabeto) a partir de content/letras-trazo.json (los puntos
de contorno, ver tools/gen_letras_puntos.py) y content/palabras-trazo.json
(la palabra de ejemplo de cada letra).

Deliberadamente NO depende de matplotlib/numpy/fonttools -- esos hacen
falta solo para tools/gen_letras_puntos.py (que ya dejó su resultado en
content/letras-trazo.json, versionado en git). Este script es tan
ligero como tools/gen_days.py, así que `make generate` y el job
`gates` de CI no ganan una dependencia pesada por esta función.

No editar a mano content/generated-letras.tex -- se sobrescribe cada
vez que se ejecuta este script.

Uso:
    python3 tools/gen_letras.py            # regenera content/generated-letras.tex
    python3 tools/gen_letras.py --check    # solo valida
"""

import json
import sys
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
PUNTOS_FILE = CONTENT_DIR / "letras-trazo.json"
PALABRAS_FILE = CONTENT_DIR / "palabras-trazo.json"
OUTPUT_FILE = CONTENT_DIR / "generated-letras.tex"

LETRAS = list("abcdefghijklmnñopqrstuvwxyz")

# cm por unidad "em" (tamaño de fuente = 1.0 en letras-trazo.json).
# Elegido para que el par más ancho (mayúscula + minúscula de la "w",
# la letra más ancha del alfabeto en Andika) siga cabiendo dentro del
# área de texto de la página (170 mm, ver \geometry en preamble.tex)
# con margen -- ver notes/02-revision-y-plan.md.
ESCALA_CM = 7.8
HUECO_EM = 0.18  # espacio entre mayúscula y minúscula, en em
RADIO_PUNTO_CM = "0.09"


class ErrorDeContenido(Exception):
    pass


def escapar(texto):
    sustituciones = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    for viejo, nuevo in sustituciones:
        texto = texto.replace(viejo, nuevo)
    return texto


PLANTILLA_LETRA = Template(
    r"""\paginaLetra{$mayus}{$minus}{$palabra}{%
\begin{tikzpicture}
\fill[colorLectura] $puntos;
\end{tikzpicture}%
}
"""
)


def puntos_tikz(entrada_mayus, entrada_minus):
    """Todos los puntos de una letra (mayúscula + minúscula), colocados
    uno junto al otro sobre la misma línea base: la mayúscula empieza
    en x=0, la minúscula empieza justo después de HUECO_EM. No hace
    falta centrar en la página -- \\paginaLetra envuelve el
    tikzpicture en \\begin{center}, y su ancho es el de su propio
    contenido, así que el centrado sale gratis."""
    uc_bbox = entrada_mayus["bbox"]
    lc_bbox = entrada_minus["bbox"]
    ancho_mayus = uc_bbox[2] - uc_bbox[0]

    piezas = []
    for x, y in (pt for contorno in entrada_mayus["contornos"] for pt in contorno):
        cx = (x - uc_bbox[0]) * ESCALA_CM
        cy = y * ESCALA_CM
        piezas.append(f"({cx:.3f},{cy:.3f}) circle ({RADIO_PUNTO_CM})")

    despl_x = ancho_mayus + HUECO_EM - lc_bbox[0]
    for x, y in (pt for contorno in entrada_minus["contornos"] for pt in contorno):
        cx = (x + despl_x) * ESCALA_CM
        cy = y * ESCALA_CM
        piezas.append(f"({cx:.3f},{cy:.3f}) circle ({RADIO_PUNTO_CM})")

    return " ".join(piezas)


def generar_tex(puntos, palabras):
    piezas = [
        "% content/generated-letras.tex\n",
        "% GENERADO por tools/gen_letras.py a partir de\n",
        "% content/letras-trazo.json y content/palabras-trazo.json.\n",
        "% NO EDITAR A MANO -- los cambios se perderán en la siguiente\n",
        "% ejecución de `make generate`.\n\n",
    ]
    for letra in LETRAS:
        if letra not in puntos:
            raise ErrorDeContenido(
                f"letra {letra!r}: no está en {PUNTOS_FILE.name} -- "
                "ejecuta tools/gen_letras_puntos.py"
            )
        if letra not in palabras:
            raise ErrorDeContenido(
                f"letra {letra!r}: no tiene palabra de ejemplo en "
                f"{PALABRAS_FILE.name}"
            )
        entrada = puntos[letra]
        piezas.append(
            PLANTILLA_LETRA.substitute(
                mayus=escapar(letra.upper()),
                minus=escapar(letra),
                palabra=escapar(palabras[letra]),
                puntos=puntos_tikz(entrada["mayuscula"], entrada["minuscula"]),
            )
        )
    return "\n".join(piezas)


def main():
    check_only = "--check" in sys.argv

    if not PUNTOS_FILE.exists():
        print(
            f"ERROR: no existe {PUNTOS_FILE} -- ejecuta "
            "tools/gen_letras_puntos.py primero (requiere matplotlib/numpy/fonttools).",
            file=sys.stderr,
        )
        return 1

    puntos = json.loads(PUNTOS_FILE.read_text(encoding="utf-8"))
    puntos.pop("_comentario", None)
    palabras = json.loads(PALABRAS_FILE.read_text(encoding="utf-8"))["palabras"]

    try:
        tex = generar_tex(puntos, palabras)
    except ErrorDeContenido as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if check_only:
        actual = OUTPUT_FILE.read_text(encoding="utf-8") if OUTPUT_FILE.exists() else None
        if actual != tex:
            print(
                f"DESACTUALIZADO: {OUTPUT_FILE} no coincide con "
                f"{PUNTOS_FILE.name}/{PALABRAS_FILE.name} -- ejecuta `make generate`.",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {len(LETRAS)} letras validadas, {OUTPUT_FILE.name} al día.")
        return 0

    OUTPUT_FILE.write_text(tex, encoding="utf-8")
    print(f"Escrito {OUTPUT_FILE} con {len(LETRAS)} letras.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
