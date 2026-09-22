#!/usr/bin/env python3
"""Genera el .tex de los días de un libro a partir de su JSON.

Nivel 1 ("Aprendo a leer", el libro por defecto): content/q*.json ->
content/generated-days.tex y content/generated-clave.tex.
Nivel 2 ("Leo con lupa", `--libro nivel2`): content/nivel2/q*.json ->
content/nivel2/generated-days.tex y content/nivel2/generated-clave.tex.
Qué distingue un libro de otro (rutas, reglas, tipos de actividad) está
en tools/libros.py; las plantillas y validaciones propias del nivel 2,
en tools/nivel2.py.

No editar los generated-*.tex a mano -- se sobrescriben cada vez que se
ejecuta este script. Los ficheros que SÍ se editan a mano son los
q1.json ... q4.json de cada libro, uno por trimestre.

Uso:
    python3 tools/gen_days.py                    # regenera el nivel 1
    python3 tools/gen_days.py --libro nivel2     # regenera el nivel 2
    python3 tools/gen_days.py [--libro X] --check
                                  # solo valida, no escribe nada; falla
                                  # (exit 1) si algo no cuadra o si el
                                  # fichero generado está desactualizado
"""

import json
import random
import re
import sys
from pathlib import Path
from string import Template

import nivel2
from comun import ErrorDeContenido, escapar
from libros import CONTENT_DIR, NIVEL1, ROOT, libro_desde_argv

LETRAS_TRAZO_FILE = CONTENT_DIR / "letras-trazo.json"
PALABRAS_TRAZO_FILE = CONTENT_DIR / "palabras-trazo.json"
LANG_FILE = ROOT / "lang" / "es.tex"

# cm por unidad "em" para la actividad "traza" (ver PLANTILLA_TRAZA) --
# el contorno de cada letra (content/letras-trazo.json, generado por
# tools/gen_letras_puntos.py a partir del glifo real de
# fonts/andika/Andika-Bold.ttf) llega en unidades de em (tamaño de
# fuente = 1.0); esta escala lo convierte a cm dentro de la caja de
# actividad, que comparte página con la caja de lectura -- por eso es
# más pequeña que un cartel a toda página. Elegida igual que en su
# momento para el apéndice de trazo: que el par más ancho del alfabeto
# (mayúscula + minúscula de la "w") siga cabiendo dentro del ancho de
# página (170 mm, ver \geometry en preamble.tex) con margen.
ESCALA_TRAZO_CM = 7.0
HUECO_TRAZO_EM = 0.18
RADIO_PUNTO_TRAZO_CM = "0.08"

# Las reglas del nivel 1, con los nombres de siempre (las notas del
# curso se refieren a ellas así). La fuente de verdad es tools/libros.py
# (NIVEL1); esto son solo alias.
TOTAL_DIAS = NIVEL1.total_dias
FRASES_POR_TRIMESTRE = NIVEL1.frases_por_trimestre
RANGO_TRIMESTRE = NIVEL1.rango_trimestre

# Medalla de fin de trimestre (recompensa intermedia, no solo el diploma
# del día 260 -- ver la revisión de un lector externo: un único hito a
# 260 días es una motivación demasiado lejana para 5-7 años). El
# trimestre 4 no lleva medalla propia: termina en el diploma final de
# backmatter/diploma.tex. La estación de cada medalla viene del mismo
# calendario que ya fija RANGO_TRIMESTRE (ver notes/02-revision-y-plan.md,
# punto 1); el texto exacto lo pone el "banner" del día que cierra cada
# trimestre -- ya existe en el JSON, no hace falta duplicarlo.
NOMBRE_MEDALLA_TRIMESTRE = NIVEL1.nombre_medalla
ULTIMO_DIA_TRIMESTRE = NIVEL1.ultimo_dia_trimestre

TIPOS_VALIDOS = NIVEL1.tipos_validos

# En el trimestre 1 la niña todavía no compone una respuesta escrita por
# sí sola -- "responde" (pregunta abierta) no se usa hasta que sepa
# hacerlo; "copia", "rodea" y "verdadero_falso" son lo que hay en su
# lugar (comprensión sin exigir escritura). Ver notes/01-curriculum.md,
# "Rotación de actividades", y notes/02-revision-y-plan.md, punto 4.
TRIMESTRES_SIN_RESPONDE = NIVEL1.trimestres_sin_responde

