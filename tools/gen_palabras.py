#!/usr/bin/env python3
"""Genera el cuaderno de PRIMERAS PALABRAS (palabras.tex) a partir de
content/palabras/q*.json -- el nivel anterior al cuaderno de frases
(tools/gen_days.py, content/q*.json).

Mismo calendario que el de frases (260 días, 52 semanas, cuatro
trimestres = cuatro estaciones, medalla al final de T1-T3) y mismos
temas semanales -- dos hermanos pueden llevar cada uno su cuaderno y
leer esa semana sobre lo mismo --, pero lo que se lee es otra cosa:

  - T1 (otoño):     1 palabra al día, solo sílabas directas (ma, pe, lo);
  - T2 (invierno):  2 palabras al día, + sílabas cerradas (sol, pan),
                    c/g suaves (ce, gi) y h muda;
  - T3 (primavera): 3 palabras al día, + trabadas (pla, tre), dígrafos
                    (ch, ll, rr, qu, gu), diptongos (ue, ie);
  - T4 (verano):    una frase de 2 a 4 palabras -- el puente hacia el
                    cuaderno de frases, que empieza en 6-8 palabras.

Esa escalera NO es una disciplina editorial: está en ESCALERA, más
abajo, y este script falla si una palabra se la salta. Cada palabra se
escribe en el JSON ya partida en sílabas ("pe-lo-ta"), y ese silabeo
tiene que coincidir con el automático de tools/silabas.py.

Casi todas las actividades de este nivel terminan dibujando, y la caja
de actividad llena todo lo que queda de página (ver
preamble-palabras.tex): el sitio para dibujar es todo el que haya.

No editar content/palabras/generated-*.tex a mano -- se sobrescriben
cada vez que se ejecuta este script.

Uso:
    python3 tools/gen_palabras.py            # regenera content/palabras/generated-*.tex
    python3 tools/gen_palabras.py --check    # solo valida; exit 1 si algo no cuadra
                                             # o si lo generado está desactualizado
    python3 tools/gen_palabras.py --tabla    # resumen por semana, en Markdown (CI)
"""

import json
import random
import sys
from pathlib import Path
from string import Template

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_days import (  # noqa: E402
    ErrorDeContenido,
    NOMBRE_MEDALLA_TRIMESTRE,
    PLANTILLA_MEDALLA,
    RANGO_TRIMESTRE,
    TOTAL_DIAS,
    ULTIMO_DIA_TRIMESTRE,
    _campos_requeridos,
    datos_trazo,
    escapar,
    puntos_tikz_letra,
)
from silabas import rasgos, silabear  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "palabras"
OUTPUT_FILE = CONTENT_DIR / "generated-days.tex"
CLAVE_FILE = CONTENT_DIR / "generated-clave.tex"

TODOS_LOS_RASGOS = {
    "cerrada", "suave", "h", "trabada", "digrafo", "diptongo", "rara",
}

# La escalera del cuaderno, semana a semana. Dentro de un tramo:
#   palabras    -- cuántas palabras trae cada día (lunes a jueves);
#   max_silabas -- sílabas como mucho en una palabra;
#   rasgos      -- qué estructuras de sílaba se admiten, además de la
#                  directa (ver tools/silabas.py, rasgos()); los tramos
#                  son acumulativos -- lo de un trimestre sigue valiendo
#                  en el siguiente;
#   frase       -- (T4) palabras mínimas y máximas de la frase del día.
# Las semanas 1-5 se quedan en dos sílabas (ma-má, pa-to) y la tercera
# llega en la semana 6 (o-to-ño), cuando ya se juntan dos sílabas sin
# esfuerzo. T4 deja de tener restricción de sílabas: lo que sube ahí es
# cuántas palabras hay que leer seguidas.
ESCALERA = [
    {"semanas": (1, 5), "palabras": 1, "max_silabas": 2, "rasgos": set()},
    {"semanas": (6, 13), "palabras": 1, "max_silabas": 3, "rasgos": set()},
    {"semanas": (14, 26), "palabras": 2, "max_silabas": 3,
     "rasgos": {"cerrada", "suave", "h"}},
    {"semanas": (27, 39), "palabras": 3, "max_silabas": 4,
     "rasgos": TODOS_LOS_RASGOS},
    {"semanas": (40, 43), "frase": (2, 2)},
    {"semanas": (44, 47), "frase": (2, 3)},
    {"semanas": (48, 52), "frase": (3, 4)},
]

# Palabras que se leen "de un golpe", como el propio nombre, sin pasar
# por la escalera: los dos nombres de la historia que no se pueden
# escribir con sílabas directas (Lu-CÍ-a, To-BY). Sin esta excepción
# la protagonista y su perro no podrían aparecer hasta el trimestre 2 o
# 3. Solo nombres propios del reparto, nunca palabras comunes.
PALABRAS_GLOBALES = {"lucía", "toby"}

