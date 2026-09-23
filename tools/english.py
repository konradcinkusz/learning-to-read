"""«Read and Draw», el cuaderno en inglés: el texto en párrafos y las
actividades de análisis sencillo -- ver notes/05-english.md para el
porqué de cada una.

tools/gen_days.py llama a este módulo cuando el libro es "Read and Draw"
(`--libro english`), con la misma forma que tools/lupa.py:
validar_texto() comprueba el texto de un día, pagina_dia() genera su
página entera (caja de lectura + actividad) y entrada_clave() su línea
en la clave de respuestas.

Un nivel por debajo de "Leo con lupa": textos más cortos, y un análisis
mucho más sencillo -- casi siempre dibujar, colorear, marcar, rodear o
unir, casi nunca escribir más de una palabra, porque se lee en un idioma
que todavía se está aprendiendo. Pero sigue siendo análisis: cada
actividad obliga a volver al texto (cuántos, de qué color, dónde, por
qué, qué pasó primero). Y el texto está hecho de oraciones compuestas
(because, when, who, that, but, so...): dos actividades, `mitades` y
`huecos`, trabajan justo eso, unir las dos partes de una frase del texto.

Lo que se puede comprobar a máquina se comprueba aquí antes de generar
nada:

  - huecos: cada frase, con su palabra en el hueco, está tal cual en los
    textos de la semana hasta ese día (la respuesta sale del texto, no de
    la imaginación de quien escribió la actividad);
  - mitades: cada frase, con sus dos mitades juntas, también;
  - busca: cada palabra que hay que encontrar está en el texto del día;
  - rodea: la respuesta es una de las opciones; si_no: hay respuestas
    "yes" y "no", no todas iguales;
  - colorea y donde: el dibujo existe (diagrams/english/);
  - el propio texto: inglés británico (colour, Mum, neighbour; Mr sin
    punto), sin letras ni signos del español fuera de los nombres del
    reparto, ni sus palabras más frecuentes (una frase copiada del
    cuaderno en español se nota aquí), y el diálogo entre comillas “ ”
    bien cerradas.
"""

import random
import re
from string import Template

from comun import ErrorDeContenido, campos_requeridos, escapar
from libros import ENGLISH, ROOT
from lupa import formatear_texto, texto_plano

DIR_DIBUJOS = ROOT / "diagrams" / "english"

# ---------------------------------------------------------------------
# El texto del día
# ---------------------------------------------------------------------
#
# "texto" es una lista de párrafos, con las mismas marcas que "Leo con
# lupa" (ver tools/lupa.py): "> " una nota, cartel, carta o postal que
# los personajes leen (recuadro blanco), "- " un elemento de lista, "\n"
# un salto de línea. El diálogo, a la inglesa: entre comillas “ ”, nunca
# con raya.

FINALES_VALIDOS = (".", "!", "?", "…", "”", ":")

# Letras fuera del inglés: solo en los nombres del reparto (Lucía,
# Sofía, Andrés, Martín). Cualquier otra palabra con tilde o eñe es,
# casi seguro, español que se ha colado.
PALABRAS_CON_TILDE = frozenset(
    n for n in ENGLISH.nombres_propios if not n.isascii()
)

# Inglés británico, el que se enseña en el colegio en España (y el de la
# familia de Amy, que viene de Londres). Palabra estadounidense ->
# británica.
AMERICANISMOS = {
    "color": "colour", "colors": "colours", "colored": "coloured",
    "coloring": "colouring", "colorful": "colourful",
    "favorite": "favourite", "favorites": "favourites",
    "neighbor": "neighbour", "neighbors": "neighbours",
    "gray": "grey", "mom": "mum", "moms": "mums", "mommy": "mummy",
    "candy": "sweets", "candies": "sweets", "cookie": "biscuit",
    "cookies": "biscuits", "vacation": "holiday", "vacations": "holidays",
    "soccer": "football", "apartment": "flat", "sidewalk": "pavement",
    "center": "centre", "theater": "theatre", "mailbox": "postbox",
    "flashlight": "torch", "trash": "rubbish", "garbage": "rubbish",
    "math": "maths", "sweater": "jumper", "eraser": "rubber",
    "truck": "lorry", "pajamas": "pyjamas", "cozy": "cosy",
    "donut": "doughnut", "mustache": "moustache", "airplane": "plane",
    "traveled": "travelled", "traveling": "travelling",
    "jewelry": "jewellery", "stroller": "pushchair", "faucet": "tap",
    "zucchini": "courgette", "eggplant": "aubergine",
}

