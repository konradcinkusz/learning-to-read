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

El mismo generador hace también «First Words», el cuaderno de primeras
palabras en inglés (`--libro firstwords`, content/firstwords/q*.json,
ver notes/06-first-words.md): mismo calendario, mismo ciclo semanal y
mismas actividades, pero la escalera es de sonidos, no de sílabas -- en
inglés se lee juntando sonidos (c, a, t: cat), así que cada palabra se
escribe partida en grafemas ("sh-ee-p") y ese partido tiene que
coincidir con el automático de tools/fonetica.py. Todo lo que cambia de
un cuaderno a otro está en su Perfil, más abajo.

Y en «First Words» no se dibuja: se colorea. Cada día lleva un
`dibujo` (diagrams/firstwords/), el de una palabra que se lee ese día
-- si se lee van, se colorea una furgoneta --, y el script lo
comprueba: que el dibujo existe y que su palabra es de las leídas. El
lunes el dibujo llena la caja ("colorea"); los demás días va debajo de
la actividad, en el sitio que quede ("Now colour: ..."); la adivinanza
se contesta coloreando uno de tres dibujos, y "une" junta cada palabra
con su dibujo. Los viernes, una escena de la semana.

No editar content/palabras/generated-*.tex (ni content/firstwords/) a
mano -- se sobrescriben cada vez que se ejecuta este script.

Uso:
    python3 tools/gen_palabras.py            # regenera content/palabras/generated-*.tex
    python3 tools/gen_palabras.py --check    # solo valida; exit 1 si algo no cuadra
                                             # o si lo generado está desactualizado
    python3 tools/gen_palabras.py --tabla    # resumen por semana, en Markdown (CI)
    python3 tools/gen_palabras.py --libro firstwords [--check | --tabla]
                                             # lo mismo, para «First Words»