# Una instrucción de lectura por trimestre -- ver
# notes/02-revision-y-plan.md, punto 5: "despacio, señalando cada
# palabra" (T1) es lo contrario de lo que se espera de quien ya lee con
# soltura (T4). Las cadenas viven en lang/es.tex; aquí solo se elige
# cuál usar, vía el título de cajaLectura (ver PLANTILLA_DIA).
INSTRUCCION_LECTURA_TRIMESTRE = NIVEL1.instruccion_lectura


def formatear_oraciones(oraciones, trimestre):
    """Texto de la caja de lectura, ya alineado según el trimestre.

    T1: una sola frase, centrada -- igual que siempre. Desde T2: cada
    frase en su propia línea, alineada a la izquierda (nunca centrada:
    con dos o más frases, un bloque centrado hace que cada línea empiece
    en un sitio distinto, el peor formato posible para quien empieza a
    leer -- ver notes/02-revision-y-plan.md, punto 5). Una frase que
    empieza por "—" es un diálogo (raya, no comillas rectas -- ver
    preamble.tex sobre el bug de babel con comillas) y lleva sangría
    francesa por si el diálogo ocupa más de una línea.
    """
    if trimestre == 1:
        return r"\centering " + " ".join(escapar(o) for o in oraciones)

    piezas = []
    for oracion in oraciones:
        texto = escapar(oracion)
        if texto.startswith("—"):
            texto = r"\hangindent=4mm\hangafter=1 " + texto
        piezas.append(texto)
    return r"\raggedright " + " \\\\\n".join(piezas)


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
\espacioDibujo[4.3cm]
}"""
)

PLANTILLA_COPIA = Template(
    r"""\actividadCopia{%
\lblInstruccionCopia
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

# Página de medalla al final de un trimestre (T1-T3) -- ver
# NOMBRE_MEDALLA_TRIMESTRE arriba. No usa \diapagina (no es un día del
# libro, no lleva \label{dia:N}) así que tools/check_pages.py necesita
# saber que esta página extra es intencionada, no un desbordamiento --
# ver SALTOS_ESPERADOS en tools/check_pages.py.
PLANTILLA_MEDALLA = Template(
    r"""\begin{center}
\vspace*{2.2cm}

\begin{tikzpicture}[line width=1.4pt, line cap=round, line join=round, color=colorCrea]
  \draw (0,0) circle (0.9);
  \draw (0,0) circle (0.68);
  \node at (0,0) {\bfseries $dia};
  \draw (-0.28,-0.85) -- (-0.56,-1.75) -- (-0.12,-1.4) -- cycle;
  \draw (0.28,-0.85)  -- (0.56,-1.75)  -- (0.12,-1.4)  -- cycle;
\end{tikzpicture}

\vspace{7mm}
{\fontsize{26}{31}\selectfont\bfseries\color{colorLectura} $titulo}\\[6mm]
{\Large\color{colorGris} $banner}\\[10mm]
{\large ¡Sigue así, \rule{55mm}{0.4pt}!}
\end{center}
\vspace*{\fill}
\newpage
"""
)

PLANTILLA_CREA = Template(
    r"""\actividadCrea{%
$prompt
\espacioDibujo
}"""
)

# "Traza" -- practicar cómo se escribe una letra, no cómo se lee (eso
# ya lo hace la niña en la propia caja de lectura). El contorno no es
# un dibujo aparte: es el glifo real de Andika (la misma fuente de todo
# el cuaderno, ver fonts/andika/), convertido en puntos por
# tools/gen_letras_puntos.py y guardado en content/letras-trazo.json.
# Aparece cada dos semanas más o menos, repartido por todo el año (ver
# la lista de conversiones en content/q*.json) -- no es un apéndice
# aparte, es una actividad más dentro del ciclo normal de cada día,
# igual que Dibuja o Completa. Ver la revisión de un lector externo.
PLANTILLA_TRAZA = Template(
    r"""\actividadTraza{%
\begin{center}
{\Large\color{colorGris} $mayus~\lblTrazoDe~$palabra}

\vspace{4mm}
\begin{tikzpicture}
\fill[colorResponde] $puntos;
\end{tikzpicture}

\vspace{4mm}
{\footnotesize\color{colorGris}\lblInstruccionTrazo}\\[5mm]
\rule{0.6\linewidth}{0.4pt}
\end{center}
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

PLANTILLA_RODEA = Template(
    r"""\actividadRodea{%
\footnotesize\color{colorGris}\lblInstruccionRodea
\par\vspace{3mm}\normalfont\large\color{black}
$pregunta
\par\vspace{6mm}
\begin{center}
\Large $opciones
\end{center}
\espacioDibujo[6cm]
}"""
)

PLANTILLA_VERDADERO_FALSO = Template(
    r"""\actividadVerdaderoFalso{%
\footnotesize\color{colorGris}\lblInstruccionVerdaderoFalso
\par\vspace{3mm}\normalfont\large\color{black}
\renewcommand{\arraystretch}{2.2}
\begin{tabularx}{\linewidth}{@{}X >{\centering\arraybackslash}p{30mm}@{}}
$filas
\end{tabularx}
\renewcommand{\arraystretch}{1}
}"""
)

PLANTILLA_BUSCA = Template(
    r"""\actividadBusca{%
$instruccion
\espacioDibujo[8cm]
}"""
)

PLANTILLA_ORDENA = Template(
    r"""\actividadOrdena{%
\footnotesize\color{colorGris}\lblInstruccionOrdena
\par\vspace{3mm}\normalfont\large\color{black}
\begin{itemize}[label=,leftmargin=10mm,itemsep=6mm]
$filas
\end{itemize}
}"""
)

PLANTILLA_RELEE = Template(
    r"""\actividadRelee{%
\footnotesize\color{colorGris}\lblInstruccionRelee
\par\vspace{3mm}\normalfont\normalsize\color{black}
$prompt
\espacioDibujo[7cm]
}"""
)

PLANTILLA_DIA = Template(
    r"""\begin{diapagina}{$dia}{$semana}{$trimestre}{$tema}
\begin{cajaLectura}{$instruccion}
\diafuente{$fuente}%
$oraciones
\end{cajaLectura}
\vspace{5mm}
$actividad
\end{diapagina}
"""
)


def _cargar_json(ruta):
    if not ruta.exists():
        raise ErrorDeContenido(f"no existe {ruta}")
    return json.loads(ruta.read_text(encoding="utf-8"))


_letras_trazo = None
_palabras_trazo = None


def datos_trazo():
    """Carga (una vez, con caché de módulo) los dos ficheros de datos
    de 'traza': el contorno de cada letra (generado, ver
    tools/gen_letras_puntos.py) y la palabra de ejemplo de cada letra
    (editada a mano). Deliberadamente solo biblioteca estándar -- a
    diferencia de tools/gen_letras_puntos.py, esto NO necesita
    matplotlib/numpy/fonttools, así que `make generate` y el job
    `gates` de CI no ganan una dependencia pesada por esta actividad."""
    global _letras_trazo, _palabras_trazo
    if _letras_trazo is None:
        datos = _cargar_json(LETRAS_TRAZO_FILE)
        datos.pop("_comentario", None)
        _letras_trazo = datos
        _palabras_trazo = _cargar_json(PALABRAS_TRAZO_FILE)["palabras"]
    return _letras_trazo, _palabras_trazo


def puntos_tikz_letra(entrada_mayus, entrada_minus):
    """Todos los puntos de una letra (mayúscula + minúscula) en cm,
    listos para un \\fill de TikZ -- mayúscula empieza en x=0,
    minúscula justo después de HUECO_TRAZO_EM. \\actividadTraza envuelve
    el tikzpicture en \\begin{center}, así que no hace falta calcular
    ningún desplazamiento para centrarlo en la página."""
    uc_bbox = entrada_mayus["bbox"]
    lc_bbox = entrada_minus["bbox"]
    ancho_mayus = uc_bbox[2] - uc_bbox[0]

    piezas = []
    for x, y in (pt for contorno in entrada_mayus["contornos"] for pt in contorno):
        cx = (x - uc_bbox[0]) * ESCALA_TRAZO_CM
        cy = y * ESCALA_TRAZO_CM
        piezas.append(f"({cx:.3f},{cy:.3f}) circle ({RADIO_PUNTO_TRAZO_CM})")

    despl_x = ancho_mayus + HUECO_TRAZO_EM - lc_bbox[0]
    for x, y in (pt for contorno in entrada_minus["contornos"] for pt in contorno):
        cx = (x + despl_x) * ESCALA_TRAZO_CM
        cy = y * ESCALA_TRAZO_CM
        piezas.append(f"({cx:.3f},{cy:.3f}) circle ({RADIO_PUNTO_TRAZO_CM})")

    return " ".join(piezas)


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
        # "respuesta" no se imprime en la página del día -- la niña
        # escribe su propia respuesta en \lineaRespuesta, sin verla --
        # pero es obligatoria para poder generar content/generated-clave.tex
        # (ver generar_clave más abajo): sin una clave para el adulto,
        # no hay forma de saber si acertó sin resolver la adivinanza uno
        # mismo. Ver la revisión de un lector externo.
        _campos_requeridos(dia_num, actividad, ["adivinanza", "respuesta"])
        return PLANTILLA_ADIVINA.substitute(
            adivinanza=escapar(actividad["adivinanza"])
        )

    if tipo == "crea":
        _campos_requeridos(dia_num, actividad, ["prompt"])
        return PLANTILLA_CREA.substitute(prompt=escapar(actividad["prompt"]))

    if tipo == "traza":
        _campos_requeridos(dia_num, actividad, ["letra"])
        letra = actividad["letra"]
        letras, palabras = datos_trazo()
        if letra not in letras:
            raise ErrorDeContenido(
                f"día {dia_num}: 'traza' pide la letra {letra!r}, que no "
                f"está en {LETRAS_TRAZO_FILE.name}"
            )
        if letra not in palabras:
            raise ErrorDeContenido(
                f"día {dia_num}: la letra {letra!r} no tiene palabra de "
                f"ejemplo en {PALABRAS_TRAZO_FILE.name}"
            )
        entrada = letras[letra]
        return PLANTILLA_TRAZA.substitute(
            mayus=escapar(letra.upper()),
            palabra=escapar(palabras[letra]),
            puntos=puntos_tikz_letra(entrada["mayuscula"], entrada["minuscula"]),
        )

    if tipo == "repasa":
        _campos_requeridos(dia_num, actividad, ["checklist", "prompt", "banner"])
        items = "\n".join(f"\\item {escapar(i)}" for i in actividad["checklist"])
        return PLANTILLA_REPASA.substitute(
            items=items,
            prompt=escapar(actividad["prompt"]),
            banner=escapar(actividad["banner"]),
        )

    if tipo == "rodea":
        _campos_requeridos(dia_num, actividad, ["pregunta", "opciones"])
        opciones = actividad["opciones"]
        if len(opciones) < 2:
            raise ErrorDeContenido(
                f"día {dia_num}: rodea necesita al menos 2 opciones"
            )
        return PLANTILLA_RODEA.substitute(
            pregunta=escapar(actividad["pregunta"]),
            opciones=r"\hspace{12mm}".join(escapar(o) for o in opciones),
        )

    if tipo == "verdadero_falso":
        _campos_requeridos(dia_num, actividad, ["afirmaciones"])
        afirmaciones = actividad["afirmaciones"]
        if not afirmaciones:
            raise ErrorDeContenido(
                f"día {dia_num}: verdadero_falso necesita al menos 1 afirmación"
            )
        filas = " \\\\\n".join(
            f"{escapar(a)} & \\lblVerdadero\\ \\casilla \\quad \\lblFalso\\ \\casilla"
            for a in afirmaciones
        )
        filas += " \\\\"
        return PLANTILLA_VERDADERO_FALSO.substitute(filas=filas)

    if tipo == "busca":
        _campos_requeridos(dia_num, actividad, ["instruccion"])
        return PLANTILLA_BUSCA.substitute(
            instruccion=escapar(actividad["instruccion"])
        )

    if tipo == "ordena":
        _campos_requeridos(dia_num, actividad, ["sucesos"])
        sucesos = actividad["sucesos"]
        if len(sucesos) < 2:
            raise ErrorDeContenido(
                f"día {dia_num}: ordena necesita al menos 2 sucesos"
            )
        rng = random.Random(dia_num)
        sucesos_mezclados = sucesos[:]
        while sucesos_mezclados == sucesos and len(sucesos) > 1:
            rng.shuffle(sucesos_mezclados)
        filas = "\n".join(
            f"\\item \\casillaNumero\\ {escapar(s)}" for s in sucesos_mezclados
        )
        return PLANTILLA_ORDENA.substitute(filas=filas)

    if tipo == "relee":
        _campos_requeridos(dia_num, actividad, ["prompt"])
        return PLANTILLA_RELEE.substitute(prompt=escapar(actividad["prompt"]))

    raise AssertionError("tipo validado arriba, no debería llegar aquí")


def _campos_requeridos(dia_num, actividad, campos):
    faltan = [c for c in campos if c not in actividad]
    if faltan:
        raise ErrorDeContenido(
            f"día {dia_num}: la actividad {actividad.get('tipo')!r} "
            f"necesita {faltan}"
        )


def _ruta_legible(ruta):
    """content/q*.json, content/nivel2/q*.json... -- para los mensajes y
    la cabecera de los ficheros generados, relativa a la raíz."""
    try:
        return ruta.relative_to(ROOT).as_posix()
    except ValueError:
        return str(ruta)


def origen_json(libro):
    return f"{_ruta_legible(libro.dir_contenido)}/q*.json"


def cargar_dias(libro=NIVEL1):
    """Lee todos los q*.json del libro y devuelve la lista de días, en orden."""
    dias = []
    for fichero in sorted(libro.dir_contenido.glob("q*.json")):
        datos = json.loads(fichero.read_text(encoding="utf-8"))
        dias.extend(datos.get("dias", []))
    dias.sort(key=lambda d: d["dia"])
    return dias


def validar_dia(num, d, libro=NIVEL1):
    """Comprueba las reglas de UN día -- trimestre válido, número dentro
    de su rango, 'responde' no en un trimestre que lo bloquea, número de
    frases correcto y frases bien terminadas (salvo 'relee', que compone
    la semana y no tiene frases propias que contar). En el nivel 2, el
    texto va en párrafos (campo "texto") y lo comprueba
    tools/nivel2.py, igual que los campos de cada actividad.

    No comprueba continuidad entre días -- de eso se encarga quien llama
    esta función: validar_dias() (más abajo) exige 1..260 sin huecos."""
    if num < 1 or num > libro.total_dias:
        raise ErrorDeContenido(f"día {num}: fuera de rango (1-{libro.total_dias})")

    trimestre = d.get("trimestre")
    if trimestre not in libro.rango_trimestre:
        raise ErrorDeContenido(f"día {num}: trimestre inválido: {trimestre!r}")

    lo, hi = libro.rango_trimestre[trimestre]
    if not (lo <= num <= hi):
        raise ErrorDeContenido(
            f"día {num}: dice ser del trimestre {trimestre} "
            f"(días {lo}-{hi}) pero su número no está en ese rango"
        )

    tipo_actividad = d.get("actividad", {}).get("tipo")
    if tipo_actividad not in libro.tipos_validos:
        raise ErrorDeContenido(
            f"día {num}: tipo de actividad desconocido en el {libro.nombre}: "
            f"{tipo_actividad!r}"
        )
    if tipo_actividad == "responde" and trimestre in libro.trimestres_sin_responde:
        raise ErrorDeContenido(
            f"día {num}: 'responde' no se usa en el trimestre {trimestre} "
            "-- la niña todavía no compone una respuesta escrita por sí "
            "sola a esta edad; usa 'copia', 'rodea' o 'verdadero_falso' "
            "en su lugar"
        )

    if libro.frases_por_trimestre is None:
        nivel2.validar_texto(num, d)
        return

    if tipo_actividad == "relee":
        return

    oraciones = d.get("oraciones", [])
    esperado_frases = libro.frases_por_trimestre[trimestre]
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


def validar_dias(dias, libro=NIVEL1):
    """Comprueba las reglas del curso -- exige además que los días sean
    1..260 sin huecos, que es lo que hace a esta lista EL libro real."""
    if not dias:
        raise ErrorDeContenido(f"no hay ningún día en {origen_json(libro)}")

    esperado = 1
    for d in dias:
        num = d["dia"]
        if num != esperado:
            raise ErrorDeContenido(
                f"los días deben ser consecutivos empezando en 1: "
                f"se esperaba el día {esperado}, se encontró el día {num}"
            )
        esperado += 1
        validar_dia(num, d, libro)


def texto_semana(dias_por_semana, dia_actual):
    """Para un día 'relee': la PRIMERA frase de cada día anterior de la
    misma semana (lunes a jueves), en orden -- ver notes/02-revision-y-plan.md,
    punto 3. No hace falta repetir el texto en el JSON de un día 'relee':
    se compone solo, a partir de lo que ya se escribió esa semana.

    Solo la primera frase de cada día (no todas): en el trimestre 1 no
    cambia nada (un día = una frase), pero a partir del trimestre 2 un
    día trae 2-4 frases, y componer TODAS las de lunes a jueves crece con
    el trimestre (hasta 16 frases en el T4) sin que quepan en una caja
    que comparte página con la actividad -- ver el hallazgo del PR de
    T2. Una frase por día mantiene el texto compuesto en ~4 frases
    siempre, del mismo orden de magnitud que ya funciona en T1."""
    clave = (dia_actual["trimestre"], dia_actual["semana"])
    anteriores = [
        d for d in dias_por_semana.get(clave, [])
        if d["dia"] < dia_actual["dia"] and d["actividad"]["tipo"] != "relee"
    ]
    anteriores.sort(key=lambda d: d["dia"])
    oraciones = [d["oraciones"][0] for d in anteriores]
    if not oraciones:
        raise ErrorDeContenido(
            f"día {dia_actual['dia']}: 'relee' no encuentra ningún día "
            "anterior de la misma semana del que componer el texto"
        )
    return oraciones


# Un día "relee" compone hasta 4 días de frases en una sola caja --
# siempre más texto que un día normal de su propio trimestre, así que
# usa un tamaño de letra fijo y más pequeño (el de T3) en vez de
# \diafuente{trimestre}, sea cual sea su trimestre real. Sin esto, un
# "relee" de T1 (fuente más grande, 28pt) no cabe en una página -- visto
# al escribir las primeras semanas nuevas de T1, no solo en teoría.
FUENTE_RELEE = 3


def fuente_lectura(d):
    if d["actividad"]["tipo"] == "relee":
        return FUENTE_RELEE
    return d["trimestre"]


def _cabecera_generada(ruta, libro):
    origen = origen_json(libro)
    return [
        f"% {_ruta_legible(ruta)}\n",
        f"% GENERADO por tools/gen_days.py a partir de {origen}.\n",
        "% NO EDITAR A MANO -- los cambios se perderán en la siguiente\n",
        f"% ejecución de `make generate`. Edita {origen} en su lugar.\n\n",
    ]


def pagina_medalla(d, libro):
    """La página de medalla que sigue al último día de un trimestre (T1-T3),
    o None si este día no cierra ningún trimestre con medalla."""
    if d["dia"] != libro.ultimo_dia_trimestre.get(d["trimestre"]):
        return None
    if d["trimestre"] not in libro.nombre_medalla:
        return None
    banner = d["actividad"].get("banner")
    if not banner:
        raise ErrorDeContenido(
            f"día {d['dia']}: cierra el trimestre {d['trimestre']} "
            "y necesita un 'banner' (en su actividad) "
            "para la medalla de fin de trimestre"
        )
    return PLANTILLA_MEDALLA.substitute(
        dia=d["dia"],
        titulo=f"¡Medalla de {libro.nombre_medalla[d['trimestre']]}!",
        banner=escapar(banner),
    )


def generar_tex(dias, libro=NIVEL1):
    piezas = _cabecera_generada(libro.salida_dias, libro)

    if libro.nivel == 2:
        dias_por_semana = {}
        for d in dias:
            dias_por_semana.setdefault((d["trimestre"], d["semana"]), []).append(d)
        for d in dias:
            semana = sorted(
                dias_por_semana[(d["trimestre"], d["semana"])], key=lambda x: x["dia"]
            )
            piezas.append(nivel2.pagina_dia(d, libro, semana))
            medalla = pagina_medalla(d, libro)
            if medalla:
                piezas.append(medalla)
        return "\n".join(piezas)

    dias_por_semana = {}
    for d in dias:
        dias_por_semana.setdefault((d["trimestre"], d["semana"]), []).append(d)

    for d in dias:
        actividad_tex = render_actividad(d["dia"], d["actividad"])
        if d["actividad"]["tipo"] == "relee":
            oraciones_dia = texto_semana(dias_por_semana, d)
        else:
            oraciones_dia = d["oraciones"]
        piezas.append(
            PLANTILLA_DIA.substitute(
                dia=d["dia"],
                semana=d["semana"],
                trimestre=d["trimestre"],
                fuente=fuente_lectura(d),
                tema=escapar(d.get("tema", "")),
                instruccion=libro.instruccion_lectura[d["trimestre"]],
                oraciones=formatear_oraciones(oraciones_dia, d["trimestre"]),
                actividad=actividad_tex,
            )
        )

        medalla = pagina_medalla(d, libro)
        if medalla:
            piezas.append(medalla)
    return "\n".join(piezas)


def generar_clave(dias, libro=NIVEL1):
    """generated-clave.tex: la respuesta de cada actividad que tiene una
    respuesta que comprobar, para que un adulto pueda hacerlo sin
    resolverla él mismo -- ver la revisión de un lector externo. En el
    nivel 1, 'adivina' y 'relaciona'; en el nivel 2, casi todas (ver
    tools/nivel2.py, entrada_clave). No se imprime en la página del día
    (ver PLANTILLA_ADIVINA); vive aparte, en la clave de respuestas del
    final de cada libro."""
    piezas = _cabecera_generada(libro.salida_clave, libro)
    if libro.nivel == 2:
        for d in dias:
            entrada = nivel2.entrada_clave(d)
            if entrada:
                piezas.append(entrada)
        return "".join(piezas)

    for d in dias:
        actividad = d["actividad"]
        tipo = actividad.get("tipo")
        if tipo == "adivina":
            texto = escapar(actividad["respuesta"])
            piezas.append(f"\\claveEntrada{{{d['dia']}}}{{\\lblAdivina}}{{{texto}}}\n")
        elif tipo == "relaciona":
            texto = " \\quad ".join(
                f"{escapar(i)} $\\rightarrow$ {escapar(j)}"
                for i, j in actividad["pares"]
            )
            piezas.append(f"\\claveEntrada{{{d['dia']}}}{{\\lblRelaciona}}{{{texto}}}\n")
    return "".join(piezas)


def comprobar_totaldias(libro):
    """lang/es.tex promete que \\totaldias (el pie de página y el
    diploma) y el total de días del libro son el mismo número -- esto es
    lo que lo comprueba (ver notes/02-revision-y-plan.md, punto 9)."""
    texto = LANG_FILE.read_text(encoding="utf-8")
    m = re.search(r"\\newcommand\{\\totaldias\}\{(\d+)\}", texto)
    if not m:
        raise ErrorDeContenido(f"{_ruta_legible(LANG_FILE)} no define \\totaldias")
    if int(m.group(1)) != libro.total_dias:
        raise ErrorDeContenido(
            f"\\totaldias vale {m.group(1)} en {_ruta_legible(LANG_FILE)}, "
            f"pero el {libro.nombre} tiene {libro.total_dias} días"
        )


def main():
    check_only = "--check" in sys.argv
    libro = libro_desde_argv(sys.argv[1:])

    try:
        comprobar_totaldias(libro)
        dias = cargar_dias(libro)
        validar_dias(dias, libro)
        tex = generar_tex(dias, libro)
        clave = generar_clave(dias, libro)
    except ErrorDeContenido as exc:
        print(f"ERROR ({libro.nombre}): {exc}", file=sys.stderr)
        return 1

    salidas = [(libro.salida_dias, tex), (libro.salida_clave, clave)]

    if check_only:
        for ruta, contenido in salidas:
            actual = ruta.read_text(encoding="utf-8") if ruta.exists() else None
            if actual != contenido:
                print(
                    f"DESACTUALIZADO: {_ruta_legible(ruta)} no coincide con "
                    f"{origen_json(libro)} -- ejecuta `make generate`.",
                    file=sys.stderr,
                )
                return 1
        print(
            f"OK ({libro.nombre}): {len(dias)} días validados, "
            f"{libro.salida_dias.name} y {libro.salida_clave.name} al día."
        )
        return 0

    for ruta, contenido in salidas:
        ruta.write_text(contenido, encoding="utf-8")
    print(f"Escrito {_ruta_legible(libro.salida_dias)} con {len(dias)} días, y {_ruta_legible(libro.salida_clave)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