# Tipos de actividad de este cuaderno. Los que no llevan palabras
# propias ("relee", "repasa") son los viernes: la caja de lectura
# recoge las palabras de toda la semana.
TIPOS_VALIDOS = {
    "dibuja", "completa", "traza", "escribe", "encuentra", "palmadas",
    "adivina", "une", "si_no", "relee", "repasa",
}
TIPOS_VIERNES = {"relee", "repasa"}
TIPOS_SOLO_PALABRAS = {"palmadas"}  # necesitan sílabas: T1-T3
TIPOS_SOLO_FRASES = {"si_no"}       # necesitan frases: T4

INSTRUCCION_LECTURA = {
    1: r"\lblPalInstruccionUno",
    2: r"\lblPalInstruccionDos",
    3: r"\lblPalInstruccionTres",
    4: r"\lblPalInstruccionCuatro",
}

# Rejilla del viernes: columnas según el trimestre (T1: 4 palabras en
# 2x2; T2: 8 en 3 columnas; T3: 12 en 3 columnas; T4: 4 frases, una
# por línea).
COLUMNAS_SEMANA = {1: 2, 2: 3, 3: 3, 4: 1}


def tramo(semana):
    for t in ESCALERA:
        lo, hi = t["semanas"]
        if lo <= semana <= hi:
            return t
    raise ErrorDeContenido(f"la semana {semana} no está en ESCALERA")


def inicial(palabra):
    """Primera letra, en minúscula y sin tilde -- pero la ñ sigue siendo
    ñ (no se puede quitar la "tilde" de la ñ: es otra letra)."""
    return palabra[:1].lower().translate(str.maketrans("áéíóúü", "aeiouu"))


def limpiar(token):
    """Una palabra de una frase, sin la puntuación de alrededor."""
    return token.strip(".,;:!¡?¿\"«»—-")


# --------------------------------------------------------------------
# Validación de palabras contra la escalera
# --------------------------------------------------------------------

def comprobar_escalera(num, palabra, semana, donde):
    """Una palabra suelta que lee la niña o el niño (en la caja de
    lectura o dentro de una actividad) tiene que respetar la escalera de
    su semana. En T4 (frases) no hay restricción de sílabas."""
    t = tramo(semana)
    if "frase" in t or palabra.lower() in PALABRAS_GLOBALES:
        return
    silabas = silabear(palabra)
    if len(silabas) > t["max_silabas"]:
        raise ErrorDeContenido(
            f"día {num} ({donde}): «{palabra}» tiene {len(silabas)} sílabas "
            f"({'-'.join(silabas)}); en la semana {semana} el máximo es "
            f"{t['max_silabas']}"
        )
    for s in silabas:
        sobra = rasgos(s) - t["rasgos"]
        if sobra:
            raise ErrorDeContenido(
                f"día {num} ({donde}): «{palabra}» tiene la sílaba «{s}» "
                f"({', '.join(sorted(sobra))}), que la escalera no admite "
                f"hasta más adelante (semana {semana})"
            )


def leer_palabra(num, escrita, semana):
    """'pe-lo-ta' -> ('pelota', ['pe', 'lo', 'ta']), comprobando que el
    silabeo escrito a mano coincide con el automático y que la palabra
    cabe en la escalera de su semana."""
    if not escrita or escrita != escrita.strip() or " " in escrita:
        raise ErrorDeContenido(f"día {num}: palabra mal escrita: {escrita!r}")
    silabas = escrita.split("-")
    palabra = "".join(silabas)
    automatico = silabear(palabra)
    if silabas != automatico:
        raise ErrorDeContenido(
            f"día {num}: «{escrita}» -- el silabeo automático da "
            f"«{'-'.join(automatico)}». Si el de a mano es el correcto, "
            "añade la palabra a EXCEPCIONES en tools/silabas.py, con su porqué"
        )
    comprobar_escalera(num, palabra, semana, "palabra del día")
    return palabra, silabas


def validar_frase(num, frase, semana, donde, minimo=None):
    """Una frase de T4: entre `frase` palabras de su tramo (o desde
    `minimo`, para las frases cortas de una actividad), con mayúscula
    inicial y punto final."""
    t = tramo(semana)
    lo, hi = t["frase"]
    if minimo is not None:
        lo = minimo
    n = len(frase.split())
    if not (lo <= n <= hi):
        raise ErrorDeContenido(
            f"día {num} ({donde}): «{frase}» tiene {n} palabras; en la "
            f"semana {semana} tienen que ser entre {lo} y {hi}"
        )
    if not frase.strip().endswith((".", "!", "?")):
        raise ErrorDeContenido(
            f"día {num} ({donde}): «{frase}» no termina en un signo de "
            "puntuación final"
        )
    primera = frase.lstrip("¡¿—")
    if not primera[:1].isupper():
        raise ErrorDeContenido(
            f"día {num} ({donde}): «{frase}» no empieza por mayúscula"
        )


