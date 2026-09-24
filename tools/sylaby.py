#!/usr/bin/env python3
"""Podział na sylaby po polsku i cechy każdej sylaby -- el silabeo del
polaco y los rasgos de cada sílaba, para «Pierwsze słowa», el cuaderno
de primeras palabras en polaco (tools/gen_palabras.py --libro slowa).
Es, para el polaco, lo que tools/silabas.py es para el español.

Dos usos, los mismos:

  - `podziel(slowo)` parte una palabra en sílabas con las reglas de más
    abajo. content/slowa/q*.json escribe cada palabra ya partida a mano
    ("ko-ło"), y tools/gen_palabras.py exige que ese silabeo coincida con
    el de aquí: dos fuentes que tienen que estar de acuerdo. Si una
    palabra real necesita otro silabeo (un prefijo: "przed-szko-le"), va
    en WYJATKI, con su porqué -- nunca se desactiva la comprobación.
  - `cechy(sylaba)` dice qué tiene de difícil una sílaba (cerrada, con
    un dígrafo, blanda, nasal, con dos consonantes delante...) -- con
    eso tools/gen_palabras.py comprueba que cada trimestre solo usa lo
    que le toca (ver ESCALERA_PL allí).

El polaco se lee por sílabas, como el español, pero sus sílabas son
otras. Las reglas (las de la escuela, suficientes para vocabulario
infantil):

  - Cada sílaba tiene una vocal: a, ą, e, ę, i, o, ó, u, y. No hay
    diptongos (na-u-ka, mo-i).
  - ch, cz, dz, dź, dż, rz, sz son UNA consonante y nunca se separan
    (dos letras, un sonido).
  - La i entre una consonante y una vocal no es vocal: ablanda la
    consonante (pies, nie-bo, zie-mia, dzie-ci). Entre dos consonantes,
    o al final, sí lo es (zi-ma, ki-no, dzie-ci).
  - Entre dos vocales, una consonante va con la sílaba siguiente
    (ma-ma, ko-ło). De dos o más, solo la última -- o las dos últimas, si
    son una consonante seguida de r, l, ł o rz, de las que no se separan
    (tr, kr, bl, pł, sł, prz...: ko-bra, ta-bli-ca, ma-sło, po-krzy-wa)
    --, y las demás se quedan con la sílaba anterior (lal-ka, mat-ka,
    ok-no, jabł-ko, łyż-ka, wios-na, sios-tra, mar-chew-ka).

El polaco admite varios silabeos para una misma palabra (sio-stra,
sios-tra, siost-ra): este cuaderno usa siempre el mismo, el de arriba,
para que las sílabas que se imprimen sean previsibles, y porque es el que
deja las sílabas más fáciles -- dos consonantes delante de la vocal solo
cuando la segunda es r, l, ł o rz, que se pronuncian pegadas a la
primera.

Uso de línea de órdenes:
    python3 tools/sylaby.py koło szkoła pies    # para probar a mano
    python3 tools/sylaby.py --prueba            # casos conocidos (CI)
"""

import sys

SAMOGLOSKI = set("aąeęioóuy")

# Dos letras, un sonido. dź y dż antes que dz: se prueban en este orden.
DWUZNAKI = ("dź", "dż", "dz", "ch", "cz", "rz", "sz")

# Las consonantes blandas que se escriben con kreska (y dź).
MIEKKIE = {"ć", "ń", "ś", "ź", "dź"}

# Las que se ablandan delante de una i que es vocal: ci, ni, si, zi, dzi
# se leen ći, ńi, śi, źi, dźi (zi-ma, ci-sza). Delante de otra vocal, la
# i ablanda a cualquier consonante (pies, kie-dy), y eso ya se ve en la
# propia i (ver _jednostki).
ZMIEKCZANE_PRZED_I = {"c", "n", "s", "z", "dz"}

# Consonante + r, l, ł o rz: dos consonantes que no se separan entre
# vocales (van juntas a la sílaba siguiente). t y d + l o ł no están: se
# separan, como en español (kot-let, pod-ło-ga).
GRUPY = {
    "pr", "br", "tr", "dr", "kr", "gr", "fr", "wr", "chr",
    "prz", "brz", "trz", "drz", "krz", "grz", "chrz", "wrz",
    "pl", "bl", "kl", "gl", "fl",
    "pł", "bł", "kł", "gł", "wł", "chł", "sł", "zł", "szł",
    "śl",
}

# Letras que no son del alfabeto polaco: solo salen en palabras de fuera.
OBCE = {"q", "v", "x"}

# Todas las letras que sabe partir: las 32 del alfabeto polaco y esas
# tres. Una palabra con otra (la í de Lucía) no es polaca: los nombres
# del reparto que no lo son se leen de un golpe, sin partirlos (ver
# PALABRAS_GLOBALES_PL en tools/gen_palabras.py).
ALFABET = set("aąbcćdeęfghijklłmnńoóprsśtuwyzźż") | OBCE

