#!/usr/bin/env python3
"""La fonética del cuaderno de primeras palabras en inglés, «First
Words» (firstwords.tex, ver notes/06-first-words.md): cómo se parte una
palabra inglesa en sus sonidos, y qué se puede leer en cada momento del
año. Es, para el inglés, lo que tools/silabas.py es para el español.

En español se aprende a leer por sílabas (pe·lo·ta); en inglés, por
sonidos (phonics): se dice cada sonido y se juntan -- c, a, t: cat. La
unidad es el GRAFEMA, la letra o el grupo de letras que se lee como un
solo sonido:

  - una letra:            c-a-t, P-i-p;
  - dos o tres letras:    sh-i-p, n-igh-t, d-u-ck, b-e-ll;
  - la "e mágica" (split digraph): en cake, la a y la e del final son un
    solo sonido, que se escribe a_e -- "c-a_e-k" -- y en la página se
    marca con un arco que une las dos letras.

En la página, cada grafema lleva debajo su "botón": un punto si es una
sola letra, una raya si son varias, un arco si es una e mágica. Es la
forma en que se enseña a leer en los colegios ingleses (sound buttons).

Cada palabra de las tarjetas se escribe en el JSON ya partida
("sh-ee-p"), y tools/gen_palabras.py exige que ese partido coincida con
el automático de aquí, segmentar(): un emparejamiento voraz, de
izquierda a derecha, que prueba primero los grafemas más largos (igh
antes que i, sh antes que s), y después la regla de la e mágica. Dos
fuentes que tienen que estar de acuerdo, como el silabeo del español.

Uso:
    python3 tools/fonetica.py --prueba     # comprueba segmentar() contra
                                           # palabras con respuesta conocida
    python3 tools/fonetica.py cat sheep    # enseña cómo parte unas palabras
"""

import re
import sys

# --------------------------------------------------------------------
# Los grafemas, por tramos del año (acumulativos)
# --------------------------------------------------------------------

# Otoño, semanas 1-5: una letra = un sonido. Todas las letras menos q, x
# e y (la x son dos sonidos, la q va siempre con u, y la y es a veces
# consonante y a veces vocal): palabras de tres sonidos como mucho, sin
# dos consonantes juntas -- cat, van, Pip, mum, dog, sun.
GRAFEMAS_T1A = frozenset("abcdefghijklmnoprstuvwz")

# Otoño, semanas 6-13: las letras dobles, que se leen como una (duck,
# bell, kiss, egg), la x (box), la y del principio de palabra (yes) y
# qu (quack).
GRAFEMAS_T1B = frozenset({"ck", "ff", "ll", "ss", "zz", "gg", "x", "y", "qu"})

# Invierno: dos letras (o tres) para un sonido -- ship, chip, bath, king;
# rain, tree, night, boat, moon, star, fork, turn, cow, coin, ear, hair,
# letter -- y el resto de consonantes dobles (letter, dinner).
GRAFEMAS_T2 = frozenset({
    "sh", "ch", "th", "ng",
    "ai", "ee", "igh", "oa", "oo", "ar", "or", "ur", "ow", "oi",
    "ear", "air", "ure", "er",
    "bb", "dd", "mm", "nn", "pp", "rr", "tt",
})

# Primavera: otras formas de escribir los mismos sonidos -- day, cloud,
# pie, sea, boy, bird, blue, saw, new, toe, key, whale, phone, catch,
# bridge -- y la e mágica (cake, bike, bone, cube, these).
GRAFEMAS_T3 = frozenset({
    "ay", "ou", "ie", "ea", "oy", "ir", "ue", "aw", "ew", "oe", "au", "ey",
    "wh", "ph", "tch", "dge",
    "a_e", "e_e", "i_e", "o_e", "u_e",
})

# Todos los del cuaderno. Una q sola (sin u) no es ninguno: una palabra
# que la tenga no cabe en ningún tramo de la escalera.
TODOS = GRAFEMAS_T1A | GRAFEMAS_T1B | GRAFEMAS_T2 | GRAFEMAS_T3

