"""Nivel 3 ("Leo con lupa"): el texto en párrafos y las actividades de
análisis -- ver notes/04-nivel-lupa.md para el porqué de cada una.

tools/gen_days.py llama a este módulo cuando el libro es "Leo con lupa"
(`--libro lupa`) o «Czytam z lupą», el mismo cuaderno en polaco
(`--libro czytam`, ver notes/10-czytam-z-lupa.md): validar_texto()
comprueba el texto de un día, pagina_dia() genera su página entera (caja
de lectura + actividad) y entrada_clave() su línea en la clave de
respuestas. Lo poco que cambia de un idioma a otro está en IDIOMAS.

La diferencia con el cuaderno de frases (nivel 2) no es solo de longitud: aquí cada
actividad obliga a volver al texto y analizarlo -- dibujar exactamente
lo que describe (dónde está cada cosa, cuántas hay, de qué color),
resolver un caso con las pistas repartidas por la semana, completar
una tabla lógica, seguir unas indicaciones en un mapa, cazar los
errores de un resumen equivocado, descifrar un mensaje... Por eso casi
todas las actividades llevan su solución en el JSON, y por eso las que
se pueden comprobar a máquina se comprueban aquí antes de generar nada:

  - logica: la tabla tiene UNA sola solución con las restricciones
    dadas, y es la que dice el JSON (fuerza bruta sobre todas las
    permutaciones -- 3x3 o 4x4, es instantáneo);
  - mapa: las casillas existen, no se repiten, y cada ruta de
    "comprobar" llega de verdad a la casilla que dice la solución;
  - errores: cada palabra equivocada está en el resumen falso, y cada
    corrección está en los textos de la semana (la respuesta sale del
    texto, no de la imaginación de quien escribió la actividad);
  - caso: la solución es una de las opciones que se ofrecen;
  - codigo: el mensaje se cifra aquí, no a mano, así que no puede
    llevar una errata que lo haga indescifrable.

Una página de cuento con una adivinanza sin solución, o un mapa que no
lleva a ninguna parte, es exactamente el tipo de error que un adulto no
detecta hasta que la niña se atasca delante del cuaderno.
"""

import itertools
import random
import re
import unicodedata
from string import Template

from comun import ErrorDeContenido, campos_requeridos, escapar

# ---------------------------------------------------------------------
# Lo que cambia de un idioma a otro (Libro.idioma)
# ---------------------------------------------------------------------
#
# El abecedario del mensaje secreto -- en polaco, las 32 letras de su
# abecedario, con ą, ć, ę, ł, ń, ó, ś, ź, ż y sin q, v ni x -- y el
# código de las vocales (en polaco, las nueve: a, ą, e, ę, i, o, ó, u,
# y), la «y» de «1, 2 y 3», las letras de verdadero y falso (las de
# \lblVerdadero y \lblFalso en lang/), la comilla que cierra una cita
# al final de un párrafo, la instrucción de "Relaciona" cuando el día no
# trae la suya y las palabras de la clave de "Compara". Todo lo demás
# (las instrucciones fijas, los títulos) son macros de lang/<idioma>.tex.
IDIOMAS = {
    "es": {
        "alfabeto": "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ",
        "vocales": {"A": "1", "E": "2", "I": "3", "O": "4", "U": "5"},
        "y": " y ",
        "verdadero": "V",
        "falso": "F",
        "cierre_cita": "»",
        "relaciona": "Une con una línea cada cosa con la que le corresponde.",
        "compara_solo": "Solo {}",
        "compara_ambos": "Los dos",
    },
    "pl": {
        "alfabeto": "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ",
        "vocales": {
            "A": "1", "Ą": "2", "E": "3", "Ę": "4", "I": "5", "O": "6",
            "Ó": "7", "U": "8", "Y": "9",
        },
        "y": " i ",
        "verdadero": "P",
        "falso": "F",
        "cierre_cita": "”",
        "relaciona": "Połącz linią pary, które do siebie pasują.",
        # «Psy: ... Wspólne: ... Koty: ...»: el nombre de cada lado, tal
        # cual, al principio de su frase -- «Tylko Psy» llevaría una
        # mayúscula en medio de la frase.
        "compara_solo": "{}",
        "compara_ambos": "Wspólne",
    },
}


def idioma_de(libro):
    """Los datos de IDIOMAS del idioma de un libro; sin libro, el
    español, el de "Leo con lupa"."""
    return IDIOMAS[libro.idioma if libro is not None else "es"]

# ---------------------------------------------------------------------
# El texto del día
# ---------------------------------------------------------------------
#
# "texto" es una lista de párrafos. Marcas, al principio de un párrafo:
#   "—..."  diálogo, con raya (nunca comillas rectas): sangría francesa
#           si ocupa más de una línea, igual que en el cuaderno de frases.
#   "> ..." una nota, cartel, carta o mensaje que los personajes leen
#           dentro de la historia: va en un recuadro blanco aparte, para
#           que se vea que es "otro texto" dentro del texto.
#   "- ..." un elemento de lista (lista de la compra, normas del club,
#           pasos de una receta); los consecutivos forman una sola lista.
# Dentro de un párrafo, "\n" es un salto de línea (poemas, direcciones
# de una carta).

