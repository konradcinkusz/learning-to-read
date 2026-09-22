"""Los cuadernos que genera tools/gen_days.py -- uno por nivel.

El repositorio tiene tres cuadernos, uno por nivel, con los mismos
personajes:

  - nivel 1, "Primeras palabras" (palabras.tex): tiene su propio
    generador, tools/gen_palabras.py, y no pasa por aquí.
  - nivel 2, "Frases" (main.tex, content/q*.json): el cuaderno original.
    Frases completas, de 1 a 4 por página (una más por trimestre).
  - nivel 3, "Leo con lupa" (lupa.tex, content/lupa/q*.json): el año
    siguiente. Oraciones compuestas y subordinadas, en párrafos, y una
    actividad de análisis cada día (dibujar con detalle lo que describe
    el texto, resolver un caso con pistas, una tabla lógica, un mapa, un
    mensaje en clave...). Ver notes/04-nivel-lupa.md.

Los dos últimos comparten generador (tools/gen_days.py), escalera
(tools/metricas.py) y página; todo lo que distingue a uno del otro vive
aquí, en un solo sitio: dónde está su contenido, qué ficheros genera,
qué escalera sigue, cuántas frases lleva una página (o si su texto va
en párrafos), qué tipos de actividad admite, qué instrucción de lectura
y qué tamaño de letra lleva cada trimestre. gen_days.py, metricas.py y
check_pages.py reciben `--libro frases` o `--libro lupa`; sin la opción,
`frases` -- así `python3 tools/gen_days.py` a secas sigue haciendo
exactamente lo mismo que antes de que existiera "Leo con lupa".
"""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

# Los cuadernos comparten calendario: 260 días laborables, cuatro
# trimestres de 13 semanas que son las cuatro estaciones del año (ver
# notes/02-revision-y-plan.md, punto 1).
RANGO_TRIMESTRE = {1: (1, 65), 2: (66, 130), 3: (131, 195), 4: (196, 260)}

# Medalla de fin de trimestre (T1-T3) -- el trimestre 4 termina en el
# diploma final de cada cuaderno (ver PLANTILLA_MEDALLA en tools/gen_days.py).
NOMBRE_MEDALLA_TRIMESTRE = {1: "Otoño", 2: "Invierno", 3: "Primavera"}


@dataclass(frozen=True, eq=False)
class Libro:
    nombre: str
    nivel: int
    dir_contenido: Path
    salida_dias: Path
    salida_clave: Path
    progresion: Path
    # Una instrucción de lectura por trimestre (macros de lang/es.tex).
    instruccion_lectura: dict
    # Tamaño de letra de la caja de lectura por trimestre (índice de
    # \diafuente en preamble.tex, o de \fuenteLupa en preamble-lupa.tex).
    fuente_trimestre: dict
    tipos_validos: frozenset
    # Frases: número exacto de frases por página en cada trimestre.
    # Lupa: None -- el texto va en párrafos libres ("texto" en el JSON, no
    # "oraciones"), y lo que se vigila es la escalera de
    # content/lupa/progresion.json (palabras, frase más larga, oraciones
    # subordinadas), no un número de frases. Es también lo que decide que
    # la página y la clave las genere tools/lupa.py (ver `parrafos`).
    frases_por_trimestre: dict = None
    trimestres_sin_responde: frozenset = frozenset()
    total_dias: int = 260
    rango_trimestre: dict = None
    nombre_medalla: dict = None
    # Nombres propios del reparto: no cuentan como vocabulario nuevo en
    # tools/metricas.py (se repiten constantemente a propósito).
    nombres_propios: frozenset = frozenset()

    def __post_init__(self):
        if self.rango_trimestre is None:
            object.__setattr__(self, "rango_trimestre", dict(RANGO_TRIMESTRE))
        if self.nombre_medalla is None:
            object.__setattr__(self, "nombre_medalla", dict(NOMBRE_MEDALLA_TRIMESTRE))

    @property
    def parrafos(self):
        """True si el texto del día va en párrafos y las actividades son
        las de análisis de tools/lupa.py (el cuaderno "Leo con lupa")."""
        return self.frases_por_trimestre is None

    @property
    def ultimo_dia_trimestre(self):
        return {t: hi for t, (lo, hi) in self.rango_trimestre.items()}