"""

import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from string import Template

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fonetica  # noqa: E402
from libros import ENGLISH, FRASES  # noqa: E402
from ediciones import (  # noqa: E402
    comprobar_campos, comprobar_preamble, ediciones_completas, ruta_edicion,
    salidas_ediciones,
)
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

# La escalera de «First Words», el cuaderno en inglés: lo que sube no es
# el número de sílabas sino qué sonidos se pueden leer (los grafemas de
# tools/fonetica.py, acumulativos), cuántos tiene una palabra como mucho
# (max_sonidos) y si puede llevar dos consonantes seguidas (grupos: frog,
# nest). Mismos tramos que la española -- una palabra al día en otoño,
# dos en invierno, tres en primavera y una frase en verano --, para que
# los dos cuadernos se lleven igual.
ESCALERA_EN = [
    {"semanas": (1, 5), "palabras": 1, "max_sonidos": 3, "grupos": False,
     "grafemas": fonetica.GRAFEMAS_T1A},
    {"semanas": (6, 13), "palabras": 1, "max_sonidos": 3, "grupos": False,
     "grafemas": fonetica.GRAFEMAS_T1A | fonetica.GRAFEMAS_T1B},
    {"semanas": (14, 26), "palabras": 2, "max_sonidos": 4, "grupos": False,
     "grafemas": fonetica.GRAFEMAS_T1A | fonetica.GRAFEMAS_T1B | fonetica.GRAFEMAS_T2},
    {"semanas": (27, 39), "palabras": 3, "max_sonidos": 5, "grupos": True,
     "grafemas": fonetica.TODOS},
    {"semanas": (40, 43), "frase": (2, 2)},
    {"semanas": (44, 47), "frase": (2, 3)},
    {"semanas": (48, 52), "frase": (3, 4)},
]

# En inglés, los nombres del reparto que no se pueden leer sonido a
# sonido con lo que se sabe (Lu-cí-a, To-by, A-my, Da-ni...) se leen de
# un golpe, como el propio nombre. Pip, Sam, Mum y Dad no están: se leen
# juntando sus sonidos desde el primer día.
PALABRAS_GLOBALES_EN = frozenset({
    "lucía", "toby", "amy", "dani", "rosa", "grandma", "marta", "luna",
    "pedro", "brown", "browns", "mr", "mrs", "andrés", "bigotes", "martín",
    "tomás", "julián", "lola", "paco",
})


@dataclass(frozen=True)
class Perfil:
    """Lo que distingue a los dos cuadernos de este generador."""
    nombre: str
    idioma: str
    dir_contenido: Path
    escalera: list
    globales: frozenset
    titulo_medalla: str
    nombres_medalla: dict
    animo_medalla: str
    # Mientras un cuaderno se escribe por partes (un PR por trimestre),
    # cuántos días tiene ya escritos: se exigen exactamente esos, del 1
    # en adelante. None = el cuaderno está entero, con sus 260 días.
    dias_escritos: int = None
    # Cuántos días, del 1 en adelante, llevan su dibujo para colorear
    # (solo «First Words»: ver preparar_dibujo). 0 = ninguno, el cuaderno
    # se dibuja; mientras los dibujos se hacen por partes (un PR por
    # estación), los días que faltan siguen como estaban.
    dias_con_dibujo: int = 0

    @property
    def salida_dias(self):
        return self.dir_contenido / "generated-days.tex"

    @property
    def salida_clave(self):
        return self.dir_contenido / "generated-clave.tex"

    @property
    def salida_sonidos(self):
        """Solo «First Words»: la tabla de sonidos del principio."""
        return self.dir_contenido / "generated-sonidos.tex"

    @property
    def ruta(self):
        """'content/palabras': para los mensajes y la cabecera de lo generado."""
        return self.dir_contenido.relative_to(ROOT).as_posix()

    @property
    def total(self):
        return self.dias_escritos or TOTAL_DIAS


PALABRAS = Perfil(
    nombre="palabras",
    idioma="es",
    dir_contenido=ROOT / "content" / "palabras",
    escalera=ESCALERA,
    globales=frozenset(PALABRAS_GLOBALES),
    titulo_medalla="¡Medalla de {}!",
    nombres_medalla=NOMBRE_MEDALLA_TRIMESTRE,
    animo_medalla=FRASES.animo_medalla,
)

FIRSTWORDS = Perfil(
    nombre="firstwords",
    idioma="en",
    dir_contenido=ROOT / "content" / "firstwords",
    escalera=ESCALERA_EN,
    globales=PALABRAS_GLOBALES_EN,
    titulo_medalla=ENGLISH.titulo_medalla,
    nombres_medalla=ENGLISH.nombre_medalla,
    animo_medalla=ENGLISH.animo_medalla,
    dias_con_dibujo=260,
)

PERFILES = {p.nombre: p for p in (PALABRAS, FIRSTWORDS)}

# El cuaderno que se está generando (main() lo cambia con --libro).
PERFIL = PALABRAS

# «First Words»: las tricky words que ya se han presentado (los viernes
# de primavera, ver preparar_dia), en minúscula, según se van validando
# los días en orden. En verano, una frase solo puede llevar estas -- y
# palabras que se leen sonido a sonido, y nombres del reparto --: nada
# de lo que se lee en verano es nuevo.
TRICKY_VISTAS = set()

# Cuántas tricky words presenta un viernes de primavera, como mucho.
MAX_TRICKY_VIERNES = 4

# Tipos de actividad de este cuaderno. Los que no llevan palabras
# propias ("relee", "repasa") son los viernes: la caja de lectura
# recoge las palabras de toda la semana.
TIPOS_VALIDOS = {
    "dibuja", "colorea", "completa", "traza", "escribe", "encuentra",
    "palmadas", "adivina", "une", "si_no", "relee", "repasa",
}
TIPOS_VIERNES = {"relee", "repasa"}

# «First Words»: el dibujo que se colorea (ver preparar_dibujo) va en
# diagrams/, y cada palabra tiene el suyo en diagrams/firstwords/, salvo
# las piezas que comparten todos (kit.tex, cargado por
# preamble-firstwords.tex). La adivinanza con dibujos da a elegir entre
# el del día y otros tantos.
DIR_DIBUJOS = ROOT / "diagrams"
DIBUJOS_QUE_NO_SE_COLOREAN = {"firstwords/kit"}
OTROS_ADIVINA = 2
# "une" con dibujos: cuántas palabras, cada una con el suyo.
PAREJAS_UNE_DIBUJOS = 4
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
    for t in PERFIL.escalera:
        lo, hi = t["semanas"]
        if lo <= semana <= hi:
            return t
    raise ErrorDeContenido(f"la semana {semana} no está en la escalera")


def max_partes(t):
    """Cuántas sílabas (español) o sonidos (inglés) puede tener una
    palabra en este tramo -- los círculos de "palmadas" son uno más."""
    return t["max_silabas"] if PERFIL.idioma == "es" else t["max_sonidos"]


def ultimo_tramo_de_palabras():
    """El último tramo de la escalera que todavía es de palabras (la
    primavera): en verano, una palabra de una frase tiene que caber en
    él -- todos los sonidos, pero no palabras más largas que en
    primavera."""
    return [t for t in PERFIL.escalera if "frase" not in t][-1]


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
    if PERFIL.idioma == "en":
        return comprobar_sonidos(num, palabra, semana, donde)
    t = tramo(semana)
    if "frase" in t or palabra.lower() in PERFIL.globales:
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


def comprobar_sonidos(num, palabra, semana, donde, grafemas=None):
    """La escalera de «First Words» para una palabra que lee la niña o
    el niño: en otoño, invierno y primavera, que solo tenga sonidos que
    ya se han visto, no más de los que admite su semana, y dos
    consonantes seguidas solo desde la primavera. En verano, las frases
    son lo que en los colegios ingleses se llama decodable text: cada
    palabra se lee sonido a sonido con todo lo que ya se sabe (la
    escalera de la primavera), o es una tricky word que ya se ha
    presentado, o un nombre del reparto."""
    t = tramo(semana)
    minus = palabra.lower()
    # num = None: una palabra que no es de ningún día (la tabla de sonidos).
    lugar = donde if num is None else f"día {num} ({donde})"
    if "frase" in t:
        # El genitivo de un nombre o de una palabra (Toby's, Mum's) es
        # la misma palabra: la 's se lee sola.
        if minus.endswith(("'s", "’s")):
            minus = minus[:-2]
            palabra = palabra[:-2]
        if minus in PERFIL.globales or minus in TRICKY_VISTAS:
            return
        # Una tricky word con -s o -es (comes, likes, does) es la misma
        # tricky word: se lee entera, y la s se añade.
        if (minus.endswith("s") and minus[:-1] in TRICKY_VISTAS) or (
            minus.endswith("es") and minus[:-2] in TRICKY_VISTAS
        ):
            return
        if minus in fonetica.TRICKY:
            raise ErrorDeContenido(
                f"{lugar}: «{palabra}» es una tricky word que todavía no se "
                "ha presentado -- tiene que salir antes en un viernes de "
                "primavera ('tricky')"
            )
        t = ultimo_tramo_de_palabras()
        grafemas = None
    elif minus in PERFIL.globales:
        return
    if minus in fonetica.TRICKY:
        raise ErrorDeContenido(
            f"{lugar}: «{palabra}» es una tricky word (tools/fonetica.py, "
            "TRICKY): se aprende entera, así que no puede salir como una "
            "palabra que se lee sonido a sonido"
        )
    if grafemas is None:
        try:
            grafemas = fonetica.segmentar(palabra)
        except fonetica.ErrorFonetica as exc:
            raise ErrorDeContenido(f"{lugar}: {exc}") from None
    r = fonetica.rasgos_de(grafemas)
    sobra = sorted(set(r["grafemas"]) - t["grafemas"])
    if sobra:
        raise ErrorDeContenido(
            f"{lugar}: «{palabra}» ({'-'.join(grafemas)}) tiene "
            f"{', '.join(sobra)}, que la escalera no admite hasta más "
            f"adelante (semana {semana})"
        )
    if r["sonidos"] > t["max_sonidos"]:
        raise ErrorDeContenido(
            f"{lugar}: «{palabra}» tiene {r['sonidos']} sonidos "
            f"({'-'.join(grafemas)}); en la semana {semana} el máximo es "
            f"{t['max_sonidos']}"
        )
    if r["grupo"] and not t["grupos"]:
        raise ErrorDeContenido(
            f"{lugar}: «{palabra}» ({'-'.join(grafemas)}) tiene "
            "dos consonantes seguidas, que la escalera no admite hasta la "
            f"primavera (semana {semana})"
        )


def leer_palabra(num, escrita, semana):
    """'pe-lo-ta' -> ('pelota', ['pe', 'lo', 'ta']), comprobando que el
    silabeo escrito a mano coincide con el automático y que la palabra
    cabe en la escalera de su semana. En inglés, lo mismo con sus
    sonidos: 'sh-ee-p' -> ('sheep', ['sh', 'ee', 'p'])."""
    if PERFIL.idioma == "en":
        return leer_palabra_en(num, escrita, semana)
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


def leer_palabra_en(num, escrita, semana):
    """Una tarjeta de «First Words». Los nombres del reparto que se leen
    de un golpe (Toby, Amy) van enteros, sin guiones: su tarjeta no
    lleva botones de sonidos."""
    if escrita.lower() in PERFIL.globales:
        if "-" in escrita:
            raise ErrorDeContenido(
                f"día {num}: «{escrita}» es un nombre que se lee de un golpe "
                "-- va entero, sin guiones"
            )
        return escrita, None
    try:
        palabra, grafemas = fonetica.leer_escrita(escrita)
    except fonetica.ErrorFonetica as exc:
        raise ErrorDeContenido(f"día {num}: {exc}") from None
    comprobar_sonidos(num, palabra, semana, "palabra del día", grafemas)
    return palabra, grafemas


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
    if PERFIL.idioma == "en":
        for token in frase.split():
            comprobar_sonidos(num, limpiar(token), semana, donde)


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
    r"""\begin{cajaPalTraza}$opciones
