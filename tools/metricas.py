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

"Read and Draw", el cuaderno en inglés (`--libro english`,
content/english/q*.json contra content/english/progresion.json): lo
mismo que "Leo con lupa", con las listas de palabras del inglés
(funcionales y nexos de subordinación: because, when, if, that, who...;
ver *_EN más abajo), su propia forma de acabar una frase (el diálogo va
entre “ ”) y una lematización igual de sencilla, pero inglesa (un
recorte de -s, -ed, -ing y una lista de verbos irregulares). El
vocabulario nuevo se cuenta contra content/english/vocabulario-base.json:
las palabras que se dan por sabidas del inglés del colegio (colores,
números, animales, la familia...).

«Zdania», el cuaderno de frases en polaco (`--libro zdania`,
content/zdania/q*.json contra content/zdania/progresion.json): las mismas
métricas que el cuaderno de frases, con las palabras funcionales del
polaco (ver *_PL más abajo) y una lematización igual de sencilla, pero
para una lengua que declina: se quita una terminación (de caso, de
número o de verbo) y se corta a unas pocas letras, así que "kot", "kota"
y "kotem" son la misma palabra, y "czyta", "czytają" y "czytać" también.
Los nombres del reparto cuentan en todas sus formas (Lucíi, Daniego,
babci...: ver ZDANIA.nombres_propios en tools/libros.py).

Uso:
    python3 tools/metricas.py            # informe por día + resumen; exit 1 si hay errores
    python3 tools/metricas.py --tabla    # tabla en Markdown por semana (para GITHUB_STEP_SUMMARY)
    python3 tools/metricas.py --libro lupa [--tabla]
    python3 tools/metricas.py --libro english [--tabla]
    python3 tools/metricas.py --libro zdania [--tabla]
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
VOCABULARIO_BASE_EN = CONTENT_DIR / "english" / "vocabulario-base.json"

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

# --- inglés ("Read and Draw") ----------------------------------------

PALABRAS_FUNCIONALES_EN = {
    "a", "an", "the", "this", "that", "these", "those", "some", "any",
    "all", "every", "each", "no", "not", "other", "another", "lots", "lot",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "its", "our", "their", "mine", "yours",
    "myself", "yourself", "himself", "herself", "itself", "ourselves",
    "themselves", "one", "ones",
    "in", "on", "at", "to", "from", "with", "without", "of", "for", "by",
    "about", "into", "onto", "under", "over", "up", "down", "out", "off",
    "near", "next", "behind", "between", "through", "after", "before",
    "around", "across", "along", "past", "till", "than", "like", "as",
    "and", "but", "or", "so", "because", "when", "if", "while", "until",
    "who", "whom", "whose", "which", "what", "where", "why", "how",
    "be", "am", "is", "are", "was", "were", "been", "being", "isn't",
    "aren't", "wasn't", "weren't",
    "do", "does", "did", "done", "don't", "doesn't", "didn't",
    "have", "has", "had", "haven't", "hasn't", "hadn't",
    "can", "can't", "cannot", "could", "couldn't", "will", "won't",
    "would", "shall", "should", "must", "let's",
    "there", "here", "then", "now", "very", "too", "also", "only", "just",
    "again", "still", "yes", "yet", "ever", "never", "always", "often",
    "today", "tomorrow", "yesterday", "tonight",
    "i'm", "you're", "he's", "she's", "it's", "we're", "they're", "i've",
    "we've", "they've", "i'll", "you'll", "he'll", "she'll", "we'll",
    "they'll", "that's", "there's", "what's", "where's", "who's",
}

# Palabras que abren una oración subordinada en inglés: adverbiales
# (because, when, if, while, before, after, until, although), relativas
# y completivas (who, which, that, where, whose). Las mismas formas son
# también palabras interrogativas ("Where is Pip?") o demostrativas
# ("that dog"): una palabra así al principio de una pregunta no cuenta
# (ver contar_subordinantes). "that" demostrativo en medio de una frase
# sí se cuela -- es una aproximación a propósito, igual que en español.
SUBORDINANTES_EN = {
    "because", "when", "if", "while", "before", "after", "until",
    "although", "though", "unless", "whenever", "who", "which", "that",
    "where", "whose",
}