# Palabras muy frecuentes del español que no son palabras inglesas
# (nada de "come" o "hay", que también lo son): una frase en español sin
# ninguna tilde ("Toby tiene una pelota") no la caza la comprobación de
# letras, pero casi seguro lleva alguna de estas.
PALABRAS_ESPANOLAS = frozenset({
    "el", "los", "las", "una", "unos", "unas", "del", "que", "y", "es",
    "con", "para", "por", "pero", "muy", "porque", "cuando", "tiene",
    "esta", "este", "sus",
})

# "Mr." y "Mrs." con punto son de Estados Unidos -- y además cortarían
# la frase en dos para tools/metricas.py.
PATRON_TRATAMIENTO = re.compile(r"\b(Mr|Mrs|Ms|Dr)\.")
PATRON_PALABRA = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)*")


def _cadenas(valor):
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for v in valor.values():
            yield from _cadenas(v)
    elif isinstance(valor, list):
        for v in valor:
            yield from _cadenas(v)


def _comprobar_ingles(num, cadena):
    """Una cadena cualquiera del día (texto o actividad): inglés
    británico, sin rastros del español ni comillas rectas."""
    corta = cadena[:50]
    if '"' in cadena:
        raise ErrorDeContenido(
            f"día {num}: comilla recta en «{corta}...» -- el diálogo va entre “ ”"
        )
    if "’" in cadena or "‘" in cadena:
        raise ErrorDeContenido(
            f"día {num}: apóstrofo tipográfico en «{corta}...» -- escribe ' "
            "(recto): LaTeX ya lo imprime curvo"
        )
    if "  " in cadena:
        raise ErrorDeContenido(f"día {num}: doble espacio en «{corta}...»")
    for signo in ("¿", "¡", "«", "»"):
        if signo in cadena:
            raise ErrorDeContenido(
                f"día {num}: «{signo}» en «{corta}...» -- es un signo del español"
            )
    if PATRON_TRATAMIENTO.search(cadena):
        raise ErrorDeContenido(
            f"día {num}: «{PATRON_TRATAMIENTO.search(cadena).group(0)}» en "
            f"«{corta}...» -- en inglés británico, sin punto (Mr Brown)"
        )
    for palabra in PATRON_PALABRA.findall(cadena):
        # "Lucía's", "Mum's": lo que se mira es la palabra, sin el 's.
        minus = palabra.lower().split("'")[0]
        if minus in AMERICANISMOS:
            raise ErrorDeContenido(
                f"día {num}: «{palabra}» es inglés de Estados Unidos -- "
                f"en británico, «{AMERICANISMOS[minus]}»"
            )
        if minus in PALABRAS_ESPANOLAS:
            raise ErrorDeContenido(
                f"día {num}: «{palabra}» en «{corta}...» -- parece español"
            )
        if not palabra.isascii() and minus not in PALABRAS_CON_TILDE:
            raise ErrorDeContenido(
                f"día {num}: «{palabra}» no es inglés (ni un nombre del reparto, "
                "ver ENGLISH.nombres_propios en tools/libros.py)"
            )