\begin{center}
{\Large\color{colorGris} $mayus~\lblTrazoDe~$palabra}

\vspace{4mm}
\begin{tikzpicture}$escala
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
    r"""\begin{cajaPalEscribe}$opciones
\instruccion{\lblPalInstruccionEscribe}
\begin{center}
$huecas
\end{center}
\lineaEscribir
$dibujo
\end{cajaPalEscribe}"""
)

PLANTILLA_ENCUENTRA = Template(
    r"""\begin{cajaPalEncuentra}$opciones
\instruccion{\lblPalInstruccionEncuentra}
\begin{center}
\fcolorbox{colorCompleta}{white}{\fontsize{30}{36}\selectfont\ $modelo\ }
\end{center}
\vspace{2mm}
{\fontsize{26}{32}\selectfont
\renewcommand{\arraystretch}{$estiramiento}
\begin{tabularx}{\linewidth}{@{}*{$columnas}{>{\centering\arraybackslash}X}@{}}
$filas
\end{tabularx}\par}
$dibujo
\end{cajaPalEncuentra}"""
)

PLANTILLA_PALMADAS = Template(
    r"""\begin{cajaPalPalmadas}$opciones
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
    r"""\begin{cajaPalUne}$opciones
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
    r"""\begin{cajaPalSiNo}$opciones
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


# «First Words», con dibujo para colorear (ver preparar_dibujo). El
# dibujo va en la parte de abajo de la caja (\tcblower, `centrado
# abajo`) y \dibujoHueco (preamble-firstwords.tex) lo hace del tamaño
# del sitio que deja la actividad: nunca se sale de la página.

PLANTILLA_COLOREA = Template(
    r"""\begin{cajaPalColorea}[centrado abajo]
{\Large $prompt\par}
\tcblower
\dibujoHueco{$dibujo}
\end{cajaPalColorea}"""
)

PLANTILLA_COMPLETA_DIBUJO = Template(
    r"""\begin{cajaPalCompleta}[centrado abajo]
{\Large $prompt\par}
\tcblower
\dibujoHueco{$dibujo}
\end{cajaPalCompleta}"""
)

PLANTILLA_ADIVINA_DIBUJOS = Template(
    r"""\begin{cajaPalAdivina}[centrado abajo]
\instruccion{$instruccion}
{\Large $adivinanza\par}
\tcblower
\tresDibujos$reserva{$a}{$b}{$c}$linea
\end{cajaPalAdivina}"""
)

PLANTILLA_UNE_DIBUJOS = Template(
    r"""\begin{cajaPalUne}
\instruccion{\lblFwInstruccionUneDibujos}
{\fontsize{26}{32}\selectfont\columnasCentradas
$anchos
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}m{\anchoUnePalabra} X >{\raggedright\arraybackslash}m{\anchoUneDibujo}@{}}
$filas
\end{tabularx}\par}
\end{cajaPalUne}"""
)

PLANTILLA_RELEE_DIBUJO = Template(
    r"""\begin{cajaPalRelee}[centrado abajo]
{\Large $prompt\par}
\tcblower
\dibujoHueco{$dibujo}
\end{cajaPalRelee}"""
)

PLANTILLA_REPASA_DIBUJO = Template(
    r"""\begin{cajaPalRepasa}[centrado abajo]
{\Large $prompt\par}
\tcblower
\dibujoHueco[\altoCartel]{$dibujo}
\cartelRepasa{$banner}
\end{cajaPalRepasa}"""
)


def remate_dibujo(actividad):
    """El "Ahora, dibuja: ..." opcional con que terminan las actividades
    que no son de dibujo en sí mismas -- en este nivel, casi todas."""
    prompt = actividad.get("prompt")
    if not prompt:
        return ""
    return r"\ahoraDibuja{" + escapar(prompt) + "}"


def remate(dia, actividad):
    """El remate de la actividad y las opciones de su caja: sin dibujo,
    el "Now draw: ..." de siempre; con dibujo («First Words»), "Now
    colour: ..." y el dibujo debajo, en todo el sitio que quede."""
    dibujo = dia.get("dibujo")
    if dibujo is None:
        return remate_dibujo(actividad), ""
    _campos_requeridos(dia["dia"], actividad, ["prompt"])
    return (
        r"\ahoraColorea{" + escapar(actividad["prompt"]) + "}\n"
        + r"\tcblower" + "\n"
        + r"\dibujoHueco{" + dibujo["ruta"] + "}",
        "[centrado abajo]",
    )


# --------------------------------------------------------------------
# La caja de lectura
# --------------------------------------------------------------------

def tarjeta_sonidos(trimestre, palabra, grafemas):
    """La tarjeta de «First Words»: la palabra, grande, con el botón de
    cada sonido debajo -- un punto si el sonido es una letra, una raya si
    son varias (sh, ee, ck), un arco de la vocal a la e si es una e
    mágica (cake). Cada grafema es un nodo de TikZ pegado al anterior, así
    que la palabra se ve entera y los botones caen debajo de sus letras.
    Los nombres que se leen de un golpe (grafemas = None) van sin
    botones."""
    if grafemas is None:
        return r"\tarjetaEntera{%d}{%s}" % (trimestre, escapar(palabra))
    nodos = []
    botones = []
    arco = None  # el nodo de la vocal de una e mágica, a la espera de su e
    for g in grafemas:
        if "_" in g:
            nodos.append(g.split("_")[0])
            arco = len(nodos)
            continue
        nodos.append(g)
        n = len(nodos)
        if fonetica.es_grafema_de_varias(g):
            botones.append(r"\botonRaya{g%d}" % n)
        else:
            botones.append(r"\botonPunto{g%d}" % n)
        if arco is not None:
            # La e va justo detrás de la consonante de la e mágica: en
            # cakes, c-a-k-e-s.
            nodos.append("e")
            botones.append(r"\botonArco{g%d}{g%d}" % (arco, len(nodos)))
            arco = None
    piezas = []
    for i, texto in enumerate(nodos, start=1):
        donde = "(0,0)" if i == 1 else f"(g{i - 1}.base east)"
        piezas.append(r"\node[grafema] (g%d) at %s {%s};" % (i, donde, escapar(texto)))
    return (
        r"\tarjetaSonidos{%d}{" % trimestre
        + " ".join(piezas) + " " + "".join(botones) + "}"
    )


def lectura_palabras(trimestre, palabras):
    """Tarjetas de palabra: sílabas arriba, palabra entera debajo (en
    inglés, la palabra con sus botones de sonidos, ver tarjeta_sonidos)."""
    if PERFIL.idioma == "en":
        tarjetas = [tarjeta_sonidos(trimestre, p, g) for p, g in palabras]
    else:
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