# Cómo puede acabar un párrafo: con un signo de final de frase, o con la
# comilla que cierra una cita (» en español, ” en polaco -- ver IDIOMAS).
FINALES_VALIDOS = (".", "!", "?", "…", ":")


def _lineas(texto):
    return r"\\ ".join(escapar(t) for t in texto.split("\n"))


def formatear_texto(parrafos):
    piezas = []
    lista = []

    def cerrar_lista():
        if lista:
            items = "\n".join(rf"\item {_lineas(i)}" for i in lista)
            piezas.append("\\begin{listaTexto}\n" + items + "\n\\end{listaTexto}")
            lista.clear()

    for parrafo in parrafos:
        if parrafo.startswith("- "):
            lista.append(parrafo[2:])
            continue
        cerrar_lista()
        if parrafo.startswith("> "):
            piezas.append(r"\notaTexto{" + _lineas(parrafo[2:]) + "}")
        elif parrafo.startswith("—"):
            piezas.append(r"\hangindent=4mm\hangafter=1 " + _lineas(parrafo))
        else:
            piezas.append(_lineas(parrafo))
    cerrar_lista()
    return "\\raggedright\n" + "\n\\separaParrafo\n".join(piezas)


def texto_plano(parrafos):
    """El texto del día sin marcas, para contar palabras y buscar dentro."""
    limpios = []
    for p in parrafos:
        if p.startswith(("> ", "- ")):
            p = p[2:]
        limpios.append(p.replace("\n", " "))
    return " ".join(limpios)


def _cadenas(valor):
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for v in valor.values():
            yield from _cadenas(v)
    elif isinstance(valor, list):
        for v in valor:
            yield from _cadenas(v)


def validar_texto(num, d, libro=None):
    finales = FINALES_VALIDOS + (idioma_de(libro)["cierre_cita"],)
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
        if parrafo.startswith(("- ", "> ")):
            continue
        if not parrafo.endswith(finales):
            raise ErrorDeContenido(
                f"día {num}: el párrafo «...{parrafo[-40:]}» no termina en un "
                "signo de puntuación final"
            )
    # Comillas rectas: ni en el texto ni en la actividad -- el diálogo va
    # con raya y las citas con «» (en polaco, con „”), como en los libros
    # infantiles de verdad (y la comilla recta es la que provocó el error
    # de babel documentado en preamble.tex).
    for cadena in _cadenas(d):
        if '"' in cadena:
            raise ErrorDeContenido(
                f"día {num}: comilla recta en «{cadena[:50]}...» -- usa raya "
                "para el diálogo y «» (en polaco, „”) para citar"
            )
        if "  " in cadena:
            raise ErrorDeContenido(
                f"día {num}: doble espacio en «{cadena[:50]}...»"
            )


# ---------------------------------------------------------------------
# Plantillas
# ---------------------------------------------------------------------

PLANTILLA_DIA = Template(
    r"""\begin{lupapagina}{$dia}{$semana}{$trimestre}{$tema}
\begin{cajaLectura}{$instruccion}
\fuenteLupa{$fuente}%
$texto
\end{cajaLectura}
\vspace{4mm}
$actividad
\end{lupapagina}
"""
)

# Todas las actividades de este cuaderno usan la misma caja (actividadLupa,
# ver preamble-lupa.tex): ocupa todo el alto que le queda a la página -- el
# espacio para dibujar o para pensar crece o encoge solo según lo largo
# que sea el texto de ese día, sin calcularlo a mano -- y lo que va
# después de \tcblower (la lista de comprobación de un dibujo, las
# líneas para escribir, el banner de las páginas leídas) se queda pegado
# al fondo de la caja.
PLANTILLA_ACTIVIDAD = Template(
    r"""\begin{actividadLupa}{$color}{$titulo}
$arriba
\tcblower
$abajo
\end{actividadLupa}"""
)

PLANTILLA_ACTIVIDAD_SIN_ABAJO = Template(
    r"""\begin{actividadLupa}{$color}{$titulo}
$arriba
\end{actividadLupa}"""
)

COLOR = {
    "dibuja_detalle": "colorDibuja",
    "vinetas": "colorDibuja",
    "mapa": "colorRelaciona",
    "logica": "colorRelaciona",
    "caso": "colorRelaciona",
    "codigo": "colorRelaciona",
    "adivina": "colorRelaciona",
    "relaciona": "colorRelaciona",
    "errores": "colorResponde",
    "verdadero_falso": "colorResponde",
    "responde": "colorResponde",
    "ordena": "colorResponde",
    "ficha": "colorResponde",
    "compara": "colorResponde",
    "crea": "colorCrea",
    "repasa": "colorCrea",
}

