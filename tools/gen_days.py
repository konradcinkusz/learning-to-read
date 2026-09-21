#!/usr/bin/env python3
"""Genera content/generated-days.tex a partir de content/q*.json.

No editar content/generated-days.tex a mano -- se sobrescribe cada vez
que se ejecuta este script. El fichero que SÍ se edita a mano es
content/q1.json (y, más adelante, q2.json, q3.json, q4.json), uno por
trimestre.

Uso:
    python3 tools/gen_days.py            # regenera content/generated-days.tex
    python3 tools/gen_days.py --check    # solo valida, no escribe nada;
                                          # falla (exit 1) si algo no
                                          # cuadra o si el fichero
                                          # generado está desactualizado
"""

import json
import random
import re
import sys
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT_FILE = CONTENT_DIR / "generated-days.tex"

TOTAL_DIAS = 260
FRASES_POR_TRIMESTRE = {1: 1, 2: 2, 3: 3, 4: 4}
RANGO_TRIMESTRE = {1: (1, 65), 2: (66, 130), 3: (131, 195), 4: (196, 260)}

TIPOS_VALIDOS = {
    "dibuja", "completa", "copia", "responde", "relaciona", "adivina", "crea",
    "repasa",
}

# En el trimestre 1 la niña todavía no compone una respuesta escrita por
# sí sola -- "responde" (pregunta abierta) no se usa hasta que sepa
# hacerlo; "copia" (repasar la frase, tres veces) es lo que hay en su
# lugar. Ver notes/01-curriculum.md, "Rotación de actividades".
TRIMESTRES_SIN_RESPONDE = {1}


class ErrorDeContenido(Exception):
    """Un día no cumple las reglas -- el mensaje ya dice cuál y por qué."""


def escapar(texto):
    """Escapa los caracteres especiales de LaTeX en texto libre (JSON)."""
    if texto is None:
        return ""
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


# --- una plantilla (string.Template, sustitución $var) por tipo de
#     actividad -- usar Template en vez de f-strings porque el cuerpo
#     está lleno de llaves de LaTeX y así no hay que escaparlas todas. --

PLANTILLA_DIBUJA = Template(
    r"""\actividadDibuja{%
$prompt
\espacioDibujo
}"""
)

PLANTILLA_COMPLETA = Template(
    r"""\actividadCompleta{%
\footnotesize\color{colorGris}\lblInstruccionCompleta
\par\vspace{3mm}\normalfont\normalsize\color{black}
\centering\resizebox{0.97\linewidth}{!}{\input{diagrams/$diagrama}}\par
\espacioDibujo[6cm]
}"""
)

PLANTILLA_COPIA = Template(
    r"""\actividadCopia{%
\lblInstruccionCopia
\lineaRespuesta
\lineaRespuesta
\lineaRespuesta
}"""
)

PLANTILLA_RESPONDE = Template(
    r"""\actividadResponde{%
$pregunta
\lineaRespuesta
\lineaRespuesta
\lineaRespuesta
}"""
)

PLANTILLA_RELACIONA = Template(
    r"""\actividadRelaciona{%
\footnotesize\color{colorGris}Une cada nombre con quién es, con una línea.
\par\vspace{3mm}\normalfont\normalsize\color{black}
\renewcommand{\arraystretch}{2.7}
\begin{tabularx}{\linewidth}{@{}X >{\centering\arraybackslash}p{3.4cm} X@{}}
$filas
\end{tabularx}
\renewcommand{\arraystretch}{1}
}"""
)

PLANTILLA_ADIVINA = Template(
    r"""\actividadAdivina{%
\Large\itshape $adivinanza
\normalfont
\lineaRespuesta
\lineaRespuesta
\vspace{5mm}
}"""
)

PLANTILLA_CREA = Template(
    r"""\actividadCrea{%
$prompt
\espacioDibujo
}"""
)

PLANTILLA_REPASA = Template(
    r"""\actividadRepasa{%
\begin{listaRepaso}
$items
\end{listaRepaso}
$prompt
\espacioDibujo[7cm]
\par\vspace{3mm}
\begin{center}\bfseries\Large\color{colorCrea} $banner\end{center}
}"""
)

PLANTILLA_DIA = Template(
    r"""\begin{diapagina}{$dia}{$semana}{$trimestre}
\begin{cajaLectura}
\centering\diafuente{$trimestre}%
$oraciones
\end{cajaLectura}
\vspace{5mm}
$actividad
\end{diapagina}
"""
)


