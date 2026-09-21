#!/usr/bin/env python3
"""Extrae el contorno real de cada letra del alfabeto español, desde la
propia fuente del cuaderno (fonts/andika/Andika-Bold.ttf), y lo guarda
como una nube de puntos en content/letras-trazo.json.

Herramienta de desarrollo, NO forma parte de `make generate`: se
ejecuta a mano solo si cambia la fuente o el conjunto de letras -- su
salida (content/letras-trazo.json) SÍ se versiona en git, precisamente
para que el resto del pipeline (tools/gen_letras.py, que compone las
páginas de content/generated-letras.tex) no dependa de matplotlib ni de
fontTools. Ver notes/02-revision-y-plan.md para el porqué de esta
separación en dos pasos.

Requiere matplotlib, numpy y fonttools (no son dependencias del
proyecto -- instálalas aparte: pip install matplotlib numpy fonttools).

Uso:
    python3 tools/gen_letras_puntos.py
"""

import json
import sys
from pathlib import Path

try:
    import numpy as np
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
except ImportError:
    print(
        "ERROR: hacen falta matplotlib, numpy y fonttools -- "
        "pip install matplotlib numpy fonttools",
        file=sys.stderr,
    )
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT / "fonts" / "andika" / "Andika-Bold.ttf"
OUTPUT_FILE = ROOT / "content" / "letras-trazo.json"

# El alfabeto español (RAE, sin ch/ll como letras aparte desde 2010).
LETRAS = list("abcdefghijklmnñopqrstuvwxyz")

# Distancia entre puntos, en unidades de em (tamaño de fuente = 1.0) --
# ajustada a ojo: suficientemente densa para que el contorno se lea
# como una letra desde lejos, suficientemente separada para que cada
# punto sea un objetivo claro donde apoyar el lápiz.
ESPACIADO_PUNTOS_EM = 0.028


def contornos_de_letra(caracter, ruta_fuente, espaciado=ESPACIADO_PUNTOS_EM):
    """Devuelve una lista de contornos (uno por trazo cerrado del
    glifo -- por ejemplo, la 'o' tiene uno, la 'i' tiene dos: el palo y
    el punto), cada uno como lista de (x, y) repartidos a distancia de
    arco aproximadamente constante a lo largo del contorno real.

    Usa TextPath (FreeType, vía matplotlib) en vez de leer los
    contornos TrueType a mano: FreeType ya resuelve la parte delicada
    -- convertir las curvas cuadráticas de la fuente en segmentos
    rectos con los puntos de control implícitos de TrueType (varios
    puntos "off-curve" seguidos) correctamente aplanados.
    """
    fp = FontProperties(fname=str(ruta_fuente))
    tp = TextPath((0, 0), caracter, size=1.0, prop=fp)
    contornos = []
    for poligono in tp.to_polygons():
        poligono = np.asarray(poligono)
        if len(poligono) < 3:
            continue
        longitud_segmento = np.hypot(*np.diff(poligono, axis=0).T)
        longitud_arco = np.concatenate([[0], np.cumsum(longitud_segmento)])
        total = longitud_arco[-1]
        if total <= 0:
            continue
        n = max(int(round(total / espaciado)), 4)
        objetivos = np.linspace(0, total, n, endpoint=False)
        xs = np.interp(objetivos, longitud_arco, poligono[:, 0])
        ys = np.interp(objetivos, longitud_arco, poligono[:, 1])
        contornos.append(
            list(zip(np.round(xs, 4).tolist(), np.round(ys, 4).tolist()))
        )
    return contornos


def main():
    if not FONT_PATH.exists():
        print(f"ERROR: no existe {FONT_PATH}", file=sys.stderr)
        return 1

    datos = {
        "_comentario": (
            "Puntos de contorno (glifo real de fonts/andika/Andika-Bold.ttf, "
            "vía fontTools/matplotlib) para las páginas de trazo -- "
            "GENERADO por tools/gen_letras_puntos.py, no editar a mano. "
            "Unidades: em (tamaño de fuente = 1.0), origen en la línea base."
        )
    }
    for letra in LETRAS:
        entrada = {}
        for caso, caracter in [("mayuscula", letra.upper()), ("minuscula", letra)]:
            contornos = contornos_de_letra(caracter, FONT_PATH)
            xs = [x for c in contornos for x, _ in c]
            ys = [y for c in contornos for _, y in c]
            entrada[caso] = {
                "contornos": contornos,
                "bbox": [min(xs), min(ys), max(xs), max(ys)] if xs else [0, 0, 0, 0],
            }
        datos[letra] = entrada
        print(f"{letra}: OK")

    OUTPUT_FILE.write_text(
        json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"Escrito {OUTPUT_FILE} con {len(LETRAS)} letras.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
