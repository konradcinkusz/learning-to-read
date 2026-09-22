"""Los libros que se construyen en este repositorio -- uno por nivel.

Todo lo que distingue un libro de otro vive aquí, en un solo sitio:
dónde está su contenido, qué ficheros genera, qué escalera de
progresión sigue, cuántas frases lleva una página (o si su texto va en
párrafos libres), qué tipos de actividad admite, qué instrucción de
lectura y qué tamaño de letra lleva cada trimestre...

tools/gen_days.py, tools/metricas.py y tools/check_pages.py reciben un
libro (`--libro nivel1` o `--libro nivel2`; sin la opción, `nivel1`)
en vez de tener cada uno sus propias constantes -- así el motor es el
mismo para los dos niveles, y añadir el nivel 2 no cambia ni una línea
del .tex que genera el nivel 1.

- nivel1 -- "Aprendo a leer": frases completas, 1 -> 4 frases por
  página (una más por trimestre). Contenido en content/q*.json.
- nivel2 -- "Leo con lupa": oraciones compuestas y subordinadas, en
  párrafos, y una actividad de análisis cada día (dibujar con detalle
  lo que describe el texto, resolver un caso con pistas, una tabla
  lógica, un mapa, un mensaje en clave...). Contenido en
  content/nivel2/q*.json. Ver notes/03-nivel2.md.
"""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

# Los dos libros comparten calendario: 260 días laborables, cuatro
# trimestres de 13 semanas que son las cuatro estaciones del año (ver
# notes/02-revision-y-plan.md, punto 1).
RANGO_TRIMESTRE = {1: (1, 65), 2: (66, 130), 3: (131, 195), 4: (196, 260)}

# Medalla de fin de trimestre (T1-T3) -- el trimestre 4 termina en el
# diploma final de cada libro (ver PLANTILLA_MEDALLA en tools/gen_days.py).
NOMBRE_MEDALLA_TRIMESTRE = {1: "Otoño", 2: "Invierno", 3: "Primavera"}


@dataclass(frozen=True)
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
    # \diafuente en preamble.tex).
    fuente_trimestre: dict
    tipos_validos: frozenset
    # Nivel 1: número exacto de frases por página en cada trimestre.
    # Nivel 2: None -- el texto va en párrafos libres, y lo que se
    # vigila es la escalera de content/nivel2/progresion.json (palabras,
    # frase más larga, oraciones subordinadas), no un número de frases.
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
    def ultimo_dia_trimestre(self):
        return {t: hi for t, (lo, hi) in self.rango_trimestre.items()}


NIVEL1 = Libro(
    nombre="nivel1",
    nivel=1,
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

NIVEL2 = Libro(
    nombre="nivel2",
    nivel=2,
    dir_contenido=CONTENT_DIR / "nivel2",
    salida_dias=CONTENT_DIR / "nivel2" / "generated-days.tex",
    salida_clave=CONTENT_DIR / "nivel2" / "generated-clave.tex",
    progresion=CONTENT_DIR / "nivel2" / "progresion.json",
    instruccion_lectura={
        1: r"\lblInstruccionLecturaNivelDosUno",
        2: r"\lblInstruccionLecturaNivelDosDos",
        3: r"\lblInstruccionLecturaNivelDosTres",
        4: r"\lblInstruccionLecturaNivelDosCuatro",
    },
    # \diafuente 5-8: más pequeños que los del nivel 1 (hay más texto
    # por página), pero nunca por debajo de 13,5 pt -- ver preamble.tex.
    fuente_trimestre={1: 5, 2: 6, 3: 7, 4: 8},
    tipos_validos=frozenset({
        # propios del nivel 2 (ver tools/nivel2.py)
        "dibuja_detalle", "mapa", "logica", "caso", "errores", "codigo",
        "ficha", "compara", "vinetas",
        # los del nivel 1 que siguen teniendo sentido, con más campos
        "responde", "ordena", "relaciona", "verdadero_falso", "adivina",
        "crea", "repasa",
    }),
    nombres_propios=frozenset({
        "lucía", "dani", "toby", "rosa", "marta", "sofía", "hugo", "paco",
        "pedro", "luna", "tomás", "andrés", "bigotes", "martín", "javier",
        "rayo", "mamá", "papá", "abuela",
    }),
)

LIBROS = {libro.nombre: libro for libro in (NIVEL1, NIVEL2)}


def libro_desde_argv(argv):
    """`--libro nivel2` (o `--libro=nivel2`) en argv -> el Libro; sin la
    opción, el nivel 1 -- así `python3 tools/gen_days.py` a secas sigue
    haciendo exactamente lo mismo que antes de que existiera el nivel 2."""
    nombre = "nivel1"
    for i, arg in enumerate(argv):
        if arg == "--libro" and i + 1 < len(argv):
            nombre = argv[i + 1]
        elif arg.startswith("--libro="):
            nombre = arg.split("=", 1)[1]
    if nombre not in LIBROS:
        raise SystemExit(
            f"ERROR: libro desconocido {nombre!r} -- los que hay: "
            + ", ".join(sorted(LIBROS))
        )
    return LIBROS[nombre]


def posicionales(argv):
    """Los argumentos de argv que no son opciones (ni el valor de --libro)."""
    salida = []
    saltar = False
    for arg in argv:
        if saltar:
            saltar = False
            continue
        if arg == "--libro":
            saltar = True
            continue
        if arg.startswith("--"):
            continue
        salida.append(arg)
    return salida