# --------------------------------------------------------------------
# Plantillas (string.Template: el cuerpo está lleno de llaves de LaTeX)
# --------------------------------------------------------------------

PLANTILLA_DIA = Template(
    r"""\begin{palabrapagina}{$dia}{$semana}{$trimestre}{$tema}
\begin{cajaLectura}{$instruccion}
$lectura
\end{cajaLectura}
\vspace{5mm}
$actividad
\end{palabrapagina}
"""
)

PLANTILLA_DIBUJA = Template(
    r"""\begin{cajaPalDibuja}
{\Large $prompt\par}
\end{cajaPalDibuja}"""
)

PLANTILLA_COMPLETA = Template(
    r"""\begin{cajaPalCompleta}[centrado abajo]
$enunciado
\tcblower
\begin{center}\resizebox{0.8\linewidth}{!}{\input{diagrams/$diagrama}}\end{center}
\end{cajaPalCompleta}"""
)

PLANTILLA_TRAZA = Template(
    r"""\begin{cajaPalTraza}
\begin{center}
{\Large\color{colorGris} $mayus~\lblTrazoDe~$palabra}

\vspace{4mm}
\begin{tikzpicture}
\fill[colorResponde] $puntos;
\end{tikzpicture}

\vspace{4mm}
{\footnotesize\color{colorGris}\lblInstruccionTrazo}\\[9mm]
\rule{0.6\linewidth}{0.5pt}
\end{center}
$dibujo
\end{cajaPalTraza}"""
)

PLANTILLA_ESCRIBE = Template(
    r"""\begin{cajaPalEscribe}
\instruccion{\lblPalInstruccionEscribe}
\begin{center}
\palabraHueca{$palabra}
\palabraHueca{$palabra}
\end{center}
\lineaEscribir
$dibujo
\end{cajaPalEscribe}"""
)

PLANTILLA_ENCUENTRA = Template(
    r"""\begin{cajaPalEncuentra}
\instruccion{\lblPalInstruccionEncuentra}
\begin{center}
\fcolorbox{colorCompleta}{white}{\fontsize{30}{36}\selectfont\ $modelo\ }
\end{center}
\vspace{2mm}
{\fontsize{26}{32}\selectfont
\renewcommand{\arraystretch}{1.9}
\begin{tabularx}{\linewidth}{@{}*{$columnas}{>{\centering\arraybackslash}X}@{}}
$filas
\end{tabularx}\par}
$dibujo
\end{cajaPalEncuentra}"""
)

PLANTILLA_PALMADAS = Template(
    r"""\begin{cajaPalPalmadas}
\instruccion{\lblPalInstruccionPalmadas}
\begin{tabularx}{\linewidth}{@{}>{\fontsize{30}{36}\selectfont}X r@{}}
$filas
\end{tabularx}
$dibujo
\end{cajaPalPalmadas}"""
)

PLANTILLA_ADIVINA = Template(
    r"""\begin{cajaPalAdivina}$opciones
\instruccion{$instruccion}
{\Large $adivinanza\par}
$linea
\end{cajaPalAdivina}"""
)

PLANTILLA_UNE = Template(
    r"""\begin{cajaPalUne}
\instruccion{$instruccion}
{\fontsize{$tam}{$salto}\selectfont
\renewcommand{\arraystretch}{1.9}
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X >{\centering\arraybackslash}p{2.2cm} >{\raggedleft\arraybackslash}X@{}}
$filas
\end{tabularx}\par}
$dibujo
\end{cajaPalUne}"""
)

PLANTILLA_SI_NO = Template(
    r"""\begin{cajaPalSiNo}
\instruccion{\lblPalInstruccionSiNo}
{\fontsize{24}{30}\selectfont
\renewcommand{\arraystretch}{1.8}
\begin{tabularx}{\linewidth}{@{}X r@{}}
$filas
\end{tabularx}\par}
$dibujo
\end{cajaPalSiNo}"""
)

PLANTILLA_RELEE = Template(
    r"""\begin{cajaPalRelee}
{\Large $prompt\par}
\end{cajaPalRelee}"""
)

PLANTILLA_REPASA = Template(
    r"""\begin{cajaPalRepasa}[abajo]
{\Large $prompt\par}
\tcblower
\begin{center}\bfseries\Large\color{colorCrea} $banner\end{center}
\end{cajaPalRepasa}"""
)


def remate_dibujo(actividad):
    """El "Ahora, dibuja: ..." opcional con que terminan las actividades
    que no son de dibujo en sí mismas -- en este nivel, casi todas."""
    prompt = actividad.get("prompt")
    if not prompt:
        return ""
    return r"\ahoraDibuja{" + escapar(prompt) + "}"