# Una palabra de ejemplo para cada grafema, en el orden en que se
# enseñan: es la tabla de sonidos del principio del cuaderno
# (frontmatter/firstwords/sonidos.tex, que tools/gen_palabras.py genera
# a partir de aquí y de su escalera). Cada ejemplo se puede leer en
# cuanto llega su sonido -- con los que ya se saben entonces, y cabe en
# la escalera de esa semana -- y casi siempre es algo que se puede
# dibujar. tools/gen_palabras.py lo comprueba, y también que no falte ni
# sobre ningún grafema.
EJEMPLOS = {
    # Otoño, semanas 1-5.
    "s": "sun", "a": "cat", "t": "top", "p": "pen", "i": "pin", "n": "net",
    "m": "mum", "d": "dog", "g": "leg", "o": "mop", "c": "cup", "k": "kit",
    "e": "hen", "u": "bus", "r": "red", "h": "hat", "b": "bed", "f": "fan",
    "l": "log", "j": "jam", "v": "van", "w": "web", "z": "zip",
    # Otoño, semanas 6-13.
    "ck": "duck", "ff": "off", "ll": "bell", "ss": "kiss", "zz": "buzz",
    "gg": "egg", "x": "box", "y": "yes", "qu": "quack",
    # Invierno.
    "sh": "ship", "ch": "chip", "th": "bath", "ng": "king", "ai": "rain",
    "ee": "feet", "igh": "night", "oa": "boat", "oo": "moon", "ar": "car",
    "or": "fork", "ur": "church", "ow": "cow", "oi": "coin", "ear": "beard",
    "air": "hair", "ure": "cure", "er": "letter",
    "bb": "rubber", "dd": "teddy", "mm": "hammer", "nn": "dinner",
    "pp": "puppy", "rr": "cherry", "tt": "otter",
    # Primavera.
    "ay": "day", "ou": "cloud", "ie": "pie", "ea": "sea", "oy": "boy",
    "ir": "bird", "ue": "blue", "aw": "saw", "ew": "new", "oe": "toe",
    "au": "launch", "ey": "key", "wh": "whale", "ph": "phone",
    "tch": "witch", "dge": "bridge",
    "a_e": "cake", "e_e": "these", "i_e": "bike", "o_e": "bone", "u_e": "cube",
}

# Los que se pueden emparejar al partir una palabra, de más largo a más
# corto (la e mágica no: se reconoce después, ver segmentar()).
_POR_LONGITUD = sorted(
    (g for g in TODOS if "_" not in g and len(g) > 1), key=len, reverse=True
)

VOCALES_SIMPLES = frozenset("aeiou")

# Consonantes (grafemas) que suenan como una s o una z: detrás de ellas,
# la terminación -es de un plural se pronuncia (boxes, wishes, buses),
# así que no es la e mágica de un plural como cakes.
SIBILANTES = frozenset({"s", "z", "x", "sh", "ch", "tch", "dge"})

# Grafemas que son una vocal (un sonido vocálico). Todo lo demás es
# consonante -- salvo la y, que depende de dónde esté: al principio de
# la palabra es consonante (yes), en cualquier otro sitio es vocal
# (happy, fly).
VOCALES = VOCALES_SIMPLES | frozenset({
    "ai", "ee", "igh", "oa", "oo", "ar", "or", "ur", "ow", "oi", "ear",
    "air", "ure", "er", "ay", "ou", "ie", "ea", "oy", "ir", "ue", "aw",
    "ew", "oe", "au", "ey", "a_e", "e_e", "i_e", "o_e", "u_e",
})


def es_vocal(grafema, posicion):
    g = grafema.lower()
    if g == "y":
        return posicion > 0
    return g in VOCALES


# --------------------------------------------------------------------
# Partir una palabra
# --------------------------------------------------------------------

class ErrorFonetica(ValueError):
    pass