TITULO = {
    "dibuja_detalle": r"\lblDibujaConLupa",
    "vinetas": r"\lblVinetas",
    "mapa": r"\lblMapa",
    "logica": r"\lblLogica",
    "caso": r"\lblCaso",
    "codigo": r"\lblCodigo",
    "adivina": r"\lblAdivina",
    "relaciona": r"\lblRelaciona",
    "errores": r"\lblErrores",
    "verdadero_falso": r"\lblVerdaderoFalso",
    "responde": r"\lblResponde",
    "ordena": r"\lblOrdena",
    "ficha": r"\lblFicha",
    "compara": r"\lblCompara",
    "crea": r"\lblCrea",
    "repasa": r"\lblRepasa",
}


def _instruccion_adulto(texto):
    """Instrucción en pequeño y gris -- la lee el adulto, o la niña si
    quiere; lo que la niña TIENE que leer va siempre a tamaño normal."""
    return r"{\footnotesize\color{colorGris}" + texto + r"\par}\vspace{2mm}"


def _lineas_escribir(n):
    return "\n".join([r"\renglon"] * n)


def _banner(actividad):
    banner = actividad.get("banner")
    if not banner:
        return ""
    return r"\bannerDia{" + escapar(banner) + "}"


def _caja(tipo, arriba, abajo, actividad):
    banner = _banner(actividad)
    if banner:
        abajo = (abajo + "\n" if abajo else "") + banner
    if not abajo:
        return PLANTILLA_ACTIVIDAD_SIN_ABAJO.substitute(
            color=COLOR[tipo], titulo=TITULO[tipo], arriba=arriba
        )
    return PLANTILLA_ACTIVIDAD.substitute(
        color=COLOR[tipo], titulo=TITULO[tipo], arriba=arriba, abajo=abajo
    )


def _lista_numerada(elementos):
    items = "\n".join(rf"\item {escapar(e)}" for e in elementos)
    return "\\begin{listaNumerada}\n" + items + "\n\\end{listaNumerada}"


def _y(elementos, idioma=IDIOMAS["es"]):
    """['1', '2', '3'] -> '1, 2 y 3' (en polaco, '1, 2 i 3')."""
    elementos = [str(e) for e in elementos]
    if len(elementos) == 1:
        return elementos[0]
    return ", ".join(elementos[:-1]) + idioma["y"] + elementos[-1]


# ---------------------------------------------------------------------
# Un render por tipo de actividad
# ---------------------------------------------------------------------

def render_dibuja_detalle(num, a, contexto):
    campos_requeridos(num, a, ["prompt", "comprueba", "clave"])
    comprueba = a["comprueba"]
    if not 2 <= len(comprueba) <= 5:
        raise ErrorDeContenido(
            f"día {num}: dibuja_detalle necesita entre 2 y 5 preguntas en 'comprueba'"
        )
    items = "\n".join(rf"\item {escapar(c)}" for c in comprueba)
    arriba = escapar(a["prompt"])
    abajo = (
        r"{\bfseries\lblCompruebaDibujo\par}" + "\n"
        + "\\begin{listaRepaso}\n" + items + "\n\\end{listaRepaso}"
    )
    return _caja("dibuja_detalle", arriba, abajo, a)


def render_vinetas(num, a, contexto):
    campos_requeridos(num, a, ["instruccion", "pies"])
    pies = a["pies"]
    if len(pies) != 3:
        raise ErrorDeContenido(f"día {num}: vinetas necesita exactamente 3 'pies'")
    celdas = " & ".join(
        rf"\vineta{{{i}}}{{{escapar(p)}}}" for i, p in enumerate(pies, start=1)
    )
    arriba = (
        escapar(a["instruccion"]) + "\n\\par\\vspace{3mm}\n"
        + "\\noindent\\begin{tabular}{@{}p{0.31\\linewidth}@{\\hspace{0.035\\linewidth}}"
        + "p{0.31\\linewidth}@{\\hspace{0.035\\linewidth}}p{0.31\\linewidth}@{}}\n"
        + celdas + "\n\\end{tabular}"
    )
    return _caja("vinetas", arriba, "", a)


# --- mapa ------------------------------------------------------------

LETRAS_COLUMNA = "ABCDEFG"
PATRON_CASILLA = re.compile(r"^([A-G])([1-6])$")
DIRECCIONES = {
    "derecha": (1, 0),
    "izquierda": (-1, 0),
    "arriba": (0, -1),
    "abajo": (0, 1),
}


def _casilla(num, texto, columnas, filas):
    m = PATRON_CASILLA.match(texto or "")
    if not m:
        raise ErrorDeContenido(f"día {num}: casilla de mapa inválida: {texto!r}")
    col = LETRAS_COLUMNA.index(m.group(1))
    fila = int(m.group(2)) - 1
    if col >= columnas or fila >= filas:
        raise ErrorDeContenido(
            f"día {num}: la casilla {texto} se sale de un mapa de "
            f"{columnas}x{filas}"
        )
    return col, fila


def _nombre_casilla(col, fila):
    return f"{LETRAS_COLUMNA[col]}{fila + 1}"


