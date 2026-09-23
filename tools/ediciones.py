"""Las ediciones de los cuadernos (ver notes/07-ediciones.md): el mismo
contenido, otra selección de días, con su propia portada y su propia
introducción.

- "verano": el cuaderno de verano -- solo los 65 días del verano (del
  196 al 260), impresos como días 1 a 65 y semanas 1 a 13.
- "muestra": la muestra gratuita -- las cuatro primeras semanas (días 1
  a 20), con su número de siempre: son el principio del libro entero.

Cada generador (tools/gen_days.py, tools/gen_palabras.py) escribe, además
del libro entero, los .tex de cada edición (generated-days-verano.tex,
generated-clave-verano.tex): las mismas páginas, una a una, de los días
de la edición -- no se vuelve a generar ninguna, se escogen --, y, si la
edición lleva mapa propio, sus filas (generated-mapa-verano.tex: cada
semana con su tema). Lo único que cambia dentro de una página es el
cartel de "¡200 páginas leídas!", que en el cuaderno de verano es "¡5
páginas leídas!" (ver banner_edicion). El número del día y de la semana
que se imprime lo resta LaTeX (\\numeroDia, preamble.tex), con los
mismos números que hay aquí -- comprobar_preamble() se asegura de que
coinciden.
"""

import re
from dataclasses import dataclass

from comun import ErrorDeContenido, escapar
from libros import ROOT


@dataclass(frozen=True)
class Edicion:
    nombre: str
    desde: int  # el primer día del libro entero que entra
    hasta: int  # y el último
    desplazamiento_dias: int  # lo que se resta al número del día al imprimirlo
    desplazamiento_semanas: int  # y al de la semana
    total_dias: int  # \totaldias en la edición (None: el del libro entero)
    mapa: bool  # si lleva su propio mapa (\mapaEdicion) en vez del del curso

    def contiene(self, dia):
        return self.desde <= dia <= self.hasta


VERANO = Edicion(
    nombre="verano", desde=196, hasta=260,
    desplazamiento_dias=195, desplazamiento_semanas=39, total_dias=65,
    mapa=True,
)

MUESTRA = Edicion(
    nombre="muestra", desde=1, hasta=20,
    desplazamiento_dias=0, desplazamiento_semanas=0, total_dias=None,
    mapa=False,
)

EDICIONES = (VERANO, MUESTRA)


def ruta_edicion(ruta, edicion):
    """content/generated-days.tex -> content/generated-days-verano.tex"""
    return ruta.with_name(f"{ruta.stem}-{edicion.nombre}{ruta.suffix}")


# El cartel de los viernes empieza siempre por el número de páginas
# leídas, que es el número del día.
PATRON_BANNER = {
    "es": re.compile(r"^¡(\d+) páginas leídas!"),
    "en": re.compile(r"^(\d+) pages read!"),
}


def banner_edicion(d, edicion, idioma):
    """El cartel del día d en la edición: con el número de páginas que se
    llevan leídas en ella (¡200 páginas leídas! es ¡5 páginas leídas! en
    el cuaderno de verano). Si el resto del cartel habla del número
    (¡Doscientas!), la actividad lleva el suyo propio para la edición:
    "banner_verano". None si el día no tiene cartel. Una edición que no
    cambia los números (la muestra) deja el cartel como está."""
    actividad = d["actividad"]
    banner = actividad.get("banner")
    if banner is None:
        return None
    if edicion.desplazamiento_dias == 0:
        return banner
    propio = actividad.get(f"banner_{edicion.nombre}")
    if propio is not None:
        return propio
    m = PATRON_BANNER[idioma].match(banner)
    if not m:
        raise ErrorDeContenido(
            f"día {d['dia']}: el cartel «{banner}» no empieza por las "
            f"páginas leídas, y la edición «{edicion.nombre}» necesita "
            f"cambiarle el número -- o ponerle uno propio en "
            f"'banner_{edicion.nombre}'"
        )
    if int(m.group(1)) != d["dia"]:
        raise ErrorDeContenido(
            f"día {d['dia']}: el cartel «{banner}» cuenta {m.group(1)} "
            "páginas leídas, que no son las de ese día"
        )
    return f"{banner[:m.start(1)]}{d['dia'] - edicion.desplazamiento_dias}{banner[m.end(1):]}"


def pagina_en_edicion(tex, d, edicion, idioma):
    """La página del día d (el .tex que ya se ha generado para el libro
    entero), tal como sale en la edición: igual, salvo el cartel."""
    nuevo = banner_edicion(d, edicion, idioma)
    if nuevo is None:
        return tex
    viejo = escapar(d["actividad"]["banner"])
    if tex.count(viejo) != 1:
        raise ErrorDeContenido(
            f"día {d['dia']}: no se encuentra una sola vez su cartel en la "
            "página generada, para cambiarlo en la edición "
            f"«{edicion.nombre}»"
        )
    return tex.replace(viejo, escapar(nuevo))