# --------------------------------------------------------------------
# La caja de lectura
# --------------------------------------------------------------------

def lectura_palabras(trimestre, palabras):
    """Tarjetas de palabra: sílabas arriba, palabra entera debajo."""
    tarjetas = [
        r"\tarjeta{%d}{%s}{%s}" % (
            trimestre,
            r"\sep ".join(escapar(s) for s in silabas),
            escapar(palabra),
        )
        for palabra, silabas in palabras
    ]
    if len(tarjetas) == 1:
        return r"\centering" + "\n" + tarjetas[0]
    columnas = len(tarjetas)
    return (
        r"\begin{tabularx}{\linewidth}{@{}*{%d}{>{\centering\arraybackslash}X}@{}}" % columnas
        + "\n" + "\n&\n".join(tarjetas) + "\n"
        + r"\end{tabularx}"
    )


def lectura_frase(frase):
    return r"\fraseDia{" + escapar(frase) + "}"


def lectura_semana(trimestre, elementos):
    """El viernes: todo lo leído de lunes a jueves, cada cosa con su
    casilla."""
    columnas = COLUMNAS_SEMANA[trimestre]
    celdas = [r"\palabraSemana{" + escapar(e) + "}" for e in elementos]
    filas = []
    for i in range(0, len(celdas), columnas):
        fila = celdas[i:i + columnas]
        fila += [""] * (columnas - len(fila))
        filas.append(" & ".join(fila))
    cuerpo = " \\\\[3mm]\n".join(filas)
    return (
        r"{\footnotesize\color{colorGris}\lblPalMarcaSemana\par}\vspace{3mm}" + "\n"
        + r"{\fuenteSemana{%d}" % trimestre + "\n"
        + r"\begin{tabularx}{\linewidth}{@{}*{%d}{>{\raggedright\arraybackslash}X}@{}}" % columnas
        + "\n" + cuerpo + "\n"
        + r"\end{tabularx}\par}"
    )


# --------------------------------------------------------------------
# Actividades
# --------------------------------------------------------------------