def segmentar(palabra):
    """'sheep' -> ['sh', 'ee', 'p']; 'cake' -> ['c', 'a_e', 'k'].
    Conserva las mayúsculas de la palabra (Pip -> ['P', 'i', 'p'])."""
    if not palabra.isalpha() or not palabra.isascii():
        raise ErrorFonetica(f"«{palabra}» no es una palabra inglesa de letras sueltas")
    minus = palabra.lower()
    grafemas = []
    i = 0
    while i < len(minus):
        for g in _POR_LONGITUD:
            if minus.startswith(g, i):
                break
        else:
            g = minus[i]
        # Una vocal con r (er, ar, ear...) justo antes de otra r: la r va
        # con la siguiente, que es una rr -- cherry es ch-e-rr-y, no
        # ch-er-r-y; carrot, c-a-rr-o-t; sorry, s-o-rr-y.
        if len(g) > 1 and g.endswith("r") and minus.startswith("r", i + len(g)):
            g = g[:-1]
        grafemas.append(palabra[i:i + len(g)])
        i += len(g)
    # La e mágica: vocal simple + UNA consonante + e final (cake, bike,
    # these, whale). Una consonante doble (little) o una vocal de dos
    # letras (horse: or + se) no la forman.
    if (
        len(grafemas) >= 3
        and grafemas[-1].lower() == "e"
        and grafemas[-3].lower() in VOCALES_SIMPLES
        and not es_vocal(grafemas[-2], len(grafemas) - 2)
        and not _es_doble(grafemas[-2])
    ):
        vocal = grafemas[-3]
        grafemas = grafemas[:-3] + [vocal + "_e", grafemas[-2]]
    # Y el plural (o la tercera persona) de una palabra con e mágica:
    # cakes es cake + s, c-a_e-k-s, no c-a-k-e-s. Detrás de una
    # consonante que suena como s (boxes, buses) la -es sí se pronuncia,
    # y no es una e mágica.
    elif (
        len(grafemas) >= 4
        and grafemas[-1].lower() == "s"
        and grafemas[-2].lower() == "e"
        and grafemas[-4].lower() in VOCALES_SIMPLES
        and not es_vocal(grafemas[-3], len(grafemas) - 3)
        and not _es_doble(grafemas[-3])
        and grafemas[-3].lower() not in SIBILANTES
    ):
        vocal = grafemas[-4]
        grafemas = grafemas[:-4] + [vocal + "_e", grafemas[-3], grafemas[-1]]
    _comprobar_trampas(palabra, minus, grafemas)
    return grafemas


def _comprobar_trampas(palabra, minus, grafemas):
    """Palabras que se pueden partir, pero que no se leen como dicen sus
    botones: una letra que no suena (house, knee, lamb, ghost), una c que
    suena /s/ (nice, city), la a de ball o la o de cold. Mejor un error
    que una tarjeta con un botón debajo de una letra que no suena, o con
    un sonido que no es el que se ha aprendido."""
    partido = "-".join(grafemas)
    if (
        len(grafemas) >= 3
        and grafemas[-1].lower() == "e"
        and not es_vocal(grafemas[-2], len(grafemas) - 2)
    ):
        raise ErrorFonetica(
            f"«{palabra}» ({partido}) termina en una e que no suena y que no "
            "es una e mágica: no se puede leer sonido a sonido"
        )
    if (
        minus.startswith(("kn", "wr", "gn")) or minus.endswith("mb")
        or "gh" in minus.replace("igh", "") or "eigh" in minus
    ):
        raise ErrorFonetica(
            f"«{palabra}» ({partido}) tiene una letra que no suena "
            "(kn, wr, gn, mb, gh): no se puede leer sonido a sonido"
        )
    if re.search(r"c[eiy]", minus):
        raise ErrorFonetica(
            f"«{palabra}» ({partido}) tiene una c que suena /s/ (ce, ci, cy): "
            "en este cuaderno la c suena siempre como en cat"
        )
    if re.search(r"all(?![aeiouy])|old|al[kfm]|wa(sh|tch|nt|sp|ter|nd)", minus):
        raise ErrorFonetica(
            f"«{palabra}» ({partido}): la a de ball, talk o want y la o de "
            "cold no suenan como en cat y en dog -- no se puede leer sonido "
            "a sonido"
        )
    # El pasado en -ed detrás de otra vocal (played, hugged): esa e no
    # suena -- salvo detrás de t o d (landed, painted). En bed o shed, la
    # e es la única vocal, y sí suena.
    if (
        len(grafemas) >= 3
        and [g.lower() for g in grafemas[-2:]] == ["e", "d"]
        and any(es_vocal(g, i) for i, g in enumerate(grafemas[:-2]))
        and minus[-3:-2] not in ("t", "d")
    ):
        raise ErrorFonetica(
            f"«{palabra}» ({partido}): la e del pasado en -ed no suena -- no "
            "se puede leer sonido a sonido"
        )
    # Una consonante + le, en plural (apples, tables): esa e tampoco
    # suena. En singular (apple) ya lo para la e muda de arriba.
    if (
        len(grafemas) >= 4
        and [g.lower() for g in grafemas[-3:]] == ["l", "e", "s"]
        and not es_vocal(grafemas[-4], len(grafemas) - 4)
    ):
        raise ErrorFonetica(
            f"«{palabra}» ({partido}) termina en -les detrás de una "
            "consonante, con una e que no suena"
        )


