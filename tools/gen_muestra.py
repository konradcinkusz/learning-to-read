#!/usr/bin/env python3
"""Genera content/generated-muestra.tex: una muestra de 10 días reales por
trimestre, para comparar de un vistazo cómo sube el nivel a lo largo del
curso (1/2/3/4 frases, la complejidad, el tipo de actividad).

NO es contenido de producción y NO afecta al cuaderno real (main.tex /
main-bw.tex): reutiliza los días 1-15 ya escritos de content/q1.json (el
verdadero Trimestre 1) más content/muestra/q2.json, q3.json, q4.json --
los días 66-80, 131-145 y 196-210 reales de los otros tres trimestres,
escritos ya con su número de día, semana y trimestre definitivos, pero
guardados fuera de content/ (en content/muestra/) a propósito: el glob
`content/q*.json` que usa tools/gen_days.py para el libro real NO debe
verlos mientras los días que faltan entre medias (16-65, 81-130,
146-195) no existan -- si los viera, el libro real fallaría su propia
comprobación de continuidad (`validar_dias`, 1..260 sin huecos).

Cuando se escriban esas semanas que faltan, el contenido de
content/muestra/q{2,3,4}.json se traslada tal cual a content/q{2,3,4}.json
y este script deja de hacer falta.

Reutiliza render_actividad/escapar/PLANTILLA_DIA de gen_days.py en vez de
duplicarlos, para que una muestra nunca se pueda renderizar de forma
distinta al libro real.

Uso:
    python3 tools/gen_muestra.py            # regenera content/generated-muestra.tex
    python3 tools/gen_muestra.py --check    # solo valida, no escribe nada
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_days import (  # noqa: E402
    ErrorDeContenido,
    FRASES_POR_TRIMESTRE,
    PLANTILLA_DIA,
    RANGO_TRIMESTRE,
    escapar,
    render_actividad,
)

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
MUESTRA_DIR = CONTENT_DIR / "muestra"
OUTPUT_FILE = CONTENT_DIR / "generated-muestra.tex"

# El Trimestre 1 real ya está en content/q1.json (producción); los demás
# viven en content/muestra/, fuera del glob del libro real.
FICHEROS = [
    CONTENT_DIR / "q1.json",
    MUESTRA_DIR / "q2.json",
    MUESTRA_DIR / "q3.json",
    MUESTRA_DIR / "q4.json",
]


def cargar_dias():
    dias = []
    for fichero in FICHEROS:
        if not fichero.exists():
            raise ErrorDeContenido(f"no existe {fichero}")
        datos = json.loads(fichero.read_text(encoding="utf-8"))
        dias.extend(datos.get("dias", []))
    return dias


def validar_dia(d):
    """Las mismas reglas que gen_days.validar_dias aplicadas a UN día --
    trimestre válido, número dentro del rango de ese trimestre, número de
    frases correcto, frases bien terminadas -- pero sin exigir que los
    días de la muestra sean consecutivos entre sí (lo son dentro de cada
    bloque de 10, que es lo que importa)."""
    num = d["dia"]
    trimestre = d.get("trimestre")
    if trimestre not in RANGO_TRIMESTRE:
        raise ErrorDeContenido(f"día {num}: trimestre inválido: {trimestre!r}")

    lo, hi = RANGO_TRIMESTRE[trimestre]
    if not (lo <= num <= hi):
        raise ErrorDeContenido(
            f"día {num}: dice ser del trimestre {trimestre} (días {lo}-{hi}) "
            "pero su número no está en ese rango"
        )

    oraciones = d.get("oraciones", [])
    esperado_frases = FRASES_POR_TRIMESTRE[trimestre]
    if len(oraciones) != esperado_frases:
        raise ErrorDeContenido(
            f"día {num} (trimestre {trimestre}): debería tener "
            f"{esperado_frases} frase(s), tiene {len(oraciones)}"
        )
    for frase in oraciones:
        if not frase.strip().endswith((".", "!", "?", "¡", "¿")):
            raise ErrorDeContenido(
                f"día {num}: la frase «{frase}» no termina en un signo de "
                "puntuación final"
            )


def generar_tex(dias):
    piezas = [
        "% content/generated-muestra.tex\n",
        "% GENERADO por tools/gen_muestra.py -- NO EDITAR A MANO.\n",
        "% Una muestra de 10 días reales por trimestre (ver la cabecera de\n",
        "% tools/gen_muestra.py), NO el libro completo -- no forma parte de\n",
        "% main.tex ni de main-bw.tex.\n\n",
    ]
    for d in dias:
        actividad_tex = render_actividad(d["dia"], d["actividad"])
        oraciones = " ".join(escapar(o) for o in d["oraciones"])
        piezas.append(
            PLANTILLA_DIA.substitute(
                dia=d["dia"],
                semana=d["semana"],
                trimestre=d["trimestre"],
                oraciones=oraciones,
                actividad=actividad_tex,
            )
        )
    return "\n".join(piezas)


def main():
    check_only = "--check" in sys.argv

    try:
        dias = cargar_dias()
        for d in dias:
            validar_dia(d)
        tex = generar_tex(dias)
    except ErrorDeContenido as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if check_only:
        actual = OUTPUT_FILE.read_text(encoding="utf-8") if OUTPUT_FILE.exists() else None
        if actual != tex:
            print(
                "DESACTUALIZADO: content/generated-muestra.tex no coincide -- "
                "ejecuta `make generate-muestra`.",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {len(dias)} días de muestra validados, al día.")
        return 0

    OUTPUT_FILE.write_text(tex, encoding="utf-8")
    print(f"Escrito {OUTPUT_FILE} con {len(dias)} días de muestra.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