def seguir_ruta(num, desde, pasos, columnas, filas):
    """Casilla a la que se llega desde `desde` siguiendo `pasos`
    ("derecha", "abajo 2"...). Falla si la ruta se sale del mapa."""
    col, fila = _casilla(num, desde, columnas, filas)
    for paso in pasos:
        partes = paso.split()
        direccion = partes[0]
        veces = int(partes[1]) if len(partes) > 1 else 1
        if direccion not in DIRECCIONES or len(partes) > 2:
            raise ErrorDeContenido(f"día {num}: paso de ruta inválido: {paso!r}")
        dx, dy = DIRECCIONES[direccion]
        for _ in range(veces):
            col, fila = col + dx, fila + dy
            if not (0 <= col < columnas and 0 <= fila < filas):
                raise ErrorDeContenido(
                    f"día {num}: la ruta desde {desde} se sale del mapa en el paso {paso!r}"
                )
    return _nombre_casilla(col, fila)


def render_mapa(num, a, contexto):
    campos_requeridos(num, a, ["instruccion", "columnas", "filas", "lugares", "clave"])
    columnas, filas = a["columnas"], a["filas"]
    if not (3 <= columnas <= 7 and 3 <= filas <= 6):
        raise ErrorDeContenido(f"día {num}: el mapa tiene que ser de 3x3 a 7x6 casillas")

    ocupadas = {}
    for casilla, nombre in a["lugares"].items():
        pos = _casilla(num, casilla, columnas, filas)
        ocupadas[pos] = nombre
    salida = a.get("salida")
    if salida:
        pos_salida = _casilla(num, salida, columnas, filas)

    for ruta in a.get("comprobar", []):
        llega = seguir_ruta(num, ruta["desde"], ruta["pasos"], columnas, filas)
        if llega != ruta["hasta"]:
            raise ErrorDeContenido(
                f"día {num}: la ruta desde {ruta['desde']} ({', '.join(ruta['pasos'])}) "
                f"llega a {llega}, no a {ruta['hasta']}"
            )

    ancho = min(2.4, 14.4 / columnas)
    alto = min(1.5, 7.2 / filas)
    nodos = []
    celdas = {pos: escapar(nombre) for pos, nombre in ocupadas.items()}
    if salida:
        # La salida no es una etiqueta aparte en una esquina (se pisaría
        # con el nombre del sitio): va encima del nombre, en la misma
        # casilla, en negrita y en el color de la caja.
        previo = celdas.get(pos_salida)
        celdas[pos_salida] = r"{\salidaMapa}" + (r"\\ " + previo if previo else "")
    # Una palabra que no cabe en el ancho de la casilla no se parte (no
    # hay guiones para una niña de 7 años): la etiqueta entera baja un
    # tamaño de letra, y si ni así cabe, es un error de contenido -- mejor
    # una etiqueta más corta que una caja desbordada.
    for (col, fila), nombre in sorted(ocupadas.items()):
        mas_larga = max(len(p) for p in nombre.split())
        if mas_larga > 5.5 * (ancho - 0.2):
            raise ErrorDeContenido(
                f"día {num}: la etiqueta de mapa {nombre!r} no cabe en una casilla "
                f"de {ancho:.1f} cm -- usa una palabra más corta"
            )
    for (col, fila), texto in sorted(celdas.items()):
        nombre = ocupadas.get((col, fila), "")
        pequena = bool(nombre) and max(len(p) for p in nombre.split()) > 4.5 * (ancho - 0.2)
        estilo = "lugarMapa, font=\\footnotesize" if pequena else "lugarMapa"
        nodos.append(
            rf"\node[{estilo}, text width={ancho - 0.2:.2f}cm] at ({col + 0.5},{fila + 0.5}) "
            rf"{{{texto}}};"
        )
    etiquetas_col = " ".join(
        rf"\node[etiquetaMapa] at ({c + 0.5},-0.28) {{{LETRAS_COLUMNA[c]}}};"
        for c in range(columnas)
    )
    etiquetas_fila = " ".join(
        rf"\node[etiquetaMapa] at (-0.22,{f + 0.5}) {{{f + 1}}};" for f in range(filas)
    )
    lineas_v = " ".join(rf"\draw[lineaMapa] ({c},0) -- ({c},{filas});" for c in range(columnas + 1))
    lineas_h = " ".join(rf"\draw[lineaMapa] (0,{f}) -- ({columnas},{f});" for f in range(filas + 1))
    tikz = (
        rf"\begin{{tikzpicture}}[x={ancho:.2f}cm, y=-{alto:.2f}cm]" + "\n"
        + lineas_v + "\n" + lineas_h + "\n" + etiquetas_col + "\n" + etiquetas_fila + "\n"
        + "\n".join(nodos) + "\n\\end{tikzpicture}"
    )
    arriba = (
        escapar(a["instruccion"]) + "\n\\par\\vspace{2mm}\n"
        + "\\begin{center}\n" + tikz + "\n\\end{center}"
    )
    preguntas = a.get("preguntas", [])
    abajo = "\n".join(
        rf"{escapar(p)}\par\renglon\par\vspace{{1mm}}" for p in preguntas
    )
    return _caja("mapa", arriba, abajo, a)


# --- logica ----------------------------------------------------------

