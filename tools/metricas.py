#!/usr/bin/env python3
"""Mide la progresión real de content/q*.json y la compara con los
objetivos de content/progresion.json -- ver notes/02-revision-y-plan.md,
Parte B punto 2 y punto 6, y Parte C.

Cuatro métricas por día (una página = un día):
  - palabras: total de palabras de todas las oraciones de ese día.
  - frase_max_dia: palabras de la oración más larga de ese día.
  - nuevas: lemas de contenido nuevos ese día (primera aparición en todo
    el libro, sin contar palabras funcionales ni nombres propios del
    reparto -- ver PALABRAS_FUNCIONALES y NOMBRES_PROPIOS más abajo).
  - lo anterior se compara contra la fila de esa semana en
    content/progresion.json.

palabras_max y frase_max son límites duros: si un día los supera, falla
(exit 1). nuevas_max es un aviso: se imprime pero no hace fallar el
check -- ver la cabecera de content/progresion.json para el porqué de
esta distinción. Un día de tipo "relee" (Etapa 2) no se mide contra
palabras_min/palabras_max: por definición es más largo, compone la
semana entera.

La lematización es deliberadamente simple (recorte de plurales +
content/familias.json opcional para excepciones a mano) -- no es un
lematizador de verdad, así que puede sobre-contar (formas irregulares
que no se recortan bien) o infra-contar (formas que no deberían
fusionarse pero lo hacen). Sirve para vigilar una tendencia, no como
métrica exacta.

"Leo con lupa", el nivel 3 (`--libro lupa`, content/lupa/q*.json
contra content/lupa/progresion.json): el texto de un día son párrafos,
no una lista de frases, así que las frases se separan aquí (ver
oraciones_de_parrafos), y se mide una cosa más -- `subordinadas`, las
conjunciones y relativos que abren una oración subordinada (que,
porque, cuando, aunque, mientras, si, donde, como...; ver
SUBORDINANTES). Es la forma sencilla de comprobar que su texto está
hecho de oraciones compuestas de verdad, que es lo que lo distingue del
cuaderno de frases: `subordinadas_min` es un límite duro, igual que
palabras_max y frase_max. Y el vocabulario nuevo se cuenta contra todo
lo que ya se leyó en el cuaderno de frases, no desde cero.

Uso:
    python3 tools/metricas.py            # informe por día + resumen; exit 1 si hay errores
    python3 tools/metricas.py --tabla    # tabla en Markdown por semana (para GITHUB_STEP_SUMMARY)
    python3 tools/metricas.py --libro lupa [--tabla]
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_days import cargar_dias  # noqa: E402
from gen_days import texto_semana  # noqa: E402
from libros import CONTENT_DIR, FRASES, libro_desde_argv  # noqa: E402
from lupa import texto_plano  # noqa: E402

FAMILIAS_FILE = CONTENT_DIR / "familias.json"

# Tipos de actividad cuyo texto de lectura no se mide contra
# palabras_min/palabras_max -- "relee" compone la semana entera a
# propósito (ver notes/02-revision-y-plan.md, punto 3 y Etapa 2).
TIPOS_SIN_PRESUPUESTO_PALABRAS = {"relee"}

# Palabras que no cuentan como vocabulario nuevo: funcionales (artículos,
# preposiciones, conjunciones, pronombres, auxiliares muy frecuentes) y
# nombres propios del reparto, que se repiten constantemente a propósito
# (ver notes/01-curriculum.md, "Vocabulario").
PALABRAS_FUNCIONALES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
    "a", "ante", "bajo", "con", "contra", "de", "desde", "durante", "en",
    "entre", "hacia", "hasta", "para", "por", "según", "sin", "so", "sobre",
    "tras",
    "y", "e", "o", "u", "ni", "que", "pero", "porque", "cuando", "como",
    "si", "aunque", "mientras", "pues", "también",
    "yo", "tú", "él", "ella", "nosotros", "vosotros", "ellos", "ellas",
    "usted", "ustedes", "me", "te", "se", "le", "les", "nos", "os",
    "su", "sus", "mi", "mis", "tu", "tus", "nuestro", "nuestra",
    "nuestros", "nuestras",
    "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas",
    "eso", "esto", "aquello",
    "todo", "toda", "todos", "todas", "otro", "otra", "otros", "otras",
    "mucho", "mucha", "muchos", "muchas", "poco", "poca", "pocos", "pocas",
    "es", "son", "era", "eran", "fue", "fueron", "ser", "sea",
    "está", "están", "estaba", "estaban", "estar", "esté",
    "ha", "han", "había", "habían", "haber", "hay",
    "no", "sí", "muy", "más", "menos", "ya", "todavía", "siempre", "nunca",
    "aquí", "allí", "ahí", "hoy", "ayer", "mañana", "bien", "mal",
    "quien", "quién", "cuál", "cuáles", "cómo", "dónde", "qué",
}

# Nombres propios del reparto: se repiten constantemente a propósito, no
# cuentan como "palabra nueva" -- ver notes/01-curriculum.md. Cada libro
# tiene su lista (tools/libros.py); esta es la del cuaderno de frases.
NOMBRES_PROPIOS = FRASES.nombres_propios

# "Leo con lupa": palabras que abren una oración subordinada (sustantiva,
# relativa o adverbial). "que" las cubre casi todas las compuestas
# (para que, antes de que, ya que, así que, hasta que...); las formas
# con tilde (qué, cómo, dónde, cuándo) NO cuentan -- son preguntas
# directas, no subordinadas. Es una aproximación a propósito, igual
# que la lematización de abajo: vigila una tendencia (que los textos
# de "Leo con lupa" sigan hechos de oraciones complejas), no hace análisis
# sintáctico.
SUBORDINANTES = {
    "que", "porque", "cuando", "aunque", "mientras", "si", "donde",
    "como", "quien", "quienes", "cual", "cuales", "cuyo", "cuya",
    "cuyos", "cuyas", "cuanto",
}

# Fin de frase en un párrafo: . ! ? … (y la raya o el cierre de
# comillas que puedan ir detrás), seguido de espacio y de algo que
# empieza una frase nueva.
_FIN_DE_FRASE = re.compile(r"(?<=[.!?…])[»—]?\s+(?=[¿¡«—A-ZÁÉÍÓÚÑ])")


def cargar_progresion(libro=FRASES):
    datos = json.loads(libro.progresion.read_text(encoding="utf-8"))
    return {fila["semana"]: fila for fila in datos["semanas"]}


def cargar_familias():
    if not FAMILIAS_FILE.exists():
        return {}
    return json.loads(FAMILIAS_FILE.read_text(encoding="utf-8"))




def lematizar(palabra, familias, nombres_propios=NOMBRES_PROPIOS):
    p = palabra.strip(".,;:!¡?¿\"«»—-").lower()
    if not p:
        return None
    if p in familias:
        return familias[p]
    if p in PALABRAS_FUNCIONALES or p in nombres_propios:
        return None
    if p.endswith("es") and len(p) > 5:
        return p[:-2]
    if p.endswith("s") and len(p) > 4:
        return p[:-1]
    return p


def oraciones_de_parrafos(parrafos):
    """Las frases de un texto de "Leo con lupa": cada párrafo (o elemento de
    lista, o nota) termina al menos una frase, y dentro de un párrafo se
    corta en cada fin de frase (ver _FIN_DE_FRASE)."""
    oraciones = []
    for parrafo in parrafos:
        if parrafo.startswith(("> ", "- ")):
            parrafo = parrafo[2:]
        for linea in parrafo.split("\n"):
            oraciones.extend(t for t in _FIN_DE_FRASE.split(linea.strip()) if t.strip())
    return oraciones


def contar_subordinantes(oraciones):
    total = 0
    for oracion in oraciones:
        for token in oracion.split():
            if token.strip(".,;:!¡?¿\"«»—-()").lower() in SUBORDINANTES:
                total += 1
    return total


def oraciones_del_dia(d, dias_por_semana, libro):
    if libro.parrafos:
        return oraciones_de_parrafos(d["texto"])
    if d["actividad"]["tipo"] == "relee":
        return texto_semana(dias_por_semana, d)
    return d["oraciones"]


def lemas_de_libro(libro, familias):
    """Todos los lemas de contenido de un libro entero -- para que el
    vocabulario nuevo de "Leo con lupa" se cuente contra lo ya leído en
    el cuaderno de frases."""
    vistos = set()
    for fila in metricas_por_dia(cargar_dias(libro), familias, libro):
        vistos.update(fila["lemas_nuevos"])
    return vistos


def metricas_por_dia(dias, familias, libro=FRASES, vistos_previos=None):
    """Devuelve una lista de dicts, uno por día, con sus métricas y la
    lista de lemas de contenido NUEVOS ese día (cumulativo, en orden de
    día -- ver la cabecera del módulo). Un día 'relee' no tiene
    `oraciones` propias en el JSON -- se componen igual que en
    tools/gen_days.py (texto_semana), para medir lo mismo que se acaba
    imprimiendo en la página."""
    dias_por_semana = {}
    for d in dias:
        dias_por_semana.setdefault((d["trimestre"], d["semana"]), []).append(d)

    vistos = set(vistos_previos or ())
    filas = []
    for d in dias:
        oraciones = oraciones_del_dia(d, dias_por_semana, libro)
        palabras = sum(len(o.split()) for o in oraciones)
        frase_max_dia = max(len(o.split()) for o in oraciones)

        lemas_dia = []
        for oracion in oraciones:
            for token in oracion.split():
                lema = lematizar(token, familias, libro.nombres_propios)
                if lema and lema not in vistos:
                    vistos.add(lema)
                    lemas_dia.append(lema)

        fila = {
            "dia": d["dia"],
            "semana": d["semana"],
            "trimestre": d["trimestre"],
            "tipo": d["actividad"]["tipo"],
            "palabras": palabras,
            "frase_max_dia": frase_max_dia,
            "nuevas": len(lemas_dia),
            "lemas_nuevos": lemas_dia,
        }
        if libro.parrafos:
            fila["subordinadas"] = contar_subordinantes(oraciones)
        filas.append(fila)
    return filas


def evaluar(filas, progresion):
    """Añade a cada fila sus violaciones (errores) y avisos, comparando
    con la semana correspondiente de progresion.json."""
    for fila in filas:
        obj = progresion.get(fila["semana"])
        errores = []
        avisos = []
        if obj is None:
            errores.append(f"la semana {fila['semana']} no está en content/progresion.json")
        else:
            mide_palabras = fila["tipo"] not in TIPOS_SIN_PRESUPUESTO_PALABRAS
            if mide_palabras and fila["palabras"] > obj["palabras_max"]:
                errores.append(
                    f"palabras={fila['palabras']} > palabras_max={obj['palabras_max']}"
                )
            if fila["frase_max_dia"] > obj["frase_max"]:
                errores.append(
                    f"frase más larga={fila['frase_max_dia']} > frase_max={obj['frase_max']}"
                )
            if mide_palabras and fila["palabras"] < obj["palabras_min"]:
                avisos.append(
                    f"palabras={fila['palabras']} < palabras_min={obj['palabras_min']}"
                )
            if fila["nuevas"] > obj["nuevas_max"]:
                avisos.append(
                    f"nuevas={fila['nuevas']} > nuevas_max={obj['nuevas_max']}"
                )
            if "subordinadas" in fila and fila["subordinadas"] < obj.get("subordinadas_min", 0):
                errores.append(
                    f"subordinadas={fila['subordinadas']} < subordinadas_min={obj['subordinadas_min']}"
                )
        fila["errores"] = errores
        fila["avisos"] = avisos
    return filas


def informe(filas):
    dias_con_error = [f for f in filas if f["errores"]]
    dias_con_aviso = [f for f in filas if f["avisos"]]

    for fila in filas:
        if not fila["errores"] and not fila["avisos"]:
            continue
        print(f"Día {fila['dia']} (semana {fila['semana']}, trimestre {fila['trimestre']}):")
        for e in fila["errores"]:
            print(f"  ERROR: {e}")
        for a in fila["avisos"]:
            print(f"  AVISO: {a}")

    print()
    print(
        f"{len(filas)} días medidos -- "
        f"{len(dias_con_error)} con error, {len(dias_con_aviso)} con aviso."
    )
    return 1 if dias_con_error else 0


def tabla_markdown(filas, progresion):
    por_semana = {}
    for fila in filas:
        por_semana.setdefault(fila["semana"], []).append(fila)

    # La columna de subordinadas solo existe en "Leo con lupa" -- la tabla
    # del cuaderno de frases sigue siendo exactamente la de siempre.
    con_subordinadas = any("subordinadas" in f for f in filas)
    cabecera = "| Semana | Trim. | Días | Palabras (real) | Objetivo | Frase más larga | Nuevas (máx. día) |"
    separador = "|---|---|---|---|---|---|---|"
    if con_subordinadas:
        cabecera += " Subordinadas (mín. día) |"
        separador += "---|"
    lineas = [cabecera + " Estado |", separador + "---|"]
    total_error = total_aviso = 0
    for semana in sorted(por_semana):
        grupo = por_semana[semana]
        obj = progresion.get(semana, {})
        palabras_reales = [f["palabras"] for f in grupo]
        frases_reales = [f["frase_max_dia"] for f in grupo]
        nuevas_reales = [f["nuevas"] for f in grupo]
        n_error = sum(1 for f in grupo if f["errores"])
        n_aviso = sum(1 for f in grupo if f["avisos"])
        total_error += n_error
        total_aviso += n_aviso
        estado = "🔴 error" if n_error else ("🟡 aviso" if n_aviso else "🟢 ok")
        linea = "| {sem} | {tri} | {n} | {pmin}–{pmax} | {omin}–{omax} | {fmax} (obj. {ofmax}) | {nmax} (máx. {onmax}) |".format(
            sem=semana,
            tri=grupo[0]["trimestre"],
            n=len(grupo),
            pmin=min(palabras_reales),
            pmax=max(palabras_reales),
            omin=obj.get("palabras_min", "?"),
            omax=obj.get("palabras_max", "?"),
            fmax=max(frases_reales),
            ofmax=obj.get("frase_max", "?"),
            nmax=max(nuevas_reales),
            onmax=obj.get("nuevas_max", "?"),
        )
        if con_subordinadas:
            linea += " {smin} (obj. {osmin}) |".format(
                smin=min(f["subordinadas"] for f in grupo),
                osmin=obj.get("subordinadas_min", "?"),
            )
        lineas.append(linea + f" {estado} |")
    print("\n".join(lineas))
    print()
    print(f"{len(filas)} días, {len(por_semana)} semanas con contenido -- {total_error} días con error, {total_aviso} con aviso.")
    return 1 if total_error else 0


def main():
    modo_tabla = "--tabla" in sys.argv
    libro = libro_desde_argv(sys.argv[1:])

    progresion = cargar_progresion(libro)
    familias = cargar_familias()
    dias = cargar_dias(libro)
    if not dias:
        origen = libro.dir_contenido.relative_to(CONTENT_DIR.parent).as_posix()
        print(f"ERROR: no hay ningún día en {origen}/q*.json", file=sys.stderr)
        return 1

    vistos_previos = None
    if libro.parrafos:
        vistos_previos = lemas_de_libro(FRASES, familias)
    filas = metricas_por_dia(dias, familias, libro, vistos_previos)
    evaluar(filas, progresion)

    if modo_tabla:
        return tabla_markdown(filas, progresion)
    return informe(filas)


if __name__ == "__main__":
    sys.exit(main())