# Palabras reales cuyo silabeo no sale de las reglas de arriba (un
# prefijo, una rz que son r y z...). Cada entrada necesita su porqué.
WYJATKI = {}


class Jednostka:
    """Una vocal ('V') o una consonante ('C') de la palabra, con su
    texto; una consonante puede llevar detrás la i que la ablanda
    (miekka_i: pies -> 'pi' + e + s)."""

    __slots__ = ("tipo", "tekst", "miekka_i")

    def __init__(self, tipo, tekst, miekka_i=False):
        self.tipo, self.tekst, self.miekka_i = tipo, tekst, miekka_i

    @property
    def spolgloska(self):
        """La consonante sin la i que la ablanda: 'pi' -> 'p'."""
        return self.tekst[:-1] if self.miekka_i else self.tekst

    def __repr__(self):
        return f"{self.tipo}({self.tekst!r})"


def _jednostki(slowo):
    """Parte la palabra (en minúsculas) en vocales y consonantes: cada
    dígrafo es una consonante, y la i entre una consonante y una vocal se
    queda pegada a la consonante (la ablanda: no es una vocal)."""
    p = slowo.lower()
    wynik = []
    i = 0
    while i < len(p):
        dwie = p[i:i + 2]
        if dwie in DWUZNAKI:
            wynik.append(Jednostka("C", dwie))
            i += 2
            continue
        c = p[i]
        if c in SAMOGLOSKI:
            if (c == "i" and wynik and wynik[-1].tipo == "C" and not wynik[-1].miekka_i
                    and i + 1 < len(p) and p[i + 1] in SAMOGLOSKI):
                wynik[-1] = Jednostka("C", wynik[-1].tekst + "i", miekka_i=True)
            else:
                wynik.append(Jednostka("V", c))
            i += 1
            continue
        if c in ALFABET:
            wynik.append(Jednostka("C", c))
            i += 1
            continue
        raise ValueError(f"«{c}» no es una letra del polaco, en {slowo!r}")
    return wynik


def podziel(slowo):
    """Lista de sílabas de `slowo`, conservando las mayúsculas."""
    klucz = slowo.lower()
    if klucz in WYJATKI:
        czesci = WYJATKI[klucz].split("-")
    else:
        jednostki = _jednostki(slowo)
        samogloski = [k for k, j in enumerate(jednostki) if j.tipo == "V"]
        if not samogloski:
            raise ValueError(f"{slowo!r} no tiene ninguna vocal")
        ciecia = []
        for a, b in zip(samogloski, samogloski[1:]):
            n = b - a - 1  # consonantes entre las dos vocales
            if n == 0:
                ciecie = b
            elif n == 1:
                ciecie = a + 1
            else:
                dwie = jednostki[b - 2].spolgloska + jednostki[b - 1].spolgloska
                ciecie = b - 2 if dwie in GRUPY else b - 1
            ciecia.append(ciecie)
        granice = [0] + ciecia + [len(jednostki)]
        czesci = [
            "".join(j.tekst for j in jednostki[lo:hi])
            for lo, hi in zip(granice, granice[1:])
        ]
    # Las sílabas, con las mayúsculas de la palabra original.
    wynik = []
    pos = 0
    for czesc in czesci:
        wynik.append(slowo[pos:pos + len(czesc)])
        pos += len(czesc)
    return wynik


def cechy(sylaba):
    """Conjunto de rasgos de dificultad de UNA sílaba. Una sílaba sin
    ningún rasgo es "directa": una vocal sola, o una consonante de una
    letra y una vocal (a, ma, ło, ty, ki) -- la única que admite el
    principio del cuaderno. Rasgos posibles:

      zamknieta -- termina en consonante (kot, dom, lal-ka)
      miekka    -- una consonante blanda: ć, ń, ś, ź, dź, o una que
                   ablanda la i (ci, ni, si, zi, dzi; pies, kie-dy)
      znak      -- ó o ż: una letra con su tilde, que suena como otra
                   (ó como u, ż como rz)
      dwuznak   -- un dígrafo: ch, cz, dz, dź, dż, rz, sz
      nosowa    -- una vocal nasal: ą, ę
      grupa     -- dos consonantes delante de la vocal (szko, kra, sło)
      obca      -- q, v, x, que no son del alfabeto polaco
    """
    jednostki = _jednostki(sylaba)
    samogloski = [k for k, j in enumerate(jednostki) if j.tipo == "V"]
    if len(samogloski) != 1:
        raise ValueError(f"una sílaba tiene una vocal: {sylaba!r}")
    k = samogloski[0]
    naglos, jadro, wyglos = jednostki[:k], jednostki[k].tekst, jednostki[k + 1:]
    r = set()
    if wyglos:
        r.add("zamknieta")
    if len(naglos) > 1:
        r.add("grupa")
    for j in naglos + wyglos:
        s = j.spolgloska
        if s in DWUZNAKI:
            r.add("dwuznak")
        if s in MIEKKIE or j.miekka_i:
            r.add("miekka")
        if s == "ż":
            r.add("znak")
        if s in OBCE:
            r.add("obca")
    if jadro in "ąę":
        r.add("nosowa")
    if jadro == "ó":
        r.add("znak")
    if jadro == "i" and naglos and not naglos[-1].miekka_i and naglos[-1].spolgloska in ZMIEKCZANE_PRZED_I:
        r.add("miekka")
    return r