def ediciones_completas(dias):
    """Las ediciones que tienen escritos todos sus días: las de un libro
    en obras (dias_escritos, un PR por trimestre) esperan a tenerlos."""
    numeros = {d["dia"] for d in dias}
    return [
        e for e in EDICIONES
        if all(n in numeros for n in range(e.desde, e.hasta + 1))
    ]


def mapa_edicion(dias, edicion):
    """\\filasMapaEdicion: una fila por semana de la edición (\\filaMapa,
    preamble.tex) con sus días y el tema de su primer día, para el mapa
    del verano -- el que va en vez del mapa del curso."""
    semanas = {}
    for d in dias:
        if edicion.contiene(d["dia"]):
            semanas.setdefault(d["semana"], []).append(d)
    filas = []
    for semana, ds in sorted(semanas.items()):
        ds.sort(key=lambda d: d["dia"])
        tema = escapar(ds[0].get("tema", ""))
        filas.append(
            f"\\filaMapa{{{semana}}}{{{ds[0]['dia']}}}{{{ds[-1]['dia']}}}{{{tema}}}%\n"
        )
    return "\\def\\filasMapaEdicion{%\n" + "".join(filas) + "}\n"


def salidas_ediciones(dias, paginas, entradas, salida_dias, salida_clave,
                      cabecera, idioma):
    """[(ruta, contenido)]: los .tex de cada edición -- las páginas del
    libro entero ([(d, tex)], en orden y sin medallas) de los días de la
    edición, con el cartel de cada viernes cambiado; sus entradas de la
    clave ([(d, entrada)]), y las filas de su mapa si lleva mapa propio.
    `cabecera(ruta)` es el comentario de "GENERADO, no editar" de cada
    generador."""
    salidas = []
    for e in ediciones_completas(dias):
        ruta_dias = ruta_edicion(salida_dias, e)
        piezas = [cabecera(ruta_dias)]
        piezas.extend(
            pagina_en_edicion(tex, d, e, idioma)
            for d, tex in paginas if e.contiene(d["dia"])
        )
        ruta_clave = ruta_edicion(salida_clave, e)
        clave = [cabecera(ruta_clave)]
        clave.extend(entrada for d, entrada in entradas if e.contiene(d["dia"]))
        salidas += [(ruta_dias, "\n".join(piezas)), (ruta_clave, "".join(clave))]
        if e.mapa:
            ruta_mapa = ruta_edicion(salida_dias.with_name("generated-mapa.tex"), e)
            salidas.append((ruta_mapa, cabecera(ruta_mapa) + mapa_edicion(dias, e)))
    return salidas


def comprobar_campos(d):
    """'banner_<edición>' solo tiene sentido en un día de esa edición que
    ya tiene cartel."""
    actividad = d["actividad"]
    for e in EDICIONES:
        clave = f"banner_{e.nombre}"
        if clave in actividad and (not e.contiene(d["dia"]) or "banner" not in actividad):
            raise ErrorDeContenido(
                f"día {d['dia']}: '{clave}' solo va en un día de la edición "
                f"«{e.nombre}» (días {e.desde}-{e.hasta}) que tenga 'banner'"
            )


def comprobar_preamble():
    """preamble.tex resta al imprimir los mismos números que hay aquí. Lo
    que el bloque de una edición no fija se queda como en el libro entero:
    nada que restar, y el \\totaldias de siempre."""
    texto = (ROOT / "preamble.tex").read_text(encoding="utf-8")
    for e in EDICIONES:
        m = re.search(
            r"\\ifx\\edicion\\aal@edicion@" + e.nombre + r"\b(.*?)\\fi", texto, re.S
        )
        if not m:
            raise ErrorDeContenido(f"preamble.tex no tiene la edición «{e.nombre}»")
        bloque = m.group(1)
        esperado = {
            r"\desplazamientoDias": (
                r"\\def\\desplazamientoDias\{(\d+)\}", e.desplazamiento_dias, 0),
            r"\desplazamientoSemanas": (
                r"\\def\\desplazamientoSemanas\{(\d+)\}", e.desplazamiento_semanas, 0),
            r"\totaldias": (
                r"\\renewcommand\{\\totaldias\}\{(\d+)\}", e.total_dias, None),
        }
        for macro, (patron, valor, por_defecto) in esperado.items():
            n = re.search(patron, bloque)
            if (int(n.group(1)) if n else por_defecto) != valor:
                debe = "no se cambia" if valor is None else f"tiene que ser {valor}"
                raise ErrorDeContenido(
                    f"preamble.tex, edición «{e.nombre}»: {macro} {debe}, "
                    "como en tools/ediciones.py"
                )