def render_actividad(dia, semana_previa):
    num = dia["dia"]
    trimestre = dia["trimestre"]
    semana = dia["semana"]
    actividad = dia["actividad"]
    tipo = actividad.get("tipo")
    # Las palabras sueltas que ha leído la niña o el niño ese día: las
    # de las tarjetas (T1-T3) o las de la frase (T4) -- ver preparar_dia.
    leidas = dia["palabras_leidas"]
    clave = None

    if tipo not in TIPOS_VALIDOS:
        raise ErrorDeContenido(f"día {num}: tipo de actividad desconocido: {tipo!r}")
    if tipo in TIPOS_SOLO_PALABRAS and trimestre == 4:
        raise ErrorDeContenido(
            f"día {num}: '{tipo}' necesita palabras con sus sílabas -- "
            "no se usa en el trimestre 4 (frases)"
        )
    if tipo in TIPOS_SOLO_FRASES and trimestre != 4:
        raise ErrorDeContenido(
            f"día {num}: '{tipo}' necesita frases -- solo se usa en el trimestre 4"
        )

    if tipo == "dibuja":
        _campos_requeridos(num, actividad, ["prompt"])
        tex = PLANTILLA_DIBUJA.substitute(prompt=escapar(actividad["prompt"]))

    elif tipo == "completa":
        _campos_requeridos(num, actividad, ["diagrama"])
        diagrama = actividad["diagrama"]
        if not (ROOT / "diagrams" / f"{diagrama}.tex").exists():
            raise ErrorDeContenido(f"día {num}: diagrams/{diagrama}.tex no existe")
        if actividad.get("prompt"):
            enunciado = r"{\Large " + escapar(actividad["prompt"]) + r"\par}"
        else:
            enunciado = r"\instruccion{\lblPalInstruccionCompleta}"
        tex = PLANTILLA_COMPLETA.substitute(enunciado=enunciado, diagrama=diagrama)

    elif tipo == "traza":
        _campos_requeridos(num, actividad, ["letra"])
        letra = actividad["letra"]
        letras, _ = datos_trazo()
        if letra not in letras:
            raise ErrorDeContenido(
                f"día {num}: 'traza' pide la letra {letra!r}, que no está "
                "en content/letras-trazo.json"
            )
        # La palabra de ejemplo ("M de mamá") es una de las que se han
        # leído ese día, no una lista aparte: así la letra que se traza
        # es la de algo que se acaba de leer.
        ejemplo = next((p for p in leidas if inicial(p) == letra), None)
        if ejemplo is None:
            raise ErrorDeContenido(
                f"día {num}: 'traza' pide la letra {letra!r}, pero ninguna "
                f"palabra de ese día empieza por ella ({', '.join(leidas)})"
            )
        entrada = letras[letra]
        tex = PLANTILLA_TRAZA.substitute(
            mayus=escapar(letra.upper()),
            palabra=escapar(ejemplo),
            puntos=puntos_tikz_letra(entrada["mayuscula"], entrada["minuscula"]),
            dibujo=remate_dibujo(actividad),
        )

    elif tipo == "escribe":
        palabra = actividad.get("palabra")
        if palabra is None:
            if trimestre == 4:
                raise ErrorDeContenido(
                    f"día {num}: 'escribe' en el trimestre 4 necesita "
                    "'palabra' (una de las de la frase)"
                )
            palabra = leidas[0]
        if palabra.lower() not in (p.lower() for p in leidas):
            raise ErrorDeContenido(
                f"día {num}: 'escribe' pide «{palabra}», que no es ninguna "
                f"de las palabras leídas ese día ({', '.join(leidas)})"
            )
        tex = PLANTILLA_ESCRIBE.substitute(
            palabra=escapar(palabra), dibujo=remate_dibujo(actividad)
        )

    elif tipo == "encuentra":
        _campos_requeridos(num, actividad, ["distractores"])
        modelo = actividad.get("palabra")
        if modelo is None:
            if trimestre == 4:
                raise ErrorDeContenido(
                    f"día {num}: 'encuentra' en el trimestre 4 necesita 'palabra'"
                )
            modelo = leidas[0]
        if modelo.lower() not in (p.lower() for p in leidas):
            raise ErrorDeContenido(
                f"día {num}: 'encuentra' busca «{modelo}», que no es ninguna "
                f"de las palabras leídas ese día ({', '.join(leidas)})"
            )
        distractores = actividad["distractores"]
        # Cuántas veces aparece la palabra buscada: 2, 3 o 4 según el
        # día si el JSON no lo fija -- si fueran siempre 3, se acabaría
        # contando en vez de leyendo.
        veces = actividad.get("veces", 2 + num % 3)
        if len(distractores) < 3 or not (2 <= veces <= 4):
            raise ErrorDeContenido(
                f"día {num}: 'encuentra' necesita al menos 3 distractores "
                "y 'veces' entre 2 y 4"
            )
        for d in distractores:
            if d == modelo:
                raise ErrorDeContenido(
                    f"día {num}: 'encuentra' tiene «{d}» como distractor y "
                    "como palabra buscada a la vez"
                )
            comprobar_escalera(num, d, semana, "encuentra")
        todas = distractores + [modelo] * veces
        rng = random.Random(num)  # reproducible, no aleatorio de verdad
        rng.shuffle(todas)
        columnas = 4 if max(len(p) for p in todas) <= 6 else 3
        filas = []
        for i in range(0, len(todas), columnas):
            fila = [escapar(p) for p in todas[i:i + columnas]]
            fila += [""] * (columnas - len(fila))
            filas.append(" & ".join(fila))
        tex = PLANTILLA_ENCUENTRA.substitute(
            modelo=escapar(modelo),
            columnas=columnas,
            filas=" \\\\\n".join(filas) + " \\\\",
            dibujo=remate_dibujo(actividad),
        )
        clave = ("encuentra", f"«{modelo}»: {veces} veces")

    elif tipo == "palmadas":
        circulos = tramo(semana)["max_silabas"] + 1
        filas = " \\\\[7mm]\n".join(
            escapar(p) + " & " + r"\hspace{2mm}".join([r"\circuloPalmada"] * circulos)
            for p in leidas
        ) + " \\\\"
        tex = PLANTILLA_PALMADAS.substitute(filas=filas, dibujo=remate_dibujo(actividad))

    elif tipo == "adivina":
        # La respuesta no sale en la página -- solo en la clave de
        # respuestas, para el adulto (backmatter/palabras/clave-respuestas.tex).
        _campos_requeridos(num, actividad, ["adivinanza", "respuesta"])
        escribe = trimestre >= 2
        tex = PLANTILLA_ADIVINA.substitute(
            instruccion=(r"\lblPalInstruccionAdivinaEscribe" if escribe
                         else r"\lblPalInstruccionAdivina"),
            adivinanza=escapar(actividad["adivinanza"]),
            opciones=("[abajo]" if escribe else ""),
            linea=(r"\tcblower" + "\n" + r"\noindent\rule{0.55\linewidth}{0.5pt}" if escribe else ""),
        )
        clave = ("adivina", actividad["respuesta"])

    elif tipo == "une":
        pares = actividad.get("pares")
        if pares is None:
            if trimestre == 4:
                raise ErrorDeContenido(
                    f"día {num}: 'une' en el trimestre 4 necesita 'pares' e 'instruccion'"
                )
            # Por defecto: minúsculas con MAYÚSCULAS, con las palabras más
            # recientes de la semana -- solo lo que ya se ha leído.
            recientes = []
            for p in reversed(semana_previa + leidas):
                if p not in recientes:
                    recientes.append(p)
            elegidas = list(reversed(recientes[:4]))
            pares = [[p, p.upper()] for p in elegidas]
            instruccion = r"\lblPalInstruccionUne"
            automatico = True
        else:
            _campos_requeridos(num, actividad, ["instruccion"])
            instruccion = escapar(actividad["instruccion"])
            automatico = False
            for izq, der in pares:
                for lado in (izq, der):
                    for token in lado.split():
                        comprobar_escalera(num, limpiar(token), semana, "une")
        if len(pares) < 3:
            raise ErrorDeContenido(f"día {num}: 'une' necesita al menos 3 pares")
        izquierda = [p[0] for p in pares]
        derecha = [p[1] for p in pares]
        # Ninguna palabra de la derecha se queda enfrente de su pareja:
        # con que una sola coincida, ya hay una línea que no hay que
        # pensar. Reproducible (semilla = número de día), no aleatorio.
        rng = random.Random(num)
        mezclada = derecha[:]
        while any(a == b for a, b in zip(mezclada, derecha)):
            rng.shuffle(mezclada)
        filas = " \\\\\n".join(
            f"{escapar(i)}\\ \\textbullet & & \\textbullet\\ {escapar(d)}"
            for i, d in zip(izquierda, mezclada)
        ) + " \\\\"
        largo = max(len(x) for x in izquierda + derecha)
        tam = 26 if largo <= 9 else 20
        tex = PLANTILLA_UNE.substitute(
            instruccion=instruccion, filas=filas, tam=tam, salto=tam + 6,
            dibujo=remate_dibujo(actividad),
        )
        # "mamá -> MAMÁ" no necesita clave; los pares escritos a mano
        # (animal y sonido, contrarios, rimas) sí.
        if not automatico:
            clave = ("une", " \\quad ".join(
                f"{escapar(i)} $\\rightarrow$ {escapar(d)}" for i, d in pares
            ))

    elif tipo == "si_no":
        _campos_requeridos(num, actividad, ["afirmaciones"])
        afirmaciones = actividad["afirmaciones"]
        if not (2 <= len(afirmaciones) <= 4):
            raise ErrorDeContenido(f"día {num}: 'si_no' necesita entre 2 y 4 frases")
        for texto, verdad in afirmaciones:
            if not isinstance(verdad, bool):
                raise ErrorDeContenido(
                    f"día {num}: en 'si_no', «{texto}» necesita true o false"
                )
            validar_frase(num, texto, semana, "si_no", minimo=2)
        filas = " \\\\\n".join(
            escapar(t) + r" & \lblSi\hspace{8mm}\lblNo" for t, _ in afirmaciones
        ) + " \\\\"
        tex = PLANTILLA_SI_NO.substitute(filas=filas, dibujo=remate_dibujo(actividad))
        respuestas = {True: r"\lblSi", False: r"\lblNo"}
        clave = ("si_no", ", ".join(
            f"{escapar(t)} {respuestas[v]}" for t, v in afirmaciones
        ))

    elif tipo == "relee":
        _campos_requeridos(num, actividad, ["prompt"])
        tex = PLANTILLA_RELEE.substitute(prompt=escapar(actividad["prompt"]))

    elif tipo == "repasa":
        _campos_requeridos(num, actividad, ["prompt", "banner"])
        tex = PLANTILLA_REPASA.substitute(
            prompt=escapar(actividad["prompt"]), banner=escapar(actividad["banner"])
        )

    else:
        raise AssertionError("tipo validado arriba")

    return tex, clave