def resolver_logica(filas, columnas, restricciones):
    """Todas las asignaciones fila -> columna (una columna distinta por
    fila) que cumplen las restricciones."""
    soluciones = []
    for perm in itertools.permutations(columnas, len(filas)):
        asignacion = dict(zip(filas, perm))
        if all(_cumple(asignacion, r) for r in restricciones):
            soluciones.append(asignacion)
    return soluciones


def _cumple(asignacion, restriccion):
    tipo = restriccion[0]
    if tipo == "si":
        return asignacion[restriccion[1]] == restriccion[2]
    if tipo == "no":
        return asignacion[restriccion[1]] != restriccion[2]
    if tipo == "uno_de":
        return asignacion[restriccion[1]] in restriccion[2]
    raise AssertionError("validado antes de llamar")


def validar_logica(num, a):
    filas, columnas = a["filas"], a["columnas"]
    if len(filas) != len(columnas) or not 3 <= len(filas) <= 4:
        raise ErrorDeContenido(
            f"día {num}: logica necesita tantas filas como columnas (3 o 4)"
        )
    for r in a["restricciones"]:
        if r[0] not in ("si", "no", "uno_de") or len(r) != 3:
            raise ErrorDeContenido(f"día {num}: restricción inválida: {r!r}")
        if r[1] not in filas:
            raise ErrorDeContenido(f"día {num}: {r[1]!r} no es una fila de la tabla")
        opciones = r[2] if r[0] == "uno_de" else [r[2]]
        for o in opciones:
            if o not in columnas:
                raise ErrorDeContenido(f"día {num}: {o!r} no es una columna de la tabla")
    soluciones = resolver_logica(filas, columnas, a["restricciones"])
    if len(soluciones) != 1:
        raise ErrorDeContenido(
            f"día {num}: la tabla lógica tiene {len(soluciones)} soluciones con "
            "estas pistas -- tiene que tener exactamente una"
        )
    if soluciones[0] != a["solucion"]:
        raise ErrorDeContenido(
            f"día {num}: la única solución de la tabla es {soluciones[0]}, "
            f"no {a['solucion']}"
        )


def render_logica(num, a, contexto):
    campos_requeridos(num, a, ["instruccion", "filas", "columnas", "restricciones", "solucion"])
    validar_logica(num, a)
    filas, columnas = a["filas"], a["columnas"]
    ancho_col = {3: "2.9cm", 4: "2.35cm"}[len(columnas)]
    cabecera = " & ".join(rf"\cabeceraLogica{{{escapar(c)}}}" for c in columnas)
    cuerpo = "\n".join(
        escapar(f) + " & " + " & ".join([r"\celdaLogica"] * len(columnas)) + r" \\ \hline"
        for f in filas
    )
    tabla = (
        "\\begin{center}\n"
        + rf"\begin{{tabular}}{{|>{{\bfseries}}l|*{{{len(columnas)}}}{{>{{\centering\arraybackslash}}p{{{ancho_col}}}|}}}}"
        + "\n\\hline\n & " + cabecera + r" \\ \hline" + "\n" + cuerpo
        + "\n\\end{tabular}\n\\end{center}"
    )
    partes = [escapar(a["instruccion"])]
    if a.get("pistas"):
        partes.append(_lista_numerada(a["pistas"]))
    partes.append(tabla)
    arriba = "\n\\par\\vspace{2mm}\n".join(partes)
    abajo = ""
    if a.get("pregunta"):
        abajo = escapar(a["pregunta"]) + r"\par\renglon"
    return _caja("logica", arriba, abajo, a)


# --- caso ------------------------------------------------------------

def render_caso(num, a, contexto):
    campos_requeridos(num, a, ["pregunta", "opciones", "solucion", "clave"])
    opciones = a["opciones"]
    if not 2 <= len(opciones) <= 5:
        raise ErrorDeContenido(f"día {num}: caso necesita entre 2 y 5 opciones")
    if a["solucion"] not in opciones:
        raise ErrorDeContenido(
            f"día {num}: la solución del caso ({a['solucion']!r}) no es una de las opciones"
        )
    lineas = a.get("lineas", 3)
    arriba = (
        r"{\bfseries " + escapar(a["pregunta"]) + r"\par}\vspace{2mm}" + "\n"
        + _instruccion_adulto(r"\lblInstruccionCaso") + "\n"
        + "\\begin{center}\n"
        + r"\hspace{12mm plus 6mm}".join(rf"\opcionCaso{{{escapar(o)}}}" for o in opciones)
        + "\n\\end{center}"
    )
    abajo = r"{\bfseries\lblPistasCaso\par}" + "\n" + _lineas_escribir(lineas)
    return _caja("caso", arriba, abajo, a)


# --- errores ---------------------------------------------------------

def _normalizar_busqueda(texto):
    return " ".join(texto.lower().split())