def render_actividad(dia_num, actividad):
    tipo = actividad.get("tipo")
    if tipo not in TIPOS_VALIDOS:
        raise ErrorDeContenido(
            f"día {dia_num}: tipo de actividad desconocido: {tipo!r}"
        )

    if tipo == "dibuja":
        _campos_requeridos(dia_num, actividad, ["prompt"])
        return PLANTILLA_DIBUJA.substitute(prompt=escapar(actividad["prompt"]))

    if tipo == "completa":
        _campos_requeridos(dia_num, actividad, ["diagrama"])
        diagrama = actividad["diagrama"]
        ruta = ROOT / "diagrams" / f"{diagrama}.tex"
        if not ruta.exists():
            raise ErrorDeContenido(
                f"día {dia_num}: diagrams/{diagrama}.tex no existe"
            )
        return PLANTILLA_COMPLETA.substitute(diagrama=diagrama)

    if tipo == "copia":
        return PLANTILLA_COPIA.substitute()

    if tipo == "responde":
        _campos_requeridos(dia_num, actividad, ["pregunta"])
        return PLANTILLA_RESPONDE.substitute(pregunta=escapar(actividad["pregunta"]))

    if tipo == "relaciona":
        _campos_requeridos(dia_num, actividad, ["pares"])
        pares = actividad["pares"]
        if len(pares) < 2:
            raise ErrorDeContenido(
                f"día {dia_num}: relaciona necesita al menos 2 pares"
            )
        izquierda = [p[0] for p in pares]
        derecha = [p[1] for p in pares]
        rng = random.Random(dia_num)  # baraja reproducible, no aleatoria de verdad
        derecha_mezclada = derecha[:]
        while derecha_mezclada == derecha and len(derecha) > 1:
            rng.shuffle(derecha_mezclada)
        filas = " \\\\\n".join(
            f"{escapar(i)} & & {escapar(d)}"
            for i, d in zip(izquierda, derecha_mezclada)
        )
        filas += " \\\\"
        return PLANTILLA_RELACIONA.substitute(filas=filas)

    if tipo == "adivina":
        _campos_requeridos(dia_num, actividad, ["adivinanza"])
        return PLANTILLA_ADIVINA.substitute(
            adivinanza=escapar(actividad["adivinanza"])
        )

    if tipo == "crea":
        _campos_requeridos(dia_num, actividad, ["prompt"])
        return PLANTILLA_CREA.substitute(prompt=escapar(actividad["prompt"]))

    if tipo == "repasa":
        _campos_requeridos(dia_num, actividad, ["checklist", "prompt", "banner"])
        items = "\n".join(f"\\item {escapar(i)}" for i in actividad["checklist"])
        return PLANTILLA_REPASA.substitute(
            items=items,
            prompt=escapar(actividad["prompt"]),
            banner=escapar(actividad["banner"]),
        )

    raise AssertionError("tipo validado arriba, no debería llegar aquí")


def _campos_requeridos(dia_num, actividad, campos):
    faltan = [c for c in campos if c not in actividad]
    if faltan:
        raise ErrorDeContenido(
            f"día {dia_num}: la actividad {actividad.get('tipo')!r} "
            f"necesita {faltan}"
        )


def cargar_dias():
    """Lee todos los content/q*.json y devuelve la lista de días, en orden."""
    dias = []
    for fichero in sorted(CONTENT_DIR.glob("q*.json")):
        datos = json.loads(fichero.read_text(encoding="utf-8"))
        dias.extend(datos.get("dias", []))
    dias.sort(key=lambda d: d["dia"])
    return dias


def validar_dias(dias):
    """Comprueba las reglas del curso. Lanza ErrorDeContenido si algo falla."""
    if not dias:
        raise ErrorDeContenido("no hay ningún día en content/q*.json")

    esperado = 1
    for d in dias:
        num = d["dia"]
        if num != esperado:
            raise ErrorDeContenido(
                f"los días deben ser consecutivos empezando en 1: "
                f"se esperaba el día {esperado}, se encontró el día {num}"
            )
        esperado += 1

        if num < 1 or num > TOTAL_DIAS:
            raise ErrorDeContenido(f"día {num}: fuera de rango (1-{TOTAL_DIAS})")

        trimestre = d.get("trimestre")
        if trimestre not in RANGO_TRIMESTRE:
            raise ErrorDeContenido(f"día {num}: trimestre inválido: {trimestre!r}")

        lo, hi = RANGO_TRIMESTRE[trimestre]
        if not (lo <= num <= hi):
            raise ErrorDeContenido(
                f"día {num}: dice ser del trimestre {trimestre} "
                f"(días {lo}-{hi}) pero su número no está en ese rango"
            )

        tipo_actividad = d.get("actividad", {}).get("tipo")
        if tipo_actividad == "responde" and trimestre in TRIMESTRES_SIN_RESPONDE:
            raise ErrorDeContenido(
                f"día {num}: 'responde' no se usa en el trimestre {trimestre} "
                "-- la niña todavía no compone una respuesta escrita por sí "
                "sola a esta edad; usa 'copia' en su lugar"
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
                # una frase real termina en punto/exclamación -- si no,
                # probablemente es un fragmento a medio escribir.
                raise ErrorDeContenido(
                    f"día {num}: la frase «{frase}» no termina en un signo "
                    "de puntuación final"
                )


def generar_tex(dias):
    piezas = [
        "% content/generated-days.tex\n",
        "% GENERADO por tools/gen_days.py a partir de content/q*.json.\n",
        "% NO EDITAR A MANO -- los cambios se perderán en la siguiente\n",
        "% ejecución de `make generate`. Edita content/q*.json en su lugar.\n\n",
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
        validar_dias(dias)
        tex = generar_tex(dias)
    except ErrorDeContenido as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if check_only:
        actual = OUTPUT_FILE.read_text(encoding="utf-8") if OUTPUT_FILE.exists() else None
        if actual != tex:
            print(
                "DESACTUALIZADO: content/generated-days.tex no coincide con "
                "content/q*.json -- ejecuta `make generate`.",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {len(dias)} días validados, content/generated-days.tex al día.")
        return 0

    OUTPUT_FILE.write_text(tex, encoding="utf-8")
    print(f"Escrito {OUTPUT_FILE} con {len(dias)} días.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