def lectura_tricky(palabras):
    """«First Words», los viernes de primavera: las tricky words de la
    semana, debajo de las palabras, cada una con su casilla y en un
    marco -- se leen enteras, no sonido a sonido."""
    celdas = r"\hspace{7mm}".join(
        r"\palabraTricky{" + escapar(p) + "}" for p in palabras
    )
    return (
        r"\par\vspace{4mm}{\footnotesize\color{colorGris}\lblFwTricky\par}\vspace{2mm}"
        + "\n" + r"{\centering " + celdas + r"\par}"
    )


# --------------------------------------------------------------------
# Actividades
# --------------------------------------------------------------------

def render_actividad(dia, semana_previa, dibujos_previos=()):
    """dibujos_previos: los dibujos con palabra de los días anteriores,
    [(palabra, ruta)] en orden (para "une" con dibujos)."""
    num = dia["dia"]
    trimestre = dia["trimestre"]
    semana = dia["semana"]
    actividad = dia["actividad"]
    tipo = actividad.get("tipo")
    # Las palabras sueltas que ha leído la niña o el niño ese día: las
    # de las tarjetas (T1-T3) o las de la frase (T4) -- ver preparar_dia.
    leidas = dia["palabras_leidas"]
    dibujo = dia.get("dibujo")
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

    if dibujo is None and tipo == "colorea":
        raise ErrorDeContenido(f"día {num}: 'colorea' necesita un 'dibujo'")
    if dibujo is not None and tipo == "dibuja":
        raise ErrorDeContenido(
            f"día {num}: tiene dibujo para colorear, así que su actividad "
            "es 'colorea', no 'dibuja'"
        )

    if tipo == "dibuja":
        _campos_requeridos(num, actividad, ["prompt"])
        tex = PLANTILLA_DIBUJA.substitute(prompt=escapar(actividad["prompt"]))

    elif tipo == "colorea":
        _campos_requeridos(num, actividad, ["prompt"])
        tex = PLANTILLA_COLOREA.substitute(
            prompt=escapar(actividad["prompt"]), dibujo=dibujo["ruta"]
        )

    elif tipo == "completa" and dibujo is not None:
        # Terminar el dibujo: colorearlo y añadirle lo que dice el
        # enunciado (un sombrero, las ruedas...).
        _campos_requeridos(num, actividad, ["prompt"])
        if "diagrama" in actividad:
            raise ErrorDeContenido(
                f"día {num}: 'completa' con dibujo para colorear no lleva "
                "'diagrama' -- se termina el dibujo"
            )
        tex = PLANTILLA_COMPLETA_DIBUJO.substitute(
            prompt=escapar(actividad["prompt"]), dibujo=dibujo["ruta"]
        )

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
        if ejemplo is None and PERFIL.idioma == "en":
            # "X as in box": en inglés casi ninguna palabra que se pueda
            # leer empieza por x, así que vale que la letra esté dentro.
            ejemplo = next((p for p in leidas if letra in p.lower()), None)
        if ejemplo is None:
            raise ErrorDeContenido(
                f"día {num}: 'traza' pide la letra {letra!r}, pero ninguna "
                f"palabra de ese día empieza por ella ({', '.join(leidas)})"
            )
        entrada = letras[letra]
        final, opciones = remate(dia, actividad)
        tex = PLANTILLA_TRAZA.substitute(
            mayus=escapar(letra.upper()),
            palabra=escapar(ejemplo),
            # Con dibujo debajo, las letras de puntos, algo más pequeñas
            # (siguen siendo grandes para repasarlas con el dedo), para
            # que al dibujo le quede sitio.
            escala="[scale=0.78]" if dibujo else "",
            puntos=puntos_tikz_letra(entrada["mayuscula"], entrada["minuscula"]),
            dibujo=final, opciones=opciones,
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
        final, opciones = remate(dia, actividad)
        # Dos veces la palabra hueca; con dibujo debajo, una, para que
        # al dibujo le quede sitio.
        hueca = r"\palabraHueca{" + escapar(palabra) + "}"
        tex = PLANTILLA_ESCRIBE.substitute(
            huecas=hueca if dibujo else hueca + "\n" + hueca,
            dibujo=final, opciones=opciones,
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
        final, opciones = remate(dia, actividad)
        tex = PLANTILLA_ENCUENTRA.substitute(
            modelo=escapar(modelo),
            columnas=columnas,
            # Con dibujo debajo, las filas de palabras, más juntas.
            estiramiento="1.5" if dibujo else "1.9",
            filas=" \\\\\n".join(filas) + " \\\\",
            dibujo=final, opciones=opciones,
        )
        if PERFIL.idioma == "en":
            clave = ("encuentra", f"“{modelo}”: {veces} times")
        else:
            clave = ("encuentra", f"«{modelo}»: {veces} veces")

    elif tipo == "palmadas":
        circulos = max_partes(tramo(semana)) + 1
        filas = " \\\\[7mm]\n".join(
            escapar(p) + " & " + r"\hspace{2mm}".join([r"\circuloPalmada"] * circulos)
            for p in leidas
        ) + " \\\\"
        final, opciones = remate(dia, actividad)
        tex = PLANTILLA_PALMADAS.substitute(filas=filas, dibujo=final, opciones=opciones)
        if PERFIL.idioma == "en":
            # Cuántos sonidos tiene cada palabra no es evidente para
            # quien no aprendió a leer en inglés (sheep: tres), así que
            # va en la clave.
            cuentas = [
                f"{p}: {len(g)}" for p, g in dia["tarjetas"] if g is not None
            ]
            clave = ("palmadas", ", ".join(cuentas))

    elif tipo == "adivina" and dibujo is not None:
        # «First Words»: la adivinanza se contesta coloreando uno de
        # tres dibujos -- el del día, que es la respuesta, y dos 'otros'
        # --, en un orden que cambia de un día a otro (reproducible).
        _campos_requeridos(num, actividad, ["adivinanza", "respuesta", "otros"])
        if "prompt" in actividad:
            raise ErrorDeContenido(
                f"día {num}: 'adivina' con dibujos no lleva 'prompt' -- lo "
                "que se colorea es la respuesta"
            )
        otros = actividad["otros"]
        if len(otros) != OTROS_ADIVINA:
            raise ErrorDeContenido(
                f"día {num}: 'adivina' con dibujos lleva {OTROS_ADIVINA} "
                f"'otros' (los dibujos que no son la respuesta), no {len(otros)}"
            )
        rutas = [dibujo["ruta"]] + [ruta_dibujo(num, o) for o in otros]
        if len(set(rutas)) != len(rutas):
            raise ErrorDeContenido(
                f"día {num}: en 'adivina', los tres dibujos tienen que ser distintos"
            )
        random.Random(num).shuffle(rutas)
        escribe = trimestre >= 2
        tex = PLANTILLA_ADIVINA_DIBUJOS.substitute(
            instruccion=(r"\lblFwInstruccionAdivinaColoreaEscribe" if escribe
                         else r"\lblFwInstruccionAdivinaColorea"),
            adivinanza=escapar(actividad["adivinanza"]),
            reserva=(r"[\altoLineaAdivina]" if escribe else ""),
            a=rutas[0], b=rutas[1], c=rutas[2],
            linea=("\n" + r"\lineaAdivina" if escribe else ""),
        )
        clave = ("adivina", actividad["respuesta"])

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

    elif tipo == "une" and dibujo is not None and "pares" not in actividad:
        if "prompt" in actividad:
            raise ErrorDeContenido(
                f"día {num}: 'une' con dibujos no lleva 'prompt' -- lo que se "
                "colorea son los dibujos de las palabras"
            )
        # «First Words»: cada palabra con su dibujo -- las más recientes
        # que tienen uno, la del día incluida, o las que diga 'dibujos'
        # (cuando dos dibujos recientes se parecen demasiado: Toby y
        # dog). Solo palabras ya leídas: son las de los dibujos de días
        # anteriores.
        disponibles = list(dibujos_previos) + [(dibujo["palabra"], dibujo["ruta"])]
        elegidas = actividad.get("dibujos")
        pares = []
        if elegidas is None:
            for palabra, ruta in reversed(disponibles):
                if any(palabra.lower() == p.lower() or ruta == r for p, r in pares):
                    continue
                pares.append((palabra, ruta))
                if len(pares) == PAREJAS_UNE_DIBUJOS:
                    break
            pares.reverse()
        else:
            for palabra in elegidas:
                ruta = next((r for p, r in reversed(disponibles)
                             if p.lower() == palabra.lower()), None)
                if ruta is None:
                    raise ErrorDeContenido(
                        f"día {num}: 'une' pide el dibujo de «{palabra}», y "
                        "ningún día hasta hoy lo tiene"
                    )
                pares.append((palabra, ruta))
            if dibujo["palabra"].lower() not in (p.lower() for p, _ in pares):
                raise ErrorDeContenido(
                    f"día {num}: en 'une', 'dibujos' tiene que llevar la "
                    f"palabra del dibujo del día («{dibujo['palabra']}»)"
                )
            if len({r for _, r in pares}) != len(pares):
                raise ErrorDeContenido(
                    f"día {num}: en 'une', dos palabras con el mismo dibujo"
                )
        if len(pares) < 3:
            raise ErrorDeContenido(
                f"día {num}: 'une' con dibujos necesita al menos 3 palabras "
                f"que tengan dibujo, y hasta hoy hay {len(pares)}"
            )
        derecha = [r for _, r in pares]
        rng = random.Random(num)
        mezclada = derecha[:]
        while any(a == b for a, b in zip(mezclada, derecha)):
            rng.shuffle(mezclada)
        filas = " \\\\\n".join(
            f"{escapar(p)}\\hfill\\textbullet & & \\dibujoUne{{{r}}}"
            for (p, _), r in zip(pares, mezclada)
        ) + " \\\\"
        tex = PLANTILLA_UNE_DIBUJOS.substitute(
            anchos="".join(f"\\anchoUne{{{escapar(p)}}}" for p, _ in pares),
            filas=filas,
        )

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
        final, opciones = remate(dia, actividad)
        tex = PLANTILLA_UNE.substitute(
            instruccion=instruccion, filas=filas, tam=tam, salto=tam + 6,
            dibujo=final, opciones=opciones,
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
        final, opciones = remate(dia, actividad)
        tex = PLANTILLA_SI_NO.substitute(filas=filas, dibujo=final, opciones=opciones)
        respuestas = {True: r"\lblSi", False: r"\lblNo"}
        clave = ("si_no", ", ".join(
            f"{escapar(t)} {respuestas[v]}" for t, v in afirmaciones
        ))

    elif tipo == "relee":
        _campos_requeridos(num, actividad, ["prompt"])
        if dibujo is not None:
            tex = PLANTILLA_RELEE_DIBUJO.substitute(
                prompt=escapar(actividad["prompt"]), dibujo=dibujo["ruta"]
            )
        else:
            tex = PLANTILLA_RELEE.substitute(prompt=escapar(actividad["prompt"]))

    elif tipo == "repasa":
        _campos_requeridos(num, actividad, ["prompt", "banner"])
        if dibujo is not None:
            tex = PLANTILLA_REPASA_DIBUJO.substitute(
                prompt=escapar(actividad["prompt"]), dibujo=dibujo["ruta"],
                banner=escapar(actividad["banner"]),
            )
        else:
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
    for fichero in sorted(PERFIL.dir_contenido.glob("q*.json")):
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
        if "tricky" in d:
            presentar_tricky(d, t)
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


def ruta_dibujo(num, nombre):
    """El dibujo `nombre` -> su ruta dentro de diagrams/, sin el .tex:
    "van" es diagrams/firstwords/van.tex; con una barra, la ruta desde
    diagrams/ ("english/loro"), para los dibujos que ya tenía el libro."""
    ruta = nombre if "/" in nombre else f"firstwords/{nombre}"
    if ruta in DIBUJOS_QUE_NO_SE_COLOREAN:
        raise ErrorDeContenido(f"día {num}: diagrams/{ruta}.tex no es un dibujo")
    if not (DIR_DIBUJOS / f"{ruta}.tex").exists():
        raise ErrorDeContenido(f"día {num}: el dibujo diagrams/{ruta}.tex no existe")
    return ruta


def preparar_dibujo(d):
    """«First Words»: el dibujo para colorear del día, `"dibujo": "van"`
    o `{"imagen": ..., "palabra": ...}` (cuando el fichero no se llama
    como la palabra). De lunes a jueves es el de una palabra que se lee
    ese día -- lo que se colorea es lo que se acaba de leer --; los
    viernes, una escena de la semana, que no necesita palabra (y si la
    lleva, es de las de la semana: ver generar). Deja en d["dibujo"]
    {"ruta", "palabra"}, con la palabra escrita como se lee (Amy)."""
    num = d["dia"]
    dibujo = d.get("dibujo")
    hasta = PERFIL.dias_con_dibujo
    if dibujo is None:
        if num <= hasta:
            raise ErrorDeContenido(
                f"día {num}: falta su 'dibujo' para colorear (lo llevan los "
                f"días 1-{hasta}: dias_con_dibujo, en el Perfil)"
            )
        return
    if num > hasta:
        raise ErrorDeContenido(
            f"día {num}: lleva 'dibujo', pero en este cuaderno solo lo llevan "
            f"los días 1-{hasta} (dias_con_dibujo, en su Perfil)"
        )
    if isinstance(dibujo, str):
        dibujo = {"imagen": dibujo}
    if (not isinstance(dibujo, dict) or "imagen" not in dibujo
            or set(dibujo) - {"imagen", "palabra"}):
        raise ErrorDeContenido(
            f"día {num}: 'dibujo' es el nombre del dibujo, o "
            "{\"imagen\": ..., \"palabra\": ...}"
        )
    ruta = ruta_dibujo(num, dibujo["imagen"])
    palabra = dibujo.get("palabra")
    if num % 5 != 0:
        if palabra is None:
            if "/" in dibujo["imagen"]:
                raise ErrorDeContenido(
                    f"día {num}: el dibujo {dibujo['imagen']} necesita su 'palabra'"
                )
            palabra = dibujo["imagen"]
        leida = next(
            (p for p in d["palabras_leidas"] if p.lower() == palabra.lower()), None
        )
        if leida is None:
            raise ErrorDeContenido(
                f"día {num}: el dibujo es de «{palabra}», que no es ninguna de "
                f"las palabras leídas ese día ({', '.join(d['palabras_leidas'])})"
            )
        palabra = leida
    d["dibujo"] = {"ruta": ruta, "palabra": palabra}


def comprobar_dibujos(dias):
    """«First Words»: ningún dibujo de diagrams/firstwords/ se queda sin
    usar -- un dibujo que no sale en ninguna página es trabajo perdido,
    o el de un día al que se le cambió la palabra y se quedó con otro."""
    if not PERFIL.dias_con_dibujo:
        return
    usados = set()
    for d in dias:
        if d.get("dibujo"):
            usados.add(d["dibujo"]["ruta"])
        for otro in d["actividad"].get("otros", []):
            usados.add(ruta_dibujo(d["dia"], otro))
    hay = {
        f"firstwords/{f.stem}" for f in (DIR_DIBUJOS / "firstwords").glob("*.tex")
    } - DIBUJOS_QUE_NO_SE_COLOREAN
    sobran = sorted(hay - usados)
    if sobran:
        raise ErrorDeContenido(
            "estos dibujos no salen en ningún día: "
            + ", ".join(f"diagrams/{r}.tex" for r in sobran)
        )


def presentar_tricky(d, t):
    """«First Words»: un viernes de primavera presenta unas pocas tricky
    words (fonetica.TRICKY), que se leen enteras. Cada una se presenta
    una sola vez en el año, y ninguna frase del verano puede llevar una
    que no se haya presentado antes."""
    num = d["dia"]
    tricky = d["tricky"]
    if PERFIL.idioma != "en" or "grupos" not in t or not t["grupos"]:
        raise ErrorDeContenido(
            f"día {num}: las tricky words solo se presentan los viernes de "
            "primavera, en «First Words»"
        )
    if not (1 <= len(tricky) <= MAX_TRICKY_VIERNES):
        raise ErrorDeContenido(
            f"día {num}: un viernes presenta entre 1 y {MAX_TRICKY_VIERNES} "
            f"tricky words, no {len(tricky)}"
        )
    for palabra in tricky:
        minus = palabra.lower()
        if minus not in fonetica.TRICKY:
            raise ErrorDeContenido(
                f"día {num}: «{palabra}» no es una tricky word "
                "(tools/fonetica.py, TRICKY)"
            )
        if minus in TRICKY_VISTAS:
            raise ErrorDeContenido(
                f"día {num}: la tricky word «{palabra}» ya se ha presentado antes"
            )
        TRICKY_VISTAS.add(minus)


def validar_dias(dias):
    if not dias:
        raise ErrorDeContenido(f"no hay ningún día en {PERFIL.ruta}/q*.json")
    if len(dias) != PERFIL.total:
        raise ErrorDeContenido(
            f"{PERFIL.ruta}/q*.json tiene {len(dias)} días, y el cuaderno "
            f"necesita {PERFIL.total}"
            + (" (dias_escritos, en su Perfil)" if PERFIL.dias_escritos else "")
        )
    for esperado, d in enumerate(dias, start=1):
        if d["dia"] != esperado:
            raise ErrorDeContenido(
                f"los días deben ser consecutivos empezando en 1: se esperaba "
                f"el día {esperado}, se encontró el día {d['dia']}"
            )
        preparar_dia(d)
        preparar_dibujo(d)


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
    "% GENERADO por tools/gen_palabras.py a partir de {ruta}/q*.json.\n"
    "% NO EDITAR A MANO -- los cambios se perderán en la siguiente\n"
    "% ejecución de `make generate`. Edita {ruta}/q*.json en su lugar.\n\n"
)


def cabecera(ruta):
    return CABECERA.format(nombre=f"{PERFIL.ruta}/{ruta.name}", ruta=PERFIL.ruta)


def generar(dias):
    """(tex, clave, paginas, entradas): el libro entero y su clave, y la
    página y la entrada de la clave de cada día -- [(d, tex)] sin las
    medallas y [(d, entrada)] --, de donde salen las ediciones
    (generar_ediciones)."""
    piezas = [cabecera(PERFIL.salida_dias)]
    claves = [cabecera(PERFIL.salida_clave)]
    paginas, entradas = [], []
    dibujos_previos = []  # [(palabra, ruta)], para "une" con dibujos
    for d in dias:
        num, trimestre = d["dia"], d["trimestre"]
        tipo = d["actividad"]["tipo"]
        previas = semana_hasta(dias, d)
        dibujo = d.get("dibujo")
        if tipo in TIPOS_VIERNES and dibujo and dibujo["palabra"]:
            palabra = dibujo["palabra"]
            leida = next((p for p in previas if p.lower() == palabra.lower()), None)
            if leida is None:
                raise ErrorDeContenido(
                    f"día {num}: el dibujo del viernes es de «{palabra}», que "
                    "no se ha leído esa semana"
                )
            dibujo["palabra"] = leida
        if tipo in TIPOS_VIERNES:
            if not previas:
                raise ErrorDeContenido(
                    f"día {num}: '{tipo}' no encuentra nada leído esa semana"
                )
            lectura = lectura_semana(trimestre, previas)
            if d.get("tricky"):
                lectura += "\n" + lectura_tricky(d["tricky"])
            instruccion = (r"\lblPalInstruccionSemanaFrases" if trimestre == 4
                           else r"\lblPalInstruccionSemana")
        elif trimestre == 4:
            lectura = lectura_frase(d["frase"])
            instruccion = INSTRUCCION_LECTURA[4]
        else:
            lectura = lectura_palabras(trimestre, d["tarjetas"])
            instruccion = INSTRUCCION_LECTURA[trimestre]
            if PERFIL.idioma == "en" and all(g is None for _, g in d["tarjetas"]):
                # Solo un nombre que se lee de un golpe: no hay botones
                # que tocar.
                instruccion = r"\lblFwInstruccionNombre"

        # Para "une" por defecto hacen falta las palabras previas de la
        # semana, no las frases.
        previas_palabras = previas if trimestre != 4 else []
        actividad_tex, clave = render_actividad(d, previas_palabras, dibujos_previos)
        if dibujo and dibujo["palabra"]:
            dibujos_previos.append((dibujo["palabra"], dibujo["ruta"]))
        pagina = PLANTILLA_DIA.substitute(
            dia=num,
            semana=d["semana"],
            trimestre=trimestre,
            tema=escapar(d["tema"]),
            instruccion=instruccion,
            lectura=lectura,
            actividad=actividad_tex,
        )
        piezas.append(pagina)
        paginas.append((d, pagina))
        if clave:
            etiqueta = {
                "adivina": r"\lblAdivina", "une": r"\lblUne",
                "encuentra": r"\lblEncuentra", "si_no": r"\lblSiNo",
                "palmadas": r"\lblPalmadas",
            }[clave[0]]
            texto = clave[1] if clave[0] in ("une", "si_no") else escapar(clave[1])
            entrada = f"\\claveEntrada{{{num}}}{{{etiqueta}}}{{{texto}}}\n"
            claves.append(entrada)
            entradas.append((d, entrada))

        if num == ULTIMO_DIA_TRIMESTRE.get(trimestre) and trimestre in PERFIL.nombres_medalla:
            banner = d["actividad"].get("banner")
            if not banner:
                raise ErrorDeContenido(
                    f"día {num}: cierra el trimestre {trimestre} y necesita "
                    "un 'banner' (actividad 'repasa') para la medalla"
                )
            piezas.append(PLANTILLA_MEDALLA.substitute(
                dia=num,
                titulo=PERFIL.titulo_medalla.format(PERFIL.nombres_medalla[trimestre]),
                banner=escapar(banner),
                animo=PERFIL.animo_medalla,
            ))
    return "\n".join(piezas), "".join(claves), paginas, entradas


def generar_ediciones(dias, paginas, entradas):
    """[(ruta, contenido)]: los .tex de cada edición del cuaderno (el
    cuaderno de verano...), ver tools/ediciones.py. En «First Words»,
    también las tricky words que la edición da por sabidas -- las que el
    libro entero presenta antes de su primer día (los viernes de
    primavera, ver presentar_tricky) --, para su página del adulto
    (\\trickyLista, preamble-firstwords.tex)."""
    salidas = salidas_ediciones(
        dias, paginas, entradas, PERFIL.salida_dias, PERFIL.salida_clave,
        cabecera, PERFIL.idioma,
    )
    if PERFIL.idioma == "en":
        for e in ediciones_completas(dias):
            ruta = ruta_edicion(PERFIL.dir_contenido / "generated-tricky.tex", e)
            palabras = [
                p for d in dias if d["dia"] < e.desde for p in d.get("tricky", [])
            ]
            salidas.append((ruta, cabecera(ruta) + "".join(
                f"\\trickyLista{{{escapar(p)}}}\n" for p in palabras
            )))
    return salidas


def comprobar_trazo(dias):
    """Las 27 letras del abecedario se trazan al menos una vez en el año
    -- igual que en el cuaderno de frases, pero aquí cada letra es la
    inicial de una palabra que se acaba de leer."""
    letras, _ = datos_trazo()
    if PERFIL.idioma == "en":
        # En inglés, las 26 letras: la ñ no está.
        letras = [l for l in letras if l in "abcdefghijklmnopqrstuvwxyz"]
    trazadas = {d["actividad"]["letra"] for d in dias if d["actividad"]["tipo"] == "traza"}
    faltan = sorted(set(letras) - trazadas)
    if faltan and len(dias) == TOTAL_DIAS:
        raise ErrorDeContenido(
            f"ninguna actividad 'traza' practica estas letras: {', '.join(faltan)}"
        )


def comprobar_cobertura(dias):
    """«First Words»: cada sonido que llega en una estación sale en alguna
    tarjeta antes de que se acabe. La tabla de sonidos del principio
    (generar_sonidos) enseña todos los de la escalera, en su estación, y
    dice "every sound in the book": tiene que ser verdad, y cada sonido
    nuevo, practicarse en alguna palabra. Una estación se comprueba en
    cuanto está escrita entera."""
    if PERFIL.idioma != "en":
        return
    vistos = set()
    al_acabar = {}  # trimestre -> los grafemas vistos hasta su último día
    fin_de = {fin: trimestre for trimestre, fin in ULTIMO_DIA_TRIMESTRE.items()}
    for d in dias:
        for _, grafemas in d.get("tarjetas", []):
            vistos.update(g.lower() for g in grafemas or [])
        if d["dia"] in fin_de:
            al_acabar[fin_de[d["dia"]]] = set(vistos)
    anteriores = frozenset()
    for t in PERFIL.escalera:
        if "grafemas" not in t:
            continue
        nuevos = t["grafemas"] - anteriores
        anteriores = t["grafemas"]
        lo, hi = t["semanas"]
        trimestre = (hi - 1) // 13 + 1
        if trimestre not in al_acabar:
            continue  # esa estación todavía no está escrita entera
        faltan = sorted(nuevos - al_acabar[trimestre])
        if faltan:
            raise ErrorDeContenido(
                f"{', '.join(faltan)}: la escalera los trae en las semanas "
                f"{lo}-{hi} y la tabla de sonidos los enseña, pero no salen "
                "en ninguna tarjeta antes del día "
                f"{ULTIMO_DIA_TRIMESTRE[trimestre]} -- alguna palabra de esa "
                "estación tiene que tenerlos"
            )


def tabla(dias):
    """Resumen por semana, en Markdown, para GITHUB_STEP_SUMMARY."""
    if PERFIL.idioma == "en":
        return tabla_en(dias)
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
                    if palabra.lower() in PERFIL.globales:
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


def tabla_en(dias):
    """La tabla de «First Words»: qué se lee cada semana, cuántos sonidos
    tiene la palabra más larga y qué grafemas salen por primera vez."""
    lineas = [
        "| Semana | Trim. | Tema | Lee | Sonidos (máx.) | Grafemas nuevos |",
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
            sonidos = "–"
            nuevos = ""
        else:
            lee = f"{t['palabras']} {'palabra' if t['palabras'] == 1 else 'palabras'}/día"
            maxima = 0
            nuevos_semana = set()
            for d in grupo:
                for _, grafemas in d.get("tarjetas", []):
                    if grafemas is None:
                        continue
                    maxima = max(maxima, len(grafemas))
                    nuevos_semana |= {g.lower() for g in grafemas}
            nuevos = " ".join(sorted(nuevos_semana - vistos))
            vistos |= nuevos_semana
            sonidos = f"{maxima} (obj. {t['max_sonidos']})"
        lineas.append(
            f"| {semana} | {grupo[0]['trimestre']} | {grupo[0]['tema']} | "
            f"{lee} | {sonidos} | {nuevos} |"
        )
    return "\n".join(lineas)


# --------------------------------------------------------------------
# «First Words»: la tabla de sonidos del principio del cuaderno
# --------------------------------------------------------------------

# El título de cada sección de la tabla (lang/en.tex): una por tramo de
# la escalera que trae sonidos nuevos.
TITULOS_SONIDOS = [
    r"\lblFwSonidosUno", r"\lblFwSonidosDos",
    r"\lblFwSonidosTres", r"\lblFwSonidosCuatro",
]

CABECERA_SONIDOS = (
    "% {nombre}\n"
    "% GENERADO por tools/gen_palabras.py a partir de tools/fonetica.py\n"
    "% (EJEMPLOS) y de la escalera de «First Words» (ESCALERA_EN).\n"
    "% NO EDITAR A MANO -- los cambios se perderán en la siguiente\n"
    "% ejecución de `make generate`.\n\n"
)


def ejemplo_resaltado(grafema, ejemplo):
    """La palabra de ejemplo, con las letras de su sonido resaltadas:
    ('sh', 'ship') -> '\\resalta{sh}ip'; ('a_e', 'cake') ->
    'c\\resalta{a}k\\resalta{e}' (la e mágica: la vocal y la e del final)."""
    piezas = []
    e_pendiente = None  # la e de una e mágica, que va tras su consonante
    for g in fonetica.segmentar(ejemplo):
        if "_" in g:
            vocal, e = g.split("_")
            if g.lower() == grafema:
                vocal, e = r"\resalta{%s}" % vocal, r"\resalta{%s}" % e
            piezas.append(vocal)
            e_pendiente = e
            continue
        piezas.append(r"\resalta{%s}" % g if g.lower() == grafema else g)
        if e_pendiente is not None:
            piezas.append(e_pendiente)
            e_pendiente = None
    return "".join(piezas)


def generar_sonidos():
    """La tabla de sonidos de «First Words» (frontmatter/firstwords/
    sonidos.tex): cada grafema en el tramo de la escalera en que llega,
    con una palabra de ejemplo (fonetica.EJEMPLOS) que ya se puede leer
    entonces. Sale de ESCALERA_EN, así que la tabla no puede decir una
    cosa y la escalera otra: falla si a un grafema le falta su ejemplo,
    si sobra alguno, o si un ejemplo no cabe en la escalera de su tramo."""
    piezas = [CABECERA_SONIDOS.format(nombre=f"{PERFIL.ruta}/generated-sonidos.tex")]
    titulos = iter(TITULOS_SONIDOS)
    anteriores = frozenset()
    for t in PERFIL.escalera:
        if "grafemas" not in t:
            continue
        nuevos = t["grafemas"] - anteriores
        anteriores = t["grafemas"]
        faltan = sorted(nuevos - set(fonetica.EJEMPLOS))
        if faltan:
            raise ErrorDeContenido(
                "tabla de sonidos: falta una palabra de ejemplo para "
                f"{', '.join(faltan)} (tools/fonetica.py, EJEMPLOS)"
            )
        piezas.append(r"\seccionSonidos{%s}" % next(titulos))
        for g in (g for g in fonetica.EJEMPLOS if g in nuevos):
            ejemplo = fonetica.EJEMPLOS[g]
            comprobar_sonidos(
                None, ejemplo, t["semanas"][0],
                f"tabla de sonidos, el ejemplo de «{g}»",
            )
            piezas.append(r"\sonido{%s}{%s}" % (
                g.replace("_", r"\textendash{}"), ejemplo_resaltado(g, ejemplo)
            ))
        piezas.append(r"\finSonidos")
    sobran = sorted(set(fonetica.EJEMPLOS) - anteriores)
    if sobran:
        raise ErrorDeContenido(
            f"tabla de sonidos: {', '.join(sobran)} tiene(n) ejemplo en "
            "tools/fonetica.py (EJEMPLOS), pero no está(n) en la escalera"
        )
    return "\n".join(piezas) + "\n"


def perfil_desde_argv(argv):
    """`--libro firstwords` (o `--libro=firstwords`) -> su Perfil; sin la
    opción, el cuaderno de primeras palabras en español, como siempre."""
    nombre = "palabras"
    for i, arg in enumerate(argv):
        if arg == "--libro" and i + 1 < len(argv):
            nombre = argv[i + 1]
        elif arg.startswith("--libro="):
            nombre = arg.split("=", 1)[1]
    if nombre not in PERFILES:
        raise SystemExit(
            f"ERROR: libro desconocido {nombre!r} -- los de este generador: "
            + ", ".join(sorted(PERFILES))
        )
    return PERFILES[nombre]


def main():
    global PERFIL
    PERFIL = perfil_desde_argv(sys.argv[1:])
    check_only = "--check" in sys.argv
    modo_tabla = "--tabla" in sys.argv

    try:
        comprobar_preamble()
        dias = cargar_dias()
        validar_dias(dias)
        for d in dias:
            comprobar_campos(d)
        comprobar_trazo(dias)
        comprobar_cobertura(dias)
        comprobar_dibujos(dias)
        tex, clave, paginas, entradas = generar(dias)
        salidas = [(PERFIL.salida_dias, tex), (PERFIL.salida_clave, clave)]
        if PERFIL.idioma == "en":
            salidas.append((PERFIL.salida_sonidos, generar_sonidos()))
        ediciones = generar_ediciones(dias, paginas, entradas)
        salidas += ediciones
    except ErrorDeContenido as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if modo_tabla:
        print(tabla(dias))
        return 0

    if check_only:
        for ruta, contenido in salidas:
            actual = ruta.read_text(encoding="utf-8") if ruta.exists() else None
            if actual != contenido:
                print(
                    f"DESACTUALIZADO: {ruta} no coincide con "
                    f"{PERFIL.ruta}/q*.json -- ejecuta `make generate`.",
                    file=sys.stderr,
                )
                return 1
        obras = ""
        if PERFIL.dias_escritos:
            obras = f" (en obras: {len(dias)} de {TOTAL_DIAS} días escritos)"
        prefijo = "" if PERFIL is PALABRAS else f" ({PERFIL.nombre})"
        nombres = [ruta.name for ruta, _ in salidas]
        dibujos = ""
        if PERFIL.dias_con_dibujo:
            n = len({d["dibujo"]["ruta"] for d in dias if d.get("dibujo")})
            dibujos = f", {n} dibujos para colorear"
        print(f"OK{prefijo}: {len(dias)} días validados{obras}{dibujos}, "
              f"{', '.join(nombres[:-1])} y {nombres[-1]} al día.")
        return 0

    for ruta, contenido in salidas:
        ruta.write_text(contenido, encoding="utf-8")
    print(f"Escrito {PERFIL.salida_dias} con {len(dias)} días, y {PERFIL.salida_clave}.")
    if PERFIL.idioma == "en":
        print(f"Escrito {PERFIL.salida_sonidos}.")
    for ruta, _ in ediciones:
        print(f"Escrito {ruta}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