def _es_doble(grafema):
    g = grafema.lower()
    return len(g) == 2 and g[0] == g[1]


def unir(grafemas):
    """El inverso de segmentar(): ['c', 'a_e', 'k'] -> 'cake', y
    ['c', 'a_e', 'k', 's'] -> 'cakes'."""
    letras = []
    for i, g in enumerate(grafemas):
        if "_" not in g:
            letras.append(g)
            continue
        resto = [x.lower() for x in grafemas[i + 2:]]
        if i + 1 >= len(grafemas) or resto not in ([], ["s"]):
            raise ErrorFonetica(
                f"«{'-'.join(grafemas)}»: la e mágica ({g}) solo puede ir en "
                "el penúltimo sonido (c-a_e-k), o en el antepenúltimo de un "
                "plural (c-a_e-k-s)"
            )
        vocal, e = g.split("_")
        letras.append(vocal)
        letras.append(grafemas[i + 1])
        letras.append(e)
        letras.extend(grafemas[i + 2:])
        break
    return "".join(letras)


def leer_escrita(escrita):
    """'sh-ee-p' -> ('sheep', ['sh', 'ee', 'p']), comprobando que el
    partido de a mano es el mismo que el automático."""
    if not escrita or escrita != escrita.strip() or " " in escrita:
        raise ErrorFonetica(f"palabra mal escrita: {escrita!r}")
    grafemas = escrita.split("-")
    if any(not g for g in grafemas):
        raise ErrorFonetica(f"«{escrita}»: un guion de más")
    palabra = unir(grafemas)
    automatico = EXCEPCIONES.get(palabra.lower())
    if automatico is None:
        automatico = [g.lower() for g in segmentar(palabra)]
    if [g.lower() for g in grafemas] != automatico:
        raise ErrorFonetica(
            f"«{escrita}» -- el partido automático da «{'-'.join(automatico)}». "
            "Si el de a mano es el correcto, añade la palabra a EXCEPCIONES "
            "en tools/fonetica.py, con su porqué"
        )
    return palabra, grafemas


# Palabras que el emparejamiento voraz parte mal, con su partido bueno y
# su porqué. Vacío por ahora: las palabras del cuaderno se eligen para
# que se lean como se escriben.
EXCEPCIONES = {}


def rasgos_de(grafemas):
    """Lo que tiene una palabra ya partida: sus grafemas (en minúscula),
    si tiene dos consonantes seguidas (un grupo: frog, nest), y cuántos
    sonidos."""
    minus = [g.lower() for g in grafemas]
    grupo = any(
        not es_vocal(a, i) and not es_vocal(b, i + 1)
        for i, (a, b) in enumerate(zip(minus, minus[1:]))
    )
    return {"grafemas": minus, "grupo": grupo, "sonidos": len(minus)}


def es_grafema_de_varias(grafema):
    return len(grafema.replace("_", "")) > 1 and "_" not in grafema


# --------------------------------------------------------------------
# Las palabras que se aprenden de memoria (tricky words)
# --------------------------------------------------------------------

# Palabras muy frecuentes que no se leen como se escriben (the, was,
# said) o que se leen antes de haber visto sus sonidos (he, my): se
# aprenden de memoria, enteras. Solo hacen falta en las frases del
# verano (y en las actividades de ese trimestre); el cuaderno las
# presenta antes, en primavera (ver notes/06-first-words.md). Las de las
# listas de los colegios ingleses, más a, is, his, has, as, of.
TRICKY = frozenset({
    "the", "to", "i", "no", "go", "into",
    "he", "she", "we", "me", "be", "was", "you", "they", "all", "are",
    "my", "her",
    "said", "have", "like", "so", "do", "some", "come", "were", "there",
    "little", "one", "when", "out", "what",
    "oh", "their", "people", "mr", "mrs", "looked", "called", "asked",
    "could",
    "a", "is", "his", "has", "as", "of",
})


# --------------------------------------------------------------------
# Prueba
# --------------------------------------------------------------------