# --------------------------------------------------------------------
# Carga y validación del libro
# --------------------------------------------------------------------

def cargar_dias():
    dias = []
    for fichero in sorted(CONTENT_DIR.glob("q*.json")):
        datos = json.loads(fichero.read_text(encoding="utf-8"))
        dias.extend(datos.get("dias", []))
    dias.sort(key=lambda d: d["dia"])
    return dias


def preparar_dia(d):
    """Valida un día y le añade `palabras_leidas` (las palabras sueltas
    que se leen ese día) y, en T1-T3, `tarjetas` [(palabra, sílabas)]."""
    num = d["dia"]
    if not (1 <= num <= TOTAL_DIAS):
        raise ErrorDeContenido(f"día {num}: fuera de rango (1-{TOTAL_DIAS})")
    trimestre = d.get("trimestre")
    if trimestre not in RANGO_TRIMESTRE:
        raise ErrorDeContenido(f"día {num}: trimestre inválido: {trimestre!r}")
    lo, hi = RANGO_TRIMESTRE[trimestre]
    if not (lo <= num <= hi):
        raise ErrorDeContenido(
            f"día {num}: dice ser del trimestre {trimestre} (días {lo}-{hi})"
        )
    semana = d.get("semana")
    if semana != (num - 1) // 5 + 1:
        raise ErrorDeContenido(
            f"día {num}: dice ser de la semana {semana}, pero le toca la "
            f"{(num - 1) // 5 + 1} (5 días por semana)"
        )
    if not d.get("tema"):
        raise ErrorDeContenido(f"día {num}: falta el 'tema' de la semana")

    tipo = d.get("actividad", {}).get("tipo")
    es_viernes = num % 5 == 0
    if es_viernes != (tipo in TIPOS_VIERNES):
        raise ErrorDeContenido(
            f"día {num}: los viernes (y solo los viernes) son 'relee' o "
            f"'repasa' -- este día es {'viernes' if es_viernes else 'de lunes a jueves'} "
            f"y su actividad es {tipo!r}"
        )

    t = tramo(semana)
    if es_viernes:
        if "palabras" in d or "frase" in d:
            raise ErrorDeContenido(
                f"día {num}: un viernes no lleva palabras propias -- la caja "
                "de lectura recoge las de lunes a jueves"
            )
        d["palabras_leidas"] = []
        return d

    if "frase" in t:
        if "palabras" in d or "frase" not in d:
            raise ErrorDeContenido(
                f"día {num}: en el trimestre 4 cada día lleva una 'frase', no 'palabras'"
            )
        validar_frase(num, d["frase"], semana, "frase del día")
        d["palabras_leidas"] = [limpiar(p) for p in d["frase"].split()]
        return d

    escritas = d.get("palabras", [])
    if "frase" in d or len(escritas) != t["palabras"]:
        raise ErrorDeContenido(
            f"día {num} (semana {semana}): debería tener {t['palabras']} "
            f"palabra(s) en 'palabras', tiene {len(escritas)}"
        )
    d["tarjetas"] = [leer_palabra(num, e, semana) for e in escritas]
    d["palabras_leidas"] = [p for p, _ in d["tarjetas"]]
    if len(set(d["palabras_leidas"])) != len(d["palabras_leidas"]):
        raise ErrorDeContenido(f"día {num}: una palabra repetida el mismo día")
    return d


