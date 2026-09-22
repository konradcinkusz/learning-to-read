#!/usr/bin/env python3
"""Silabeo ortográfico del español y clasificación de cada sílaba, para
el cuaderno de primeras palabras (tools/gen_palabras.py).

Dos usos:

  - `silabear(palabra)` parte una palabra en sílabas con las reglas de
    siempre (ver más abajo). content/palabras/q*.json escribe cada
    palabra ya partida a mano ("pe-lo-ta"), y tools/gen_palabras.py
    exige que ese silabeo coincida con el de aquí: dos fuentes
    independientes que tienen que estar de acuerdo, en vez de fiarse de
    una sola. Si alguna vez una palabra real necesita un silabeo que
    estas reglas no dan (prefijos como "sub-ra-yar"), va en
    EXCEPCIONES, con un comentario -- nunca se desactiva la
    comprobación.
  - `rasgos(silaba)` dice qué tiene de "difícil" una sílaba (cerrada,
    trabada, dígrafo, diptongo, c/g suave, h muda...) -- con eso
    tools/gen_palabras.py comprueba que cada trimestre solo usa las
    estructuras que le tocan (ver ESCALERA allí).

Reglas de silabeo (las de la escuela, suficientes para vocabulario
infantil):

  - ch, ll, rr cuentan como UNA consonante y nunca se separan; qu y gu
    delante de e/i también (la u no suena).
  - Vocales fuertes a, e, o (y í, ú con tilde) no forman diptongo entre
    sí: hiato. Débil sin tilde (i, u, ü) + cualquier otra vocal:
    diptongo (o triptongo, débil + fuerte + débil).
  - "y" es vocal a final de palabra (rey, hoy, Toby) o entre
    consonantes; si no, consonante (yo-yó, ma-yo).
  - Entre dos núcleos: 1 consonante va con la sílaba siguiente; 2 se
    separan salvo que sean un grupo inseparable (pr, bl, tr...); de 3 o
    4, el grupo inseparable final (si lo hay) va con la siguiente y el
    resto se queda con la anterior (ins-tan-te, hom-bro).

Uso de línea de órdenes:
    python3 tools/silabas.py pelota abuela Toby   # para probar a mano
    python3 tools/silabas.py --prueba             # casos conocidos (CI)
"""

import sys
import unicodedata

VOCALES_FUERTES = set("aeoáéó")
VOCALES_DEBILES_TILDE = set("íú")  # se comportan como fuertes: hiato
VOCALES_DEBILES = set("iuü")
VOCALES = VOCALES_FUERTES | VOCALES_DEBILES_TILDE | VOCALES_DEBILES

# Grupos consonánticos que no se separan nunca (sílaba trabada).
GRUPOS_INSEPARABLES = {
    "pr", "pl", "br", "bl", "fr", "fl", "tr", "dr",
    "cr", "cl", "gr", "gl", "kr", "kl",
}

DIGRAFOS = ("ch", "ll", "rr")

# Palabras reales cuyo silabeo no sale de las reglas de arriba. Vacío a
# propósito hasta que haga falta: cada entrada necesita su porqué.
EXCEPCIONES = {}


def _unidades(palabra):
    """Parte la palabra (en minúsculas) en unidades: cada una es
    ('C', texto) o ('V', texto). ch/ll/rr y qu/gu (+e/i) son una sola
    consonante; la 'y' se decide aquí, según su posición."""
    p = palabra.lower()
    unidades = []
    i = 0
    while i < len(p):
        c = p[i]
        par = p[i:i + 2]
        if par in DIGRAFOS:
            unidades.append(("C", par))
            i += 2
            continue
        if par in ("qu", "gu") and i + 2 < len(p) and p[i + 2] in "eiéí":
            unidades.append(("C", par))
            i += 2
            continue
        if c == "y":
            siguiente = p[i + 1] if i + 1 < len(p) else ""
            if siguiente and siguiente in VOCALES:
                unidades.append(("C", c))
            else:
                unidades.append(("V", c))  # rey, hoy, Toby, muy
            i += 1
            continue
        if c in VOCALES:
            unidades.append(("V", c))
        elif c.isalpha():
            unidades.append(("C", c))
        else:
            raise ValueError(f"carácter inesperado {c!r} en {palabra!r}")
        i += 1
    return unidades


def _es_debil(v):
    return v in VOCALES_DEBILES or v == "y"


def _nucleos(unidades):
    """Agrupa vocales seguidas en núcleos, separando los hiatos. Devuelve
    una lista de ('C', texto) / ('N', texto)."""
    salida = []
    for tipo, texto in unidades:
        if tipo == "C":
            salida.append(("C", texto))
            continue
        if salida and salida[-1][0] == "N":
            previo = salida[-1][1]
            ultima = previo[-1]
            # hiato: dos vocales que no son débiles sin tilde
            if not (_es_debil(ultima) or _es_debil(texto)):
                salida.append(("N", texto))
                continue
            # un triptongo como mucho: débil + fuerte + débil
            if len(previo) >= 3 or (len(previo) == 2 and not _es_debil(texto)):
                salida.append(("N", texto))
                continue
            salida[-1] = ("N", previo + texto)
        else:
            salida.append(("N", texto))
    return salida