# Palabras con su partido conocido: cada grafema, la e mágica, la y
# consonante y vocal, las letras dobles, los grafemas de tres letras.
PRUEBA = {
    "cat": "c-a-t", "Pip": "P-i-p", "van": "v-a-n", "up": "u-p",
    "duck": "d-u-ck", "bell": "b-e-ll", "kiss": "k-i-ss", "egg": "e-gg",
    "box": "b-o-x", "yes": "y-e-s", "quack": "qu-a-ck", "buzz": "b-u-zz",
    "ship": "sh-i-p", "chip": "ch-i-p", "bath": "b-a-th", "king": "k-i-ng",
    "rain": "r-ai-n", "tree": "t-r-ee", "night": "n-igh-t", "boat": "b-oa-t",
    "moon": "m-oo-n", "book": "b-oo-k", "star": "s-t-ar", "fork": "f-or-k",
    "turn": "t-ur-n", "cow": "c-ow", "coin": "c-oi-n", "ear": "ear",
    "chair": "ch-air", "letter": "l-e-tt-er", "dinner": "d-i-nn-er",
    "sheep": "sh-ee-p", "queen": "qu-ee-n", "three": "th-r-ee",
    "day": "d-ay", "cloud": "c-l-ou-d", "pie": "p-ie", "tea": "t-ea",
    "boy": "b-oy", "bird": "b-ir-d", "blue": "b-l-ue", "saw": "s-aw",
    "new": "n-ew", "toe": "t-oe", "key": "k-ey", "whale": "wh-a_e-l",
    "phone": "ph-o_e-n", "catch": "c-a-tch", "bridge": "b-r-i-dge",
    "cake": "c-a_e-k", "bike": "b-i_e-k", "bone": "b-o_e-n",
    "cube": "c-u_e-b", "these": "th-e_e-s", "snake": "s-n-a_e-k",
    "happy": "h-a-pp-y", "fly": "f-l-y", "plant": "p-l-a-n-t",
    "spring": "s-p-r-i-ng", "rabbit": "r-a-bb-i-t",
    "cherry": "ch-e-rr-y", "carrot": "c-a-rr-o-t", "sorry": "s-o-rr-y",
    "hurry": "h-u-rr-y", "mirror": "m-i-rr-or", "he": "h-e", "the": "th-e",
    "cakes": "c-a_e-k-s", "bikes": "b-i_e-k-s", "shines": "sh-i_e-n-s",
    "waves": "w-a_e-v-s", "hates": "h-a_e-t-s", "boxes": "b-o-x-e-s",
    "wishes": "w-i-sh-e-s", "buses": "b-u-s-e-s", "shed": "sh-e-d",
    "landed": "l-a-n-d-e-d", "treasure": "t-r-ea-s-ure",
}

# Palabras que se pueden partir pero no leer sonido a sonido (ver
# _comprobar_trampas): segmentar() tiene que rechazarlas todas.
PRUEBA_TRAMPAS = [
    "house", "horse", "apple", "cheese", "knee", "write", "gnome", "lamb",
    "ghost", "eight", "nice", "city", "juice", "ball", "small", "cold",
    "talk", "walk", "half", "want", "wash", "water", "played", "hugged",
    "liked", "apples", "tables",
]


def prueba():
    fallos = []
    for palabra, esperado in PRUEBA.items():
        obtenido = "-".join(segmentar(palabra))
        if obtenido != esperado:
            fallos.append(f"  {palabra}: se esperaba {esperado}, sale {obtenido}")
        if unir(esperado.split("-")) != palabra:
            fallos.append(f"  {palabra}: unir({esperado}) no devuelve la palabra")
    for palabra in PRUEBA_TRAMPAS:
        try:
            obtenido = "-".join(segmentar(palabra))
        except ErrorFonetica:
            continue
        fallos.append(f"  {palabra}: se esperaba un error, sale {obtenido}")
    for grafema, palabra in EJEMPLOS.items():
        if grafema not in (g.lower() for g in segmentar(palabra)):
            fallos.append(f"  EJEMPLOS: «{palabra}» no tiene el sonido «{grafema}»")
    if fallos:
        print("FALLOS en tools/fonetica.py:\n" + "\n".join(fallos))
        return 1
    print(f"OK: {len(PRUEBA)} palabras partidas en sonidos como se esperaba, "
          f"{len(PRUEBA_TRAMPAS)} trampas rechazadas y {len(EJEMPLOS)} "
          "ejemplos de la tabla de sonidos con su sonido.")
    return 0


def main(argv):
    if "--prueba" in argv:
        return prueba()
    for palabra in argv:
        grafemas = segmentar(palabra)
        r = rasgos_de(grafemas)
        print(f"{palabra}: {'-'.join(grafemas)} ({r['sonidos']} sonidos"
              f"{', con grupo' if r['grupo'] else ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