def validar_texto(num, d):
    texto = d.get("texto")
    if not isinstance(texto, list) or not texto:
        raise ErrorDeContenido(
            f"día {num}: este cuaderno necesita 'texto', una lista de párrafos"
        )
    if not d.get("tema"):
        raise ErrorDeContenido(f"día {num}: falta el 'tema' del día")
    for parrafo in texto:
        if not isinstance(parrafo, str) or not parrafo.strip():
            raise ErrorDeContenido(f"día {num}: hay un párrafo vacío en 'texto'")
        if parrafo != parrafo.strip():
            raise ErrorDeContenido(
                f"día {num}: el párrafo «{parrafo[:40]}...» empieza o termina "
                "con espacios"
            )
        if parrafo.startswith(("—", "–", "-")) and not parrafo.startswith("- "):
            raise ErrorDeContenido(
                f"día {num}: «{parrafo[:40]}...» -- en inglés, el diálogo va "
                "entre comillas “ ”, no con raya"
            )
        if parrafo.count("“") != parrafo.count("”"):
            raise ErrorDeContenido(
                f"día {num}: comillas sin cerrar en «{parrafo[:50]}...»"
            )
        if parrafo.startswith(("- ", "> ")):
            continue
        if not parrafo.endswith(FINALES_VALIDOS):
            raise ErrorDeContenido(
                f"día {num}: el párrafo «...{parrafo[-40:]}» no termina en un "
                "signo de puntuación final"
            )
    for cadena in _cadenas(d):
        _comprobar_ingles(num, cadena)


# ---------------------------------------------------------------------
# Plantillas
# ---------------------------------------------------------------------

PLANTILLA_DIA = Template(
    r"""\begin{lupapagina}{$dia}{$semana}{$trimestre}{$tema}
\begin{cajaLectura}{$instruccion}
\fuenteIngles{$fuente}%
$texto
\end{cajaLectura}
\vspace{4mm}
$actividad
\end{lupapagina}
"""
)

# Todas las actividades usan la misma caja (actividadIngles, ver
# preamble-english.tex), que llena todo el alto que le queda a la
# página; lo que va después de \tcblower (la lista para comprobar un
# dibujo, el banner de las páginas leídas) se queda pegado al fondo.
PLANTILLA_ACTIVIDAD = Template(
    r"""\begin{actividadIngles}{$color}{$icono\ $titulo}
$arriba
\tcblower
$abajo
\end{actividadIngles}"""
)

PLANTILLA_ACTIVIDAD_SIN_ABAJO = Template(
    r"""\begin{actividadIngles}{$color}{$icono\ $titulo}
$arriba
\end{actividadIngles}"""
)

# Mismos colores que en los otros cuadernos, por familias: azul para
# dibujar, rosa para colorear, morado para comprobar leyendo (marcar,
# rodear, ordenar, escribir una palabra), naranja para unir y adivinar,
# fucsia para lo propio (repasar, crear).
COLOR = {
    "dibuja": "colorDibuja",
    "donde": "colorDibuja",
    "vinetas": "colorDibuja",
    "colorea": "colorCompleta",
    "si_no": "colorResponde",
    "rodea": "colorResponde",
    "ordena": "colorResponde",
    "huecos": "colorResponde",
    "busca": "colorResponde",
    "relaciona": "colorRelaciona",
    "mitades": "colorRelaciona",
    "adivina": "colorRelaciona",
    "repasa": "colorCrea",
    "crea": "colorCrea",
}

TITULO = {
    "dibuja": r"\lblIngDibuja",
    "donde": r"\lblIngDonde",
    "vinetas": r"\lblIngVinetas",
    "colorea": r"\lblIngColorea",
    "si_no": r"\lblIngSiNo",
    "rodea": r"\lblIngRodea",
    "ordena": r"\lblIngOrdena",
    "huecos": r"\lblIngHuecos",
    "busca": r"\lblIngBusca",
    "relaciona": r"\lblIngRelaciona",
    "mitades": r"\lblIngMitades",
    "adivina": r"\lblIngAdivina",
    "repasa": r"\lblIngRepasa",
    "crea": r"\lblIngCrea",
}