# Fin de frase en inglés: . ! ? … (y la comilla que cierra un diálogo),
# seguido de espacio y de algo que empieza una frase nueva -- una
# mayúscula o una comilla que abre. “Look!” says Dani: después de “!”
# viene una minúscula, así que la frase sigue.
_FIN_DE_FRASE_EN = re.compile(r"(?<=[.!?…])[”’]?\s+(?=[“‘A-ZÁÉÍÓÚÑ])")

# Verbos irregulares (y algún plural) frecuentes: forma -> lema, para que
# "went" no cuente como palabra nueva si "go" ya salió.
IRREGULARES_EN = {
    "went": "go", "goes": "go", "gone": "go", "saw": "see", "seen": "see",
    "came": "come", "ran": "run", "ate": "eat", "eaten": "eat",
    "took": "take", "taken": "take", "made": "make", "said": "say",
    "says": "say", "got": "get", "gave": "give", "given": "give",
    "found": "find", "told": "tell", "thought": "think",
    "brought": "bring", "bought": "buy", "caught": "catch", "sat": "sit",
    "stood": "stand", "flew": "fly", "flies": "fly", "fell": "fall",
    "fallen": "fall", "felt": "feel", "knew": "know", "known": "know",
    "wrote": "write", "written": "write", "drew": "draw", "drawn": "draw",
    "sang": "sing", "sung": "sing", "swam": "swim", "woke": "wake",
    "wore": "wear", "began": "begin", "broke": "break", "broken": "break",
    "built": "build", "chose": "choose", "drank": "drink", "drove": "drive",
    "forgot": "forget", "hid": "hide", "hidden": "hide", "held": "hold",
    "kept": "keep", "lost": "lose", "met": "meet", "rode": "ride",
    "rang": "ring", "sent": "send", "slept": "sleep", "spoke": "speak",
    "threw": "throw", "understood": "understand", "won": "win",
    "heard": "hear", "left": "leave", "meant": "mean", "paid": "pay",
    "sold": "sell", "shook": "shake", "stuck": "stick", "swept": "sweep",
    "taught": "teach", "tore": "tear", "blew": "blow", "grew": "grow",
    "grown": "grow", "lit": "light", "dug": "dig", "fed": "feed",
    "children": "child", "men": "man", "women": "woman", "feet": "foot",
    "teeth": "tooth", "mice": "mouse", "sheep": "sheep", "fish": "fish",
    "people": "person", "leaves": "leaf", "knives": "knife",
    "wolves": "wolf", "shelves": "shelf",
    "better": "good", "best": "good", "worse": "bad", "worst": "bad",
}

# --- polaco («Zdania») ------------------------------------------------

# Palabras funcionales del polaco, en todas las formas que salen en un
# cuaderno para niños: pronombres y posesivos (declinados), demostrativos,
# preposiciones, conjunciones, partículas, interrogativos y "być".
PALABRAS_FUNCIONALES_PL = {
    "ja", "mnie", "mi", "mną", "ty", "ciebie", "cię", "tobie", "ci", "tobą",
    "on", "jego", "go", "niego", "jemu", "mu", "niemu", "nim", "ona", "jej",
    "niej", "ją", "nią", "ono", "my", "nas", "nam", "nami", "wy", "was",
    "wam", "wami", "oni", "one", "ich", "nich", "im", "nimi", "je",
    "się", "siebie", "sobie", "sobą",
    "mój", "moja", "moje", "mojego", "mojej", "mojemu", "moim", "moją",
    "moich", "twój", "twoja", "twoje", "twojego", "twojej", "twoim",
    "twoją", "twoich", "swój", "swoja", "swoje", "swojego", "swojej",
    "swojemu", "swoim", "swoją", "swoich", "swoimi", "nasz", "nasza",
    "nasze", "naszego", "naszej", "naszemu", "naszym", "naszą", "naszych",
    "wasz", "wasza", "wasze",
    "ten", "ta", "to", "te", "tego", "tej", "temu", "tym", "tę", "tą",
    "tych", "tymi", "tamten", "tamta", "tamto", "taki", "taka", "takie",
    "w", "we", "na", "z", "ze", "do", "od", "ode", "o", "po", "przy", "pod",
    "nad", "za", "przed", "między", "bez", "dla", "u", "przez", "ku",
    "obok", "koło", "wokół", "zamiast", "podczas", "oprócz", "wśród",
    "spod", "znad", "zza",
    "i", "a", "ale", "lub", "albo", "czy", "że", "bo", "gdy", "kiedy",
    "jeśli", "jeżeli", "żeby", "aby", "więc", "oraz", "ani", "niż", "jak",
    "ponieważ", "chociaż", "choć", "zanim",
    "nie", "tak", "już", "jeszcze", "też", "także", "tylko", "nawet",
    "bardzo", "może", "no", "oto", "właśnie", "chyba", "zawsze", "nigdy",
    "często", "czasem", "teraz", "potem", "dziś", "dzisiaj", "wczoraj",
    "jutro", "tu", "tutaj", "tam", "gdzie", "wtedy", "zaraz", "trochę",
    "dużo", "mało", "bardziej", "więcej", "mniej",
    "kto", "kogo", "komu", "kim", "co", "czego", "czemu", "czym", "jaki",
    "jaka", "jakie", "który", "która", "które", "którego", "której",
    "dlaczego", "ile",
    "wszystko", "wszyscy", "wszystkie", "wszystkich", "każdy", "każda",
    "każde",
    "być", "jest", "są", "był", "była", "było", "byli", "były", "będzie",
    "będą", "jestem", "jesteś", "jesteśmy",
}