FRASES = Libro(
    nombre="frases",
    nivel=2,
    dir_contenido=CONTENT_DIR,
    salida_dias=CONTENT_DIR / "generated-days.tex",
    salida_clave=CONTENT_DIR / "generated-clave.tex",
    progresion=CONTENT_DIR / "progresion.json",
    instruccion_lectura={
        1: r"\lblInstruccionLecturaUno",
        2: r"\lblInstruccionLecturaDos",
        3: r"\lblInstruccionLecturaTres",
        4: r"\lblInstruccionLecturaCuatro",
    },
    fuente_trimestre={1: 1, 2: 2, 3: 3, 4: 4},
    tipos_validos=frozenset({
        "dibuja", "completa", "copia", "responde", "relaciona", "adivina",
        "crea", "repasa", "rodea", "verdadero_falso", "busca", "ordena",
        "relee", "traza",
    }),
    frases_por_trimestre={1: 1, 2: 2, 3: 3, 4: 4},
    # En el trimestre 1 la niña todavía no compone una respuesta escrita
    # por sí sola -- ver TRIMESTRES_SIN_RESPONDE en tools/gen_days.py.
    trimestres_sin_responde=frozenset({1}),
    nombres_propios=frozenset({
        "lucía", "dani", "toby", "rosa", "marta", "sofía",
        "mamá", "papá", "abuela",
    }),
)

LUPA = Libro(
    nombre="lupa",
    nivel=3,
    dir_contenido=CONTENT_DIR / "lupa",
    salida_dias=CONTENT_DIR / "lupa" / "generated-days.tex",
    salida_clave=CONTENT_DIR / "lupa" / "generated-clave.tex",
    progresion=CONTENT_DIR / "lupa" / "progresion.json",
    instruccion_lectura={
        1: r"\lblLupaInstruccionUno",
        2: r"\lblLupaInstruccionDos",
        3: r"\lblLupaInstruccionTres",
        4: r"\lblLupaInstruccionCuatro",
    },
    # \fuenteLupa (preamble-lupa.tex): más pequeña que la del cuaderno de
    # frases -- hay más texto por página --, pero nunca por debajo de
    # 14 pt.
    fuente_trimestre={1: 1, 2: 2, 3: 3, 4: 4},
    tipos_validos=frozenset({
        # propios de este cuaderno (ver tools/lupa.py)
        "dibuja_detalle", "mapa", "logica", "caso", "errores", "codigo",
        "ficha", "compara", "vinetas",
        # los del cuaderno de frases que siguen teniendo sentido, con más
        # campos
        "responde", "ordena", "relaciona", "verdadero_falso", "adivina",
        "crea", "repasa",
    }),
    nombres_propios=frozenset({
        "lucía", "dani", "toby", "rosa", "marta", "sofía", "hugo", "paco",
        "pedro", "luna", "tomás", "andrés", "bigotes", "martín", "javier",
        "rayo", "mamá", "papá", "abuela",
    }),
)

LIBROS = {libro.nombre: libro for libro in (FRASES, LUPA)}


def libro_desde_argv(argv):
    """`--libro lupa` (o `--libro=lupa`) en argv -> el Libro; sin la
    opción, el cuaderno de frases -- así `python3 tools/gen_days.py` a
    secas sigue haciendo exactamente lo mismo que antes."""
    nombre = "frases"
    for i, arg in enumerate(argv):
        if arg == "--libro" and i + 1 < len(argv):
            nombre = argv[i + 1]
        elif arg.startswith("--libro="):
            nombre = arg.split("=", 1)[1]
    if nombre not in LIBROS:
        raise SystemExit(
            f"ERROR: libro desconocido {nombre!r} -- los que hay: "
            + ", ".join(sorted(LIBROS))
            + " (el de primeras palabras tiene su propio generador,"
            " tools/gen_palabras.py)"
        )
    return LIBROS[nombre]