ICONO = {
    "dibuja": r"\icoLapiz",
    "donde": r"\icoSitio",
    "vinetas": r"\icoVinetas",
    "colorea": r"\icoCera",
    "si_no": r"\icoMarca",
    "rodea": r"\icoRodea",
    "ordena": r"\icoOrden",
    "huecos": r"\icoHueco",
    "busca": r"\icoBusca",
    "relaciona": r"\icoUne",
    "mitades": r"\icoUne",
    "adivina": r"\icoAdivina",
    "repasa": r"\icoEstrella",
    "crea": r"\icoCara",
}


def _instruccion(texto_tex):
    return r"\instruccionIng{" + texto_tex + "}"


def _banner(actividad):
    banner = actividad.get("banner")
    if not banner:
        return ""
    return r"\bannerDia{" + escapar(banner) + "}"


def _caja(tipo, arriba, abajo, actividad):
    banner = _banner(actividad)
    if banner:
        abajo = (abajo + "\n" if abajo else "") + banner
    datos = {"color": COLOR[tipo], "icono": ICONO[tipo], "titulo": TITULO[tipo],
             "arriba": arriba}
    if not abajo:
        return PLANTILLA_ACTIVIDAD_SIN_ABAJO.substitute(datos)
    return PLANTILLA_ACTIVIDAD.substitute(datos, abajo=abajo)


def _y(elementos):
    """['1', '2', '3'] -> '1, 2 \\lblIngY{} 3' ("1, 2 and 3")."""
    elementos = [str(e) for e in elementos]
    if len(elementos) == 1:
        return elementos[0]
    return ", ".join(elementos[:-1]) + r" \lblIngY{} " + elementos[-1]


def _barajar(num, elementos):
    """Baraja reproducible (la misma cada vez que se genera el libro) y
    nunca en el orden original -- si no, no hay nada que ordenar o unir."""
    rng = random.Random(num)
    mezclados = elementos[:]
    while mezclados == elementos and len(set(elementos)) > 1:
        rng.shuffle(mezclados)
    return mezclados


def _normalizar(texto):
    """Para buscar una frase de la actividad dentro del texto: sin
    mayúsculas, con los espacios colapsados."""
    return " ".join(texto.lower().split())


def _sin_cortes(texto):
    """Una palabra o expresión de una lista (lo que hay que dibujar, las
    palabras de huecos) en una caja, para que la línea se corte entre dos
    elementos y nunca por dentro de uno («the paw / prints»)."""
    return r"\mbox{" + escapar(texto) + "}"


def _dibujo(num, nombre):
    if not (DIR_DIBUJOS / f"{nombre}.tex").exists():
        raise ErrorDeContenido(
            f"día {num}: no existe diagrams/english/{nombre}.tex"
        )
    return r"\dibujoIng{" + nombre + "}"


def _tabla_une(filas_izq, filas_der):
    """Dos columnas con un punto pegado a cada frase -- al final de la
    izquierda, al principio de la derecha --, para unirlas con una línea
    (relaciona, mitades). El punto va dentro del texto y no en una
    columna aparte: si una frase ocupa dos líneas, el punto sigue
    estando donde acaba (o empieza) la frase."""
    filas = "\n".join(
        f"{escapar(i)}~\\puntoUne & & \\puntoUne~{escapar(d)} \\\\[5mm]"
        for i, d in zip(filas_izq, filas_der)
    )
    return (
        r"\renewcommand{\arraystretch}{1.3}" + "\n"
        + r"\begin{tabularx}{\linewidth}{@{}>{\raggedleft\arraybackslash}X"
        + r" p{18mm} >{\raggedright\arraybackslash}X@{}}" + "\n"
        + filas + "\n\\end{tabularx}\n"
        + r"\renewcommand{\arraystretch}{1}"
    )


# ---------------------------------------------------------------------
# Un render por tipo de actividad
# ---------------------------------------------------------------------