# Las terminaciones que quita lematizar_pl, de la más larga a la más
# corta: de caso y de número (kot-a, kot-em, dom-ami), de verbo (czyt-ać,
# czyt-ają, czyta-ła) y de adjetivo (mał-ego, duż-ymi).
FINALES_PL = (
    "iami", "ami", "ach", "ego", "emu", "owi", "ymi", "imi", "ych", "ich",
    "ają", "eją", "iła", "ała", "ało", "ały", "ali", "ić", "ać", "eć",
    "yć", "uć", "ów", "om", "em", "ie", "ią", "ię", "ej", "ym", "im",
    "ą", "ę", "a", "e", "i", "o", "u", "y", "ł",
)
LETRAS_LEMA_PL = 5


def lematizar_pl(palabra, nombres_propios=frozenset()):
    """El lema aproximado de una palabra polaca: sin la parte de detrás
    del apóstrofo (Toby'ego), sin una terminación (FINALES_PL, dejando
    al menos tres letras) y cortada a LETRAS_LEMA_PL letras. No es un
    lematizador de verdad, igual que el del español y el del inglés:
    sirve para vigilar cuántas palabras nuevas trae cada día."""
    p = palabra.strip(".,;:!?\"„”«»()…—–-").lower().replace("’", "'")
    p = p.split("'")[0]
    if not p or not p.isalpha():
        return None
    if p in PALABRAS_FUNCIONALES_PL or p in nombres_propios:
        return None
    for final in FINALES_PL:
        if p.endswith(final) and len(p) - len(final) >= 3:
            p = p[:-len(final)]
            break
    return p[:LETRAS_LEMA_PL]


IDIOMAS = {
    "es": {"funcionales": PALABRAS_FUNCIONALES, "subordinantes": SUBORDINANTES,
           "fin_de_frase": _FIN_DE_FRASE},
    "en": {"funcionales": PALABRAS_FUNCIONALES_EN, "subordinantes": SUBORDINANTES_EN,
           "fin_de_frase": _FIN_DE_FRASE_EN},
}


def cargar_progresion(libro=FRASES):
    datos = json.loads(libro.progresion.read_text(encoding="utf-8"))
    return {fila["semana"]: fila for fila in datos["semanas"]}


def cargar_familias():
    if not FAMILIAS_FILE.exists():
        return {}
    return json.loads(FAMILIAS_FILE.read_text(encoding="utf-8"))




def lematizar(palabra, familias, nombres_propios=NOMBRES_PROPIOS, idioma="es"):
    if idioma == "en":
        return lematizar_en(palabra, nombres_propios)
    if idioma == "pl":
        return lematizar_pl(palabra, nombres_propios)
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


def _sin_doble(p):
    """runn -> run, stopp -> stop: la consonante que se dobla ante -ing/-ed."""
    if len(p) > 2 and p[-1] == p[-2] and p[-1] not in "aeiouls":
        return p[:-1]
    return p