def validar_dias(dias):
    if not dias:
        raise ErrorDeContenido("no hay ningún día en content/palabras/q*.json")
    for esperado, d in enumerate(dias, start=1):
        if d["dia"] != esperado:
            raise ErrorDeContenido(
                f"los días deben ser consecutivos empezando en 1: se esperaba "
                f"el día {esperado}, se encontró el día {d['dia']}"
            )
        preparar_dia(d)


def semana_hasta(dias, d):
    """Lo leído en la misma semana antes de este día, en orden: las
    palabras (T1-T3, sin repetir) o las frases (T4)."""
    anteriores = [
        x for x in dias
        if x["semana"] == d["semana"] and x["dia"] < d["dia"]
    ]
    if d["trimestre"] == 4:
        return [x["frase"] for x in anteriores if "frase" in x]
    vistas = []
    for x in anteriores:
        for p in x["palabras_leidas"]:
            if p not in vistas:
                vistas.append(p)
    return vistas


CABECERA = (
    "% {nombre}\n"
    "% GENERADO por tools/gen_palabras.py a partir de content/palabras/q*.json.\n"
    "% NO EDITAR A MANO -- los cambios se perderán en la siguiente\n"
    "% ejecución de `make generate`. Edita content/palabras/q*.json en su lugar.\n\n"
)