def render_dibuja(num, a, contexto):
    """Read and draw: el texto describe algo con detalle (cuántos, de
    qué color, dónde) y se dibuja tal cual. Abajo, preguntas para
    comprobar el dibujo con el texto delante -- preguntan, no dan la
    respuesta: si la dieran, no haría falta volver al texto."""
    campos_requeridos(num, a, ["prompt", "comprueba", "clave"])
    comprueba = a["comprueba"]
    if not 2 <= len(comprueba) <= 4:
        raise ErrorDeContenido(
            f"día {num}: dibuja necesita entre 2 y 4 preguntas en 'comprueba'"
        )
    arriba = _instruccion(escapar(a["prompt"]))
    abajo = ""
    if a.get("rotula"):
        palabras = r"\separaPalabras ".join(_sin_cortes(p) for p in a["rotula"])
        abajo += r"{\bfseries\lblIngRotula\par}" + "\n" + r"\palabrasIng{" + palabras + "}\n"
    items = "\n".join(rf"\item {escapar(c)}" for c in comprueba)
    abajo += (
        r"{\bfseries\lblIngCompruebaDibujo\par}" + "\n"
        + "\\begin{listaComprueba}\n" + items + "\n\\end{listaComprueba}"
    )
    return _caja("dibuja", arriba, abajo, a)


def render_colorea(num, a, contexto):
    """Read and colour: un dibujo de línea (diagrams/english/) y el texto
    dice de qué color es cada parte."""
    campos_requeridos(num, a, ["prompt", "dibujo", "clave"])
    arriba = _instruccion(escapar(a["prompt"])) + "\n" + _dibujo(num, a["dibujo"])
    return _caja("colorea", arriba, "", a)


def render_donde(num, a, contexto):
    """Where is it?: una escena (una habitación, el jardín...) y el texto
    dice dónde está cada cosa -- in, on, under, next to, behind,
    between. La lista dice QUÉ hay que dibujar, nunca dónde."""
    campos_requeridos(num, a, ["prompt", "escena", "cosas", "clave"])
    cosas = a["cosas"]
    if not 2 <= len(cosas) <= 4:
        raise ErrorDeContenido(f"día {num}: donde necesita entre 2 y 4 'cosas'")
    lista = r"\separaPalabras ".join(_sin_cortes(c) for c in cosas)
    arriba = (
        _instruccion(escapar(a["prompt"])) + "\n"
        + r"{\bfseries\lblIngDibujaEsto}\ " + lista + "\\par\n"
        + _dibujo(num, a["escena"])
    )
    return _caja("donde", arriba, "", a)


def render_si_no(num, a, contexto):
    campos_requeridos(num, a, ["afirmaciones", "respuestas"])
    afirmaciones, respuestas = a["afirmaciones"], a["respuestas"]
    if not 3 <= len(afirmaciones) <= 5 or len(respuestas) != len(afirmaciones):
        raise ErrorDeContenido(
            f"día {num}: si_no necesita 3-5 frases y una respuesta por frase"
        )
    if any(r not in ("yes", "no") for r in respuestas):
        raise ErrorDeContenido(f"día {num}: cada respuesta de si_no es 'yes' o 'no'")
    if len(set(respuestas)) == 1:
        raise ErrorDeContenido(
            f"día {num}: si_no con todas las respuestas iguales -- mezcla 'yes' y 'no'"
        )
    filas = "\n".join(rf"\filaSiNo{{{escapar(af)}}}" for af in afirmaciones)
    return _caja("si_no", _instruccion(r"\lblIngInstruccionSiNo") + "\n" + filas, "", a)


def render_rodea(num, a, contexto):
    campos_requeridos(num, a, ["preguntas"])
    preguntas = a["preguntas"]
    if not 2 <= len(preguntas) <= 4:
        raise ErrorDeContenido(f"día {num}: rodea necesita entre 2 y 4 preguntas")
    bloques = []
    for i, p in enumerate(preguntas, start=1):
        campos_requeridos(num, p, ["pregunta", "opciones", "solucion"])
        if not 2 <= len(p["opciones"]) <= 3:
            raise ErrorDeContenido(
                f"día {num}: cada pregunta de rodea tiene 2 o 3 opciones"
            )
        if p["solucion"] not in p["opciones"]:
            raise ErrorDeContenido(
                f"día {num}: la solución {p['solucion']!r} no es una de las opciones"
            )
        # En una línea si caben, una debajo de otra si no: lo decide
        # \opcionesRodea (preamble-english.tex), que mide la línea de verdad.
        en_linea = r"\separaOpciones ".join(escapar(o) for o in p["opciones"])
        en_lista = r"\par ".join(escapar(o) for o in p["opciones"])
        bloques.append(
            rf"\preguntaNumerada{{{i}}}{{{escapar(p['pregunta'])}}}"
            + "\n" + rf"\opcionesRodea{{{en_linea}}}{{{en_lista}}}"
        )
    arriba = _instruccion(r"\lblIngInstruccionRodea") + "\n" + "\n".join(bloques)
    return _caja("rodea", arriba, "", a)