# Casos con respuesta conocida -- uno por cada regla de arriba, y los que
# más fácil se rompen (la i que ablanda, los dígrafos, los grupos de tres
# consonantes). `--prueba` los comprueba todos, en CI antes que nada.
CASOS_PRUEBA = {
    # sílabas directas
    "mama": "ma-ma", "koło": "ko-ło", "łopata": "ło-pa-ta", "kino": "ki-no",
    "oko": "o-ko", "nauka": "na-u-ka", "moi": "mo-i",
    # una consonante entre vocales, y las que terminan en consonante
    "kot": "kot", "ogon": "o-gon", "lalka": "lal-ka", "piłka": "pił-ka",
    "matka": "mat-ka", "okno": "ok-no", "bałwan": "bał-wan",
    # dos consonantes que no se separan (consonante + r, l, ł, rz)
    "kobra": "ko-bra", "tablica": "ta-bli-ca", "masło": "ma-sło",
    "krzesło": "krze-sło", "pokrzywa": "po-krzy-wa", "wiadro": "wia-dro",
    "jabłoń": "ja-błoń", "szuflada": "szu-fla-da",
    # y las que sí (s + consonante, t + ł...)
    "wiosna": "wios-na", "miska": "mis-ka", "kotlet": "kot-let",
    "podłoga": "pod-ło-ga", "łyżka": "łyż-ka", "książka": "książ-ka",
    # tres consonantes: el grupo del final va con la sílaba siguiente
    "siostra": "sios-tra", "jabłko": "jabł-ko", "kostka": "kost-ka",
    "gwiazdka": "gwiazd-ka", "marchewka": "mar-chew-ka",
    # la i que ablanda, y la que es vocal
    "pies": "pies", "niebo": "nie-bo", "ziemia": "zie-mia", "zima": "zi-ma",
    "dzieci": "dzie-ci", "ogień": "o-gień", "radio": "ra-dio",
    "historia": "his-to-ria", "boisko": "bo-is-ko", "Zosia": "Zo-sia",
    # dígrafos, blandas, nasales
    "szkoła": "szko-ła", "czapka": "czap-ka", "rękawiczki": "rę-ka-wicz-ki",
    "dźwig": "dźwig", "dżem": "dżem", "koń": "koń", "słońce": "słoń-ce",
    "pszczoła": "pszczo-ła", "wąż": "wąż", "miód": "miód", "żaba": "ża-ba",
}

CECHY_PRUEBA = {
    "ma": set(), "ło": set(), "ki": set(), "kot": {"zamknieta"},
    "pie": {"miekka"}, "zi": {"miekka"}, "ci": {"miekka"}, "koń": {"miekka", "zamknieta"},
    "sza": {"dwuznak"}, "krze": {"grupa", "dwuznak"}, "rę": {"nosowa"},
    "ża": {"znak"}, "miód": {"miekka", "znak", "zamknieta"}, "ćma": {"miekka", "grupa"},
    "dzie": {"dwuznak", "miekka"}, "szko": {"dwuznak", "grupa"}, "xa": {"obca"},
}


def prueba():
    fallos = []
    for slowo, esperado in CASOS_PRUEBA.items():
        obtenido = "-".join(podziel(slowo))
        if obtenido != esperado:
            fallos.append(f"{slowo}: se esperaba {esperado}, sale {obtenido}")
    for sylaba, esperado in CECHY_PRUEBA.items():
        obtenido = cechy(sylaba)
        if obtenido != esperado:
            fallos.append(
                f"rasgos de «{sylaba}»: se esperaba {sorted(esperado)}, sale {sorted(obtenido)}"
            )
    for f in fallos:
        print(f"FALLO: {f}", file=sys.stderr)
    if fallos:
        return 1
    print(
        f"OK: {len(CASOS_PRUEBA)} palabras silabeadas y {len(CECHY_PRUEBA)} "
        "sílabas clasificadas como se esperaba."
    )
    return 0


def main():
    if "--prueba" in sys.argv:
        return prueba()
    for slowo in sys.argv[1:]:
        sylaby = podziel(slowo)
        detalle = "  ".join(
            f"{s}{'[' + ','.join(sorted(cechy(s))) + ']' if cechy(s) else ''}"
            for s in sylaby
        )
        print(f"{slowo:15} {'-'.join(sylaby):20} {detalle}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