def generar(dias):
    piezas = [CABECERA.format(nombre="content/palabras/generated-days.tex")]
    claves = [CABECERA.format(nombre="content/palabras/generated-clave.tex")]
    for d in dias:
        num, trimestre = d["dia"], d["trimestre"]
        tipo = d["actividad"]["tipo"]
        previas = semana_hasta(dias, d)
        if tipo in TIPOS_VIERNES:
            if not previas:
                raise ErrorDeContenido(
                    f"día {num}: '{tipo}' no encuentra nada leído esa semana"
                )
            lectura = lectura_semana(trimestre, previas)
            instruccion = (r"\lblPalInstruccionSemanaFrases" if trimestre == 4
                           else r"\lblPalInstruccionSemana")
        elif trimestre == 4:
            lectura = lectura_frase(d["frase"])
            instruccion = INSTRUCCION_LECTURA[4]
        else:
            lectura = lectura_palabras(trimestre, d["tarjetas"])
            instruccion = INSTRUCCION_LECTURA[trimestre]

        # Para "une" por defecto hacen falta las palabras previas de la
        # semana, no las frases.
        previas_palabras = previas if trimestre != 4 else []
        actividad_tex, clave = render_actividad(d, previas_palabras)
        piezas.append(PLANTILLA_DIA.substitute(
            dia=num,
            semana=d["semana"],
            trimestre=trimestre,
            tema=escapar(d["tema"]),
            instruccion=instruccion,
            lectura=lectura,
            actividad=actividad_tex,
        ))
        if clave:
            etiqueta = {
                "adivina": r"\lblAdivina", "une": r"\lblUne",
                "encuentra": r"\lblEncuentra", "si_no": r"\lblSiNo",
            }[clave[0]]
            texto = clave[1] if clave[0] in ("une", "si_no") else escapar(clave[1])
            claves.append(f"\\claveEntrada{{{num}}}{{{etiqueta}}}{{{texto}}}\n")

        if num == ULTIMO_DIA_TRIMESTRE.get(trimestre) and trimestre in NOMBRE_MEDALLA_TRIMESTRE:
            banner = d["actividad"].get("banner")
            if not banner:
                raise ErrorDeContenido(
                    f"día {num}: cierra el trimestre {trimestre} y necesita "
                    "un 'banner' (actividad 'repasa') para la medalla"
                )
            piezas.append(PLANTILLA_MEDALLA.substitute(
                dia=num,
                titulo=f"¡Medalla de {NOMBRE_MEDALLA_TRIMESTRE[trimestre]}!",
                banner=escapar(banner),
            ))
    return "\n".join(piezas), "".join(claves)


def comprobar_trazo(dias):
    """Las 27 letras del abecedario se trazan al menos una vez en el año
    -- igual que en el cuaderno de frases, pero aquí cada letra es la
    inicial de una palabra que se acaba de leer."""
    letras, _ = datos_trazo()
    trazadas = {d["actividad"]["letra"] for d in dias if d["actividad"]["tipo"] == "traza"}
    faltan = sorted(set(letras) - trazadas)
    if faltan and len(dias) == TOTAL_DIAS:
        raise ErrorDeContenido(
            f"ninguna actividad 'traza' practica estas letras: {', '.join(faltan)}"
        )


def tabla(dias):
    """Resumen por semana, en Markdown, para GITHUB_STEP_SUMMARY."""
    lineas = [
        "| Semana | Trim. | Tema | Lee | Sílabas (máx.) | Estructuras nuevas |",
        "|---|---|---|---|---|---|",
    ]
    vistos = set()
    por_semana = {}
    for d in dias:
        por_semana.setdefault(d["semana"], []).append(d)
    for semana, grupo in sorted(por_semana.items()):
        t = tramo(semana)
        if "frase" in t:
            n = [len(d["frase"].split()) for d in grupo if "frase" in d]
            rango = str(min(n)) if min(n) == max(n) else f"{min(n)}–{max(n)}"
            lee = f"frase de {rango} palabras"
            silabas = "–"
            nuevos = ""
        else:
            lee = f"{t['palabras']} {'palabra' if t['palabras'] == 1 else 'palabras'}/día"
            maxima = 0
            nuevos_semana = set()
            for d in grupo:
                for palabra, sil in d.get("tarjetas", []):
                    if palabra.lower() in PALABRAS_GLOBALES:
                        continue
                    maxima = max(maxima, len(sil))
                    for s in sil:
                        nuevos_semana |= rasgos(s)
            nuevos = ", ".join(sorted(nuevos_semana - vistos))
            vistos |= nuevos_semana
            silabas = f"{maxima} (obj. {t['max_silabas']})"
        lineas.append(
            f"| {semana} | {grupo[0]['trimestre']} | {grupo[0]['tema']} | "
            f"{lee} | {silabas} | {nuevos} |"
        )
    return "\n".join(lineas)


def main():
    check_only = "--check" in sys.argv
    modo_tabla = "--tabla" in sys.argv

    try:
        dias = cargar_dias()
        validar_dias(dias)
        comprobar_trazo(dias)
        tex, clave = generar(dias)
    except ErrorDeContenido as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if modo_tabla:
        print(tabla(dias))
        return 0

    salidas = [(OUTPUT_FILE, tex), (CLAVE_FILE, clave)]
    if check_only:
        for ruta, contenido in salidas:
            actual = ruta.read_text(encoding="utf-8") if ruta.exists() else None
            if actual != contenido:
                print(
                    f"DESACTUALIZADO: {ruta} no coincide con "
                    "content/palabras/q*.json -- ejecuta `make generate`.",
                    file=sys.stderr,
                )
                return 1
        print(f"OK: {len(dias)} días validados, {OUTPUT_FILE.name} y {CLAVE_FILE.name} al día.")
        return 0

    for ruta, contenido in salidas:
        ruta.write_text(contenido, encoding="utf-8")
    print(f"Escrito {OUTPUT_FILE} con {len(dias)} días, y {CLAVE_FILE}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