def render_relaciona(num, a, contexto):
    campos_requeridos(num, a, ["pares"])
    pares = a["pares"]
    if not 3 <= len(pares) <= 5:
        raise ErrorDeContenido(f"día {num}: relaciona necesita entre 3 y 5 pares")
    izquierda = [p[0] for p in pares]
    derecha = _barajar(num, [p[1] for p in pares])
    instruccion = escapar(a["instruccion"]) if a.get("instruccion") else r"\lblIngInstruccionRelaciona"
    return _caja("relaciona", _instruccion(instruccion) + "\n" + _tabla_une(izquierda, derecha), "", a)


def render_mitades(num, a, contexto):
    """Match the halves: frases compuestas del texto, partidas por el
    nexo (because, when, who, but...), para volver a unirlas."""
    campos_requeridos(num, a, ["mitades"])
    mitades = a["mitades"]
    if not 3 <= len(mitades) <= 4:
        raise ErrorDeContenido(f"día {num}: mitades necesita 3 o 4 frases")
    semana = _normalizar(contexto["texto_semana"])
    for primera, segunda in mitades:
        frase = f"{primera} {segunda}"
        if _normalizar(frase) not in semana:
            raise ErrorDeContenido(
                f"día {num}: la frase «{frase}» no está tal cual en los textos "
                "de esta semana -- tiene que poder encontrarse leyendo"
            )
    izquierda = [m[0] for m in mitades]
    derecha = _barajar(num, [m[1] for m in mitades])
    arriba = _instruccion(r"\lblIngInstruccionMitades") + "\n" + _tabla_une(izquierda, derecha)
    return _caja("mitades", arriba, "", a)


def render_ordena(num, a, contexto):
    campos_requeridos(num, a, ["sucesos"])
    sucesos = a["sucesos"]
    if not 3 <= len(sucesos) <= 4:
        raise ErrorDeContenido(f"día {num}: ordena necesita 3 o 4 sucesos")
    filas = "\n".join(
        rf"\item \casillaNumero\ {escapar(s)}" for s in _barajar(num, sucesos)
    )
    # "Put the story in order", salvo que el día pida otra cosa (una
    # receta, unas instrucciones: "Put the recipe in order...").
    if a.get("instruccion"):
        instruccion = escapar(a["instruccion"])
    else:
        instruccion = rf"\lblIngInstruccionOrdena{{{_y(range(1, len(sucesos) + 1))}}}"
    arriba = (
        _instruccion(instruccion)
        + "\n\\begin{listaOrdena}\n" + filas + "\n\\end{listaOrdena}"
    )
    return _caja("ordena", arriba, "", a)


HUECO = "___"