def silabear(palabra):
    """Lista de sílabas de `palabra`, conservando mayúsculas y tildes."""
    clave = palabra.lower()
    if clave in EXCEPCIONES:
        partes = EXCEPCIONES[clave].split("-")
    else:
        piezas = _nucleos(_unidades(palabra))
        indices = [i for i, (t, _) in enumerate(piezas) if t == "N"]
        if not indices:
            raise ValueError(f"{palabra!r} no tiene ninguna vocal")
        cortes = []  # posición (en piezas) donde empieza cada sílaba, salvo la primera
        for a, b in zip(indices, indices[1:]):
            consonantes = [piezas[k][1] for k in range(a + 1, b)]
            n = len(consonantes)
            if n == 0:
                corte = b
            elif n == 1:
                corte = a + 1
            else:
                ultimas = "".join(consonantes[-2:])
                if ultimas in GRUPOS_INSEPARABLES:
                    corte = b - 2
                else:
                    corte = b - 1
            cortes.append(corte)
        limites = [0] + cortes + [len(piezas)]
        partes = [
            "".join(t for _, t in piezas[lo:hi])
            for lo, hi in zip(limites, limites[1:])
        ]
    # Devolver las sílabas con las mayúsculas originales.
    salida = []
    pos = 0
    for parte in partes:
        salida.append(palabra[pos:pos + len(parte)])
        pos += len(parte)
    return salida


def _sin_tilde(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def rasgos(silaba):
    """Conjunto de rasgos de dificultad de UNA sílaba. Una sílaba sin
    ningún rasgo es "directa" (V o CV con una consonante de las
    regulares: ma, pe, lo, a) -- la única que admite el principio del
    cuaderno. Rasgos posibles:

      cerrada   -- termina en consonante (sol, pan, ár-bol)
      suave     -- c/g suaves: ce, ci, ge, gi
      h         -- h muda
      trabada   -- dos consonantes delante de la vocal (pla, tre, flor)
      digrafo   -- ch, ll, rr, qu, gu (+e/i), gü
      diptongo  -- dos o tres vocales en la misma sílaba (bue, cie, hoy)
      rara      -- k, w, x, o la "y" como vocal (Toby, rey)
    """
    unidades = _unidades(silaba)
    r = set()
    tipos = [t for t, _ in unidades]
    if "V" not in tipos:
        raise ValueError(f"sílaba sin vocal: {silaba!r}")
    primera_v = tipos.index("V")
    ultima_v = len(tipos) - 1 - tipos[::-1].index("V")
    ataque = [t for _, t in unidades[:primera_v]]
    nucleo = [t for _, t in unidades[primera_v:ultima_v + 1]]
    coda = [t for _, t in unidades[ultima_v + 1:]]

    if coda:
        r.add("cerrada")
    if len(nucleo) > 1:
        r.add("diptongo")
    if len(ataque) > 1:
        r.add("trabada")
    for c in ataque + coda:
        if c in DIGRAFOS or c in ("qu", "gu"):
            r.add("digrafo")
        if c == "h":
            r.add("h")
        if c in ("k", "w", "x"):
            r.add("rara")
    if "ü" in nucleo:
        r.add("digrafo")
    if "y" in nucleo:
        r.add("rara")
    if ataque and ataque[-1] in ("c", "g") and _sin_tilde(nucleo[0]) in ("e", "i"):
        r.add("suave")
    return r


# Casos con respuesta conocida -- uno por cada regla de arriba, y los
# que más fácil se rompen (hiatos, h intercalada, "y", qu/gu/gü, grupos
# de tres consonantes). `--prueba` los comprueba todos; si alguien toca
# las reglas y rompe uno, CI lo dice antes de que se note en el cuaderno.
CASOS_PRUEBA = {
    "mamá": "ma-má", "pelota": "pe-lo-ta", "Toby": "To-by", "Lucía": "Lu-cí-a",
    "sol": "sol", "árbol": "ár-bol", "bufanda": "bu-fan-da", "ratón": "ra-tón",
    "perro": "pe-rro", "calle": "ca-lle", "leche": "le-che", "queso": "que-so",
    "guitarra": "gui-ta-rra", "pingüino": "pin-güi-no", "canguro": "can-gu-ro",
    "libro": "li-bro", "flor": "flor", "atleta": "at-le-ta", "hombro": "hom-bro",
    "instante": "ins-tan-te", "abstracto": "abs-trac-to",
    "abuela": "a-bue-la", "nieve": "nie-ve", "lluvia": "llu-via",
    "paraguas": "pa-ra-guas", "buey": "buey", "hoy": "hoy", "yoyó": "yo-yó",
    "mayo": "ma-yo", "leer": "le-er", "león": "le-ón", "poeta": "po-e-ta",
    "raíz": "ra-íz", "país": "pa-ís", "río": "rí-o", "baúl": "ba-úl",
    "búho": "bú-ho", "ahora": "a-ho-ra", "almohada": "al-mo-ha-da",
    "zanahoria": "za-na-ho-ria", "koala": "ko-a-la", "ñu": "ñu",
}


def prueba():
    fallos = [
        (palabra, esperado, "-".join(silabear(palabra)))
        for palabra, esperado in CASOS_PRUEBA.items()
        if "-".join(silabear(palabra)) != esperado
    ]
    for palabra, esperado, obtenido in fallos:
        print(f"FALLO: {palabra}: se esperaba {esperado}, sale {obtenido}", file=sys.stderr)
    if fallos:
        return 1
    print(f"OK: {len(CASOS_PRUEBA)} palabras silabeadas como se esperaba.")
    return 0


def main():
    if "--prueba" in sys.argv:
        return prueba()
    for palabra in sys.argv[1:]:
        silabas = silabear(palabra)
        detalle = "  ".join(
            f"{s}{'[' + ','.join(sorted(rasgos(s))) + ']' if rasgos(s) else ''}"
            for s in silabas
        )
        print(f"{palabra:15} {'-'.join(silabas):20} {detalle}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