def render_errores(num, a, contexto):
    campos_requeridos(num, a, ["instruccion", "relato", "errores"])
    relato = a["relato"]
    errores = a["errores"]
    if not 2 <= len(errores) <= 4:
        raise ErrorDeContenido(f"día {num}: errores necesita entre 2 y 4 errores")
    relato_n = _normalizar_busqueda(relato)
    semana_n = _normalizar_busqueda(contexto["texto_semana"])
    for mal, bien in errores:
        if _normalizar_busqueda(mal) not in relato_n:
            raise ErrorDeContenido(
                f"día {num}: el error {mal!r} no aparece en el resumen equivocado"
            )
        if _normalizar_busqueda(bien) not in semana_n:
            raise ErrorDeContenido(
                f"día {num}: la corrección {bien!r} no aparece en los textos de "
                "esta semana -- la respuesta tiene que poder encontrarse leyendo"
            )
    arriba = (
        escapar(a["instruccion"]) + "\n\\par\\vspace{2mm}\n"
        + r"\relatoErrores{" + escapar(relato) + "}"
    )
    lineas = "\n".join(
        rf"\renglonNumerado{{{i}}}" for i in range(1, len(errores) + 1)
    )
    abajo = r"{\bfseries\lblCorrigeErrores\par}" + "\n" + lineas
    return _caja("errores", arriba, abajo, a)


# --- codigo ----------------------------------------------------------

def normalizar_mensaje(mensaje, alfabeto=IDIOMAS["es"]["alfabeto"]):
    """Mayúsculas, solo letras y espacios, y sin tildes, salvo en las
    letras que son del abecedario: la Ñ en español; en polaco, Ą, Ć, Ę,
    Ł, Ń, Ó, Ś, Ź y Ż (y "Lucía" se queda en LUCIA)."""
    salida = []
    for c in mensaje.upper():
        if c in alfabeto:
            salida.append(c)
            continue
        base = unicodedata.normalize("NFD", c)[0]
        salida.append(base)
    return "".join(salida)


def render_codigo(num, a, contexto):
    campos_requeridos(num, a, ["instruccion", "mensaje", "cifrado"])
    alfabeto = contexto["idioma"]["alfabeto"]
    vocales = contexto["idioma"]["vocales"]
    mensaje = normalizar_mensaje(a["mensaje"], alfabeto)
    if any(c not in alfabeto and c != " " for c in mensaje):
        raise ErrorDeContenido(
            f"día {num}: el mensaje secreto solo puede llevar letras y espacios"
        )
    palabras = mensaje.split()
    cifrado = a["cifrado"]
    partes = [escapar(a["instruccion"])]

    if cifrado == "numeros":
        if len(mensaje.replace(" ", "")) > 26:
            raise ErrorDeContenido(
                f"día {num}: mensaje demasiado largo para el cifrado de números (máx. 26 letras)"
            )
        if a.get("mostrar_clave", True):
            # La tabla, en dos filas: las 27 letras del español en filas de
            # 14 (la columna que sobra, vacía), las 32 del polaco en filas
            # de 16 -- \begin{tablaCodigo}[16], ver preamble-lupa.tex.
            ancho = (len(alfabeto) + 1) // 2
            filas_tabla = []
            for mitad in (alfabeto[:ancho], alfabeto[ancho:]):
                letras = [rf"\textbf{{{c}}}" for c in mitad]
                numeros = [str(alfabeto.index(c) + 1) for c in mitad]
                relleno = [""] * (ancho - len(mitad))
                filas_tabla.append(" & ".join(letras + relleno) + r" \\")
                filas_tabla.append(" & ".join(numeros + relleno) + r" \\ \hline")
            columnas = "" if ancho == 14 else f"[{ancho}]"
            partes.append(
                "\\begin{center}\\begin{tablaCodigo}" + columnas + "\n\\hline\n"
                + "\n".join(filas_tabla)
                + "\n\\end{tablaCodigo}\\end{center}"
            )
        grupos = []
        for p in palabras:
            celdas = "".join(rf"\celdaCodigo{{{alfabeto.index(c) + 1}}}" for c in p)
            grupos.append(r"\mbox{" + celdas + "}")
        partes.append(
            "\\begin{center}\n" + r"\hspace{7mm plus 3mm}".join(grupos) + "\n\\end{center}"
        )
        abajo = ""
    elif cifrado == "vocales":
        cifrada = " ".join(
            "".join(vocales.get(c, c) for c in p) for p in palabras
        )
        if a.get("mostrar_clave", False):
            partes.append(
                r"\begin{center}\large "
                + r" \quad ".join(f"{v} = {n}" for v, n in vocales.items())
                + r"\end{center}"
            )
        partes.append(r"\mensajeCifrado{" + escapar(cifrada) + "}")
        abajo = _lineas_escribir(2)
    elif cifrado == "reves":
        cifrada = " ".join(p[::-1] for p in palabras)
        partes.append(r"\mensajeCifrado{" + escapar(cifrada) + "}")
        abajo = _lineas_escribir(2)
    else:
        raise ErrorDeContenido(f"día {num}: cifrado desconocido: {cifrado!r}")

    arriba = "\n\\par\\vspace{2mm}\n".join(partes)
    return _caja("codigo", arriba, abajo, a)


# --- ficha, compara --------------------------------------------------