def render_huecos(num, a, contexto):
    """Frases del texto con una palabra menos, y una caja con las
    palabras que faltan (y, si se quiere, alguna que sobra)."""
    campos_requeridos(num, a, ["frases", "soluciones"])
    frases, soluciones = a["frases"], a["soluciones"]
    extra = a.get("extra", [])
    if not 3 <= len(frases) <= 4 or len(soluciones) != len(frases):
        raise ErrorDeContenido(
            f"día {num}: huecos necesita 3 o 4 frases y una solución por frase"
        )
    semana = _normalizar(contexto["texto_semana"])
    for frase, solucion in zip(frases, soluciones):
        if frase.count(HUECO) != 1:
            raise ErrorDeContenido(
                f"día {num}: la frase «{frase}» tiene que tener un hueco ({HUECO})"
            )
        completa = frase.replace(HUECO, solucion)
        if _normalizar(completa) not in semana:
            raise ErrorDeContenido(
                f"día {num}: la frase «{completa}» no está tal cual en los textos "
                "de esta semana -- tiene que poder encontrarse leyendo"
            )
    caja = soluciones + extra
    if len(set(caja)) != len(caja):
        raise ErrorDeContenido(
            f"día {num}: palabras repetidas en la caja de huecos -- cada palabra, una vez"
        )
    palabras = r"\separaPalabras ".join(_sin_cortes(p) for p in _barajar(num, sorted(caja)))
    filas = []
    for i, frase in enumerate(frases, start=1):
        antes, despues = frase.split(HUECO)
        filas.append(
            rf"\preguntaNumerada{{{i}}}{{{escapar(antes)}\huecoIng{{}}{escapar(despues)}}}"
        )
    arriba = (
        _instruccion(r"\lblIngInstruccionHuecos") + "\n"
        + r"\palabrasIng{" + palabras + "}\n" + "\n\\separaFrases\n".join(filas)
    )
    return _caja("huecos", arriba, "", a)


def render_busca(num, a, contexto):
    """Word hunt: buscar en el texto del día palabras de un tipo (dos
    colores, tres animales...) y escribirlas."""
    campos_requeridos(num, a, ["instruccion", "soluciones"])
    soluciones = a["soluciones"]
    if not 2 <= len(soluciones) <= 4:
        raise ErrorDeContenido(f"día {num}: busca necesita entre 2 y 4 soluciones")
    palabras_dia = {
        p.lower().split("'")[0] for p in PATRON_PALABRA.findall(contexto["texto_dia"])
    }
    for s in soluciones:
        if s.lower() not in palabras_dia:
            raise ErrorDeContenido(
                f"día {num}: la palabra «{s}» no está en el texto de hoy"
            )
    renglones = "\n".join(
        rf"\renglonNumerado{{{i}}}" for i in range(1, len(soluciones) + 1)
    )
    return _caja("busca", _instruccion(escapar(a["instruccion"])) + "\n" + renglones, "", a)


def render_adivina(num, a, contexto):
    campos_requeridos(num, a, ["adivinanza", "respuesta"])
    lineas = r"\\ ".join(escapar(t) for t in a["adivinanza"].split("\n"))
    arriba = (
        r"{\fontsize{18}{25}\selectfont " + lineas + r"\par}\vspace{3mm}" + "\n"
        + _instruccion(r"\lblIngDibujaRespuesta")
    )
    abajo = r"\lblIngRespuestaAdivina\ \renglonCorto"
    return _caja("adivina", arriba, abajo, a)


def render_vinetas(num, a, contexto):
    """Draw the story: tres recuadros para los tres momentos de la
    historia de la semana (principio, medio y final)."""
    campos_requeridos(num, a, ["instruccion", "pies"])
    pies = a["pies"]
    if len(pies) != 3:
        raise ErrorDeContenido(f"día {num}: vinetas necesita exactamente 3 'pies'")
    celdas = " & ".join(
        rf"\vinetaIng{{{i}}}{{{escapar(p)}}}" for i, p in enumerate(pies, start=1)
    )
    arriba = (
        _instruccion(escapar(a["instruccion"])) + "\n"
        + "\\noindent\\begin{tabular}{@{}p{0.31\\linewidth}@{\\hspace{0.035\\linewidth}}"
        + "p{0.31\\linewidth}@{\\hspace{0.035\\linewidth}}p{0.31\\linewidth}@{}}\n"
        + celdas + "\n\\end{tabular}"
    )
    return _caja("vinetas", arriba, "", a)