def lematizar_en(palabra, nombres_propios=frozenset()):
    """El lema aproximado de una palabra inglesa: sin el posesivo, sin
    -s/-es/-ies, sin -ing/-ed (deshaciendo la consonante doblada) y sin
    la -e final -- "like", "likes", "liked" y "liking" acaban todas en
    "lik". No es un lematizador de verdad, igual que el del español:
    sirve para vigilar cuántas palabras nuevas trae cada día."""
    p = palabra.strip(".,;:!?\"“”‘’()…—-").lower().replace("’", "'")
    if p.endswith("'s"):
        p = p[:-2]
    p = p.strip("'")
    if not p or not p.isalpha():
        return None
    if p in PALABRAS_FUNCIONALES_EN or p in nombres_propios:
        return None
    if p in IRREGULARES_EN:
        p = IRREGULARES_EN[p]
    elif p.endswith("ies") and len(p) > 4:
        p = p[:-3] + "y"
    elif p.endswith(("ches", "shes", "sses", "xes", "zes")):
        p = p[:-2]
    elif p.endswith("s") and not p.endswith(("ss", "us", "is")) and len(p) > 3:
        p = p[:-1]
    if p.endswith("ing") and len(p) > 5:
        p = _sin_doble(p[:-3])
    elif p.endswith("ed") and len(p) > 4:
        p = _sin_doble(p[:-2])
    if p.endswith("e") and len(p) > 3:
        p = p[:-1]
    return p


def oraciones_de_parrafos(parrafos, idioma="es"):
    """Las frases de un texto en párrafos ("Leo con lupa", "Read and
    Draw"): cada párrafo (o elemento de lista, o nota) termina al menos
    una frase, y dentro de un párrafo se corta en cada fin de frase (ver
    _FIN_DE_FRASE y _FIN_DE_FRASE_EN)."""
    fin_de_frase = IDIOMAS[idioma]["fin_de_frase"]
    oraciones = []
    for parrafo in parrafos:
        if parrafo.startswith(("> ", "- ")):
            parrafo = parrafo[2:]
        for linea in parrafo.split("\n"):
            oraciones.extend(t for t in fin_de_frase.split(linea.strip()) if t.strip())
    return oraciones


def contar_subordinantes(oraciones, idioma="es"):
    subordinantes = IDIOMAS[idioma]["subordinantes"]
    total = 0
    for oracion in oraciones:
        tokens = oracion.split()
        # En inglés, "Where is Pip?" o "Who is it?": la palabra que abre
        # una pregunta es interrogativa, no un nexo (en español lo dice
        # la tilde: dónde, quién).
        pregunta = idioma == "en" and oracion.rstrip("”’ ").endswith("?")
        for i, token in enumerate(tokens):
            if pregunta and i == 0:
                continue
            if token.strip(".,;:!¡?¿\"«»“”‘’—-()").lower() in subordinantes:
                total += 1
    return total


def oraciones_del_dia(d, dias_por_semana, libro):
    if libro.parrafos:
        return oraciones_de_parrafos(d["texto"], libro.idioma)
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


def vocabulario_base_en(libro):
    """Los lemas que el cuaderno en inglés da por sabidos desde el primer
    día (content/english/vocabulario-base.json): el inglés del colegio."""
    if not VOCABULARIO_BASE_EN.exists():
        return set()
    datos = json.loads(VOCABULARIO_BASE_EN.read_text(encoding="utf-8"))
    vistos = set()
    for palabras in datos["temas"].values():
        for palabra in palabras:
            lema = lematizar_en(palabra, libro.nombres_propios)
            if lema:
                vistos.add(lema)
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
                lema = lematizar(token, familias, libro.nombres_propios, libro.idioma)
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
            fila["subordinadas"] = contar_subordinantes(oraciones, libro.idioma)
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
    if libro.idioma == "en":
        vistos_previos = vocabulario_base_en(libro)
    elif libro.parrafos:
        vistos_previos = lemas_de_libro(FRASES, familias)
    filas = metricas_por_dia(dias, familias, libro, vistos_previos)
    evaluar(filas, progresion)

    if modo_tabla:
        return tabla_markdown(filas, progresion)
    return informe(filas)


if __name__ == "__main__":
    sys.exit(main())