def render_ficha(num, a, contexto):
    campos_requeridos(num, a, ["instruccion", "titulo", "campos", "respuestas"])
    if len(a["campos"]) != len(a["respuestas"]):
        raise ErrorDeContenido(f"día {num}: ficha necesita una respuesta por campo")
    campos = "\n".join(rf"\campoFicha{{{escapar(c)}}}" for c in a["campos"])
    arriba = (
        escapar(a["instruccion"]) + "\n\\par\\vspace{3mm}\n"
        + r"{\Large\bfseries " + escapar(a["titulo"]) + r"\par}" + "\n" + campos
    )
    return _caja("ficha", arriba, "", a)


def render_compara(num, a, contexto):
    campos_requeridos(num, a, ["instruccion", "a", "b", "solucion"])
    sol = a["solucion"]
    if set(sol) != {"a", "ambos", "b"}:
        raise ErrorDeContenido(
            f"día {num}: la solución de compara necesita 'a', 'ambos' y 'b'"
        )
    arriba = (
        escapar(a["instruccion"]) + "\n\\par\\vspace{2mm}\n"
        + rf"\diagramaCompara{{{escapar(a['a'])}}}{{{escapar(a['b'])}}}"
    )
    return _caja("compara", arriba, "", a)


# --- los tipos del cuaderno de frases, con más campos ----------------

def render_responde(num, a, contexto):
    campos_requeridos(num, a, ["preguntas", "respuestas"])
    preguntas = a["preguntas"]
    if not 1 <= len(preguntas) <= 3 or len(a["respuestas"]) != len(preguntas):
        raise ErrorDeContenido(
            f"día {num}: responde necesita 1-3 preguntas y una respuesta modelo por pregunta"
        )
    lineas = a.get("lineas", 2)
    bloques = []
    for i, p in enumerate(preguntas, start=1):
        bloques.append(
            rf"\preguntaNumerada{{{i}}}{{{escapar(p)}}}" + "\n" + _lineas_escribir(lineas)
        )
    arriba = "\n\\par\\vspace{3mm}\n".join(bloques)
    return _caja("responde", arriba, "", a)


def render_ordena(num, a, contexto):
    campos_requeridos(num, a, ["sucesos"])
    sucesos = a["sucesos"]
    if not 3 <= len(sucesos) <= 6:
        raise ErrorDeContenido(f"día {num}: ordena necesita entre 3 y 6 sucesos")
    rng = random.Random(num)
    mezclados = sucesos[:]
    while mezclados == sucesos:
        rng.shuffle(mezclados)
    filas = "\n".join(rf"\item \casillaNumero\ {escapar(s)}" for s in mezclados)
    arriba = (
        _instruccion_adulto(
            rf"\lblLupaInstruccionOrdena{{{_y(range(1, len(sucesos) + 1), contexto['idioma'])}}}"
        )
        + "\n\\begin{listaOrdena}\n" + filas + "\n\\end{listaOrdena}"
    )
    return _caja("ordena", arriba, "", a)


def render_relaciona(num, a, contexto):
    campos_requeridos(num, a, ["pares"])
    pares = a["pares"]
    if not 3 <= len(pares) <= 5:
        raise ErrorDeContenido(f"día {num}: relaciona necesita entre 3 y 5 pares")
    izquierda = [p[0] for p in pares]
    derecha = [p[1] for p in pares]
    rng = random.Random(num)
    mezclada = derecha[:]
    while mezclada == derecha:
        rng.shuffle(mezclada)
    filas = " \\\\\n".join(
        f"{escapar(i)} & & {escapar(d)}" for i, d in zip(izquierda, mezclada)
    ) + " \\\\"
    cabeceras = ""
    if a.get("cabeceras"):
        c1, c2 = a["cabeceras"]
        cabeceras = rf"\bfseries {escapar(c1)} & & \bfseries {escapar(c2)} \\[-2mm]" + "\n"
    instruccion = escapar(a.get("instruccion", contexto["idioma"]["relaciona"]))
    arriba = (
        _instruccion_adulto(instruccion) + "\n"
        + r"\renewcommand{\arraystretch}{2.3}" + "\n"
        + r"\begin{tabularx}{\linewidth}{@{}X >{\centering\arraybackslash}p{2.4cm} X@{}}" + "\n"
        + cabeceras + filas + "\n\\end{tabularx}\n"
        + r"\renewcommand{\arraystretch}{1}"
    )
    return _caja("relaciona", arriba, "", a)