def render_repasa(num, a, contexto):
    campos_requeridos(num, a, ["checklist", "prompt", "banner"])
    if not 2 <= len(a["checklist"]) <= 4:
        raise ErrorDeContenido(f"día {num}: repasa necesita entre 2 y 4 frases en 'checklist'")
    items = "\n".join(rf"\item {escapar(i)}" for i in a["checklist"])
    arriba = (
        _instruccion(r"\lblIngInstruccionRepasa") + "\n"
        + "\\begin{listaComprueba}\n" + items + "\n\\end{listaComprueba}\n"
        + "\\par\\vspace{4mm}\n" + _instruccion(escapar(a["prompt"]))
    )
    return _caja("repasa", arriba, "", a)


def render_crea(num, a, contexto):
    campos_requeridos(num, a, ["prompt"])
    lineas = a.get("lineas", 0)
    if not 0 <= lineas <= 3:
        raise ErrorDeContenido(f"día {num}: crea lleva de 0 a 3 'lineas'")
    abajo = "\n".join([r"\renglon"] * lineas)
    return _caja("crea", _instruccion(escapar(a["prompt"])), abajo, a)


RENDER = {
    "dibuja": render_dibuja,
    "colorea": render_colorea,
    "donde": render_donde,
    "si_no": render_si_no,
    "rodea": render_rodea,
    "relaciona": render_relaciona,
    "mitades": render_mitades,
    "ordena": render_ordena,
    "huecos": render_huecos,
    "busca": render_busca,
    "adivina": render_adivina,
    "vinetas": render_vinetas,
    "repasa": render_repasa,
    "crea": render_crea,
}


def render_actividad(num, actividad, contexto):
    tipo = actividad.get("tipo")
    if tipo not in RENDER:
        raise ErrorDeContenido(f"día {num}: tipo de actividad desconocido: {tipo!r}")
    return RENDER[tipo](num, actividad, contexto)


# ---------------------------------------------------------------------
# La página y la clave
# ---------------------------------------------------------------------

def pagina_dia(d, libro, semana):
    """La página entera de un día. `semana` son todos los días de su
    semana, en orden -- huecos y mitades comprueban que sus frases están
    en lo leído hasta hoy."""
    num = d["dia"]
    hasta_hoy = [x for x in semana if x["dia"] <= num]
    contexto = {
        "texto_semana": " ".join(texto_plano(x["texto"]) for x in hasta_hoy),
        "texto_dia": texto_plano(d["texto"]),
    }
    trimestre = d["trimestre"]
    return PLANTILLA_DIA.substitute(
        dia=num,
        semana=d["semana"],
        trimestre=trimestre,
        tema=escapar(d["tema"]),
        instruccion=libro.instruccion_lectura[trimestre],
        fuente=libro.fuente_trimestre[trimestre],
        texto=formatear_texto(d["texto"]),
        actividad=render_actividad(num, d["actividad"], contexto),
    )


def _numeradas(respuestas):
    return " ".join(f"{i}) {escapar(r)}" for i, r in enumerate(respuestas, start=1))


def _texto_clave(a):
    tipo = a["tipo"]
    if tipo in ("dibuja", "colorea", "donde"):
        return escapar(a["clave"])
    if tipo == "si_no":
        return _numeradas(a["respuestas"])
    if tipo == "rodea":
        return _numeradas(p["solucion"] for p in a["preguntas"])
    if tipo == "relaciona":
        return "; ".join(f"{escapar(i)} $\\rightarrow$ {escapar(j)}" for i, j in a["pares"])
    if tipo == "mitades":
        return _numeradas(f"{p} {s}" for p, s in a["mitades"])
    if tipo == "ordena":
        return _numeradas(a["sucesos"])
    if tipo == "huecos":
        return _numeradas(a["soluciones"])
    if tipo == "busca":
        return escapar(", ".join(a["soluciones"]))
    if tipo == "adivina":
        return escapar(a["respuesta"])
    return None


def entrada_clave(d):
    a = d["actividad"]
    texto = _texto_clave(a)
    if texto is None:
        return None
    return f"\\claveEntrada{{{d['dia']}}}{{{TITULO[a['tipo']]}}}{{{texto}}}\n"