def render_verdadero_falso(num, a, contexto):
    campos_requeridos(num, a, ["afirmaciones", "respuestas"])
    afirmaciones, respuestas = a["afirmaciones"], a["respuestas"]
    if not 3 <= len(afirmaciones) <= 5 or len(respuestas) != len(afirmaciones):
        raise ErrorDeContenido(
            f"día {num}: verdadero_falso necesita 3-5 afirmaciones y una respuesta por afirmación"
        )
    # "V" o "F: corrección" -- en polaco, "P" (prawda) o "F" (fałsz), las
    # letras de las casillas (\lblVerdadero y \lblFalso en lang/pl.tex).
    verdadero, falso = contexto["idioma"]["verdadero"], contexto["idioma"]["falso"]
    for r in respuestas:
        if not (r == verdadero or r.startswith(falso)):
            raise ErrorDeContenido(
                f"día {num}: cada respuesta de verdadero_falso empieza por "
                f"{verdadero!r} o {falso!r}: {r!r}"
            )
    corrige = a.get("corrige", True)
    filas = []
    for af in afirmaciones:
        fila = rf"\afirmacionVF{{{escapar(af)}}}"
        if corrige:
            fila += r"\renglonCorrige"
        filas.append(fila)
    instruccion = r"\lblLupaInstruccionVerdaderoFalso" if corrige else r"\lblInstruccionVerdaderoFalso"
    arriba = _instruccion_adulto(instruccion) + "\n" + "\n".join(filas)
    return _caja("verdadero_falso", arriba, "", a)


def render_adivina(num, a, contexto):
    campos_requeridos(num, a, ["adivinanza", "respuesta"])
    arriba = r"{\Large " + _lineas(a["adivinanza"]) + r"\par}"
    abajo = r"\lblRespuesta:\ \renglonCorto"
    return _caja("adivina", arriba, abajo, a)


def render_crea(num, a, contexto):
    campos_requeridos(num, a, ["prompt"])
    lineas = a.get("lineas", 0)
    return _caja("crea", escapar(a["prompt"]), _lineas_escribir(lineas) if lineas else "", a)


def render_repasa(num, a, contexto):
    campos_requeridos(num, a, ["checklist", "prompt", "banner"])
    items = "\n".join(rf"\item {escapar(i)}" for i in a["checklist"])
    arriba = (
        "\\begin{listaRepaso}\n" + items + "\n\\end{listaRepaso}\n"
        + "\\par\\vspace{3mm}\n" + escapar(a["prompt"])
    )
    return _caja("repasa", arriba, "", a)


RENDER = {
    "dibuja_detalle": render_dibuja_detalle,
    "vinetas": render_vinetas,
    "mapa": render_mapa,
    "logica": render_logica,
    "caso": render_caso,
    "errores": render_errores,
    "codigo": render_codigo,
    "ficha": render_ficha,
    "compara": render_compara,
    "responde": render_responde,
    "ordena": render_ordena,
    "relaciona": render_relaciona,
    "verdadero_falso": render_verdadero_falso,
    "adivina": render_adivina,
    "crea": render_crea,
    "repasa": render_repasa,
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
    semana, en orden -- 'errores' comprueba que cada corrección está en
    lo leído hasta hoy."""
    num = d["dia"]
    hasta_hoy = [x for x in semana if x["dia"] <= num]
    contexto = {
        "texto_semana": " ".join(texto_plano(x["texto"]) for x in hasta_hoy),
        "idioma": idioma_de(libro),
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


def _texto_clave(a, idioma):
    tipo = a["tipo"]
    if tipo in ("dibuja_detalle", "mapa", "caso"):
        return escapar(a["clave"])
    if tipo == "logica":
        texto = "; ".join(f"{escapar(f)}: {escapar(c)}" for f, c in a["solucion"].items())
        if a.get("respuesta_pregunta"):
            texto += ". " + escapar(a["respuesta_pregunta"])
        return texto
    if tipo == "errores":
        return "; ".join(
            f"{escapar(mal)} $\\rightarrow$ {escapar(bien)}" for mal, bien in a["errores"]
        )
    if tipo == "codigo":
        return escapar(a["mensaje"])
    if tipo == "ficha":
        return "; ".join(
            f"{escapar(c)}: {escapar(r)}" for c, r in zip(a["campos"], a["respuestas"])
        )
    if tipo == "compara":
        s = a["solucion"]
        solo = idioma["compara_solo"]
        return (
            f"{solo.format(escapar(a['a']))}: {escapar(', '.join(s['a']))}. "
            f"{idioma['compara_ambos']}: {escapar(', '.join(s['ambos']))}. "
            f"{solo.format(escapar(a['b']))}: {escapar(', '.join(s['b']))}."
        )
    if tipo == "responde":
        return " ".join(f"{i}) {escapar(r)}" for i, r in enumerate(a["respuestas"], start=1))
    if tipo == "ordena":
        return " ".join(f"{i}) {escapar(s)}" for i, s in enumerate(a["sucesos"], start=1))
    if tipo == "relaciona":
        return "; ".join(f"{escapar(i)} $\\rightarrow$ {escapar(j)}" for i, j in a["pares"])
    if tipo == "verdadero_falso":
        return "; ".join(f"{i}) {escapar(r)}" for i, r in enumerate(a["respuestas"], start=1))
    if tipo == "adivina":
        return escapar(a["respuesta"])
    return None


def entrada_clave(d, libro=None):
    a = d["actividad"]
    texto = _texto_clave(a, idioma_de(libro))
    if texto is None:
        return None
    return f"\\claveEntrada{{{d['dia']}}}{{{TITULO[a['tipo']]}}}{{{texto}}}\n"
