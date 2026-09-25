"""Los cuadernos que genera tools/gen_days.py -- uno por nivel.

El repositorio tiene tres cuadernos en español, uno por nivel, y otros
en inglés y en polaco, con los mismos personajes. Los que genera este
script:

  - nivel 1, "Primeras palabras" (palabras.tex): tiene su propio
    generador, tools/gen_palabras.py, y no pasa por aquí.
  - nivel 2, "Frases" (main.tex, content/q*.json): el cuaderno original.
    Frases completas, de 1 a 4 por página (una más por trimestre).
  - nivel 3, "Leo con lupa" (lupa.tex, content/lupa/q*.json): el año
    siguiente. Oraciones compuestas y subordinadas, en párrafos, y una
    actividad de análisis cada día (dibujar con detalle lo que describe
    el texto, resolver un caso con pistas, una tabla lógica, un mapa, un
    mensaje en clave...). Ver notes/04-nivel-lupa.md.
  - "Read and Draw" (english.tex, content/english/q*.json): todo en
    inglés, un nivel por debajo de "Leo con lupa" -- textos más cortos,
    pero hechos también de oraciones compuestas (because, when, who,
    that...), y cada día un análisis muy sencillo de lo leído: casi
    siempre dibujar exactamente lo que dice el texto. Ver
    notes/05-english.md.
  - «Zdania» (zdania.tex, content/zdania/q*.json): el cuaderno de
    frases en polaco -- los mismos 260 días, frase a frase, con los
    mismos temas, y con su propia escalera, medida en palabras
    polacas. Ver notes/09-zdania.md.

Los cuatro últimos comparten generador (tools/gen_days.py), escalera
(tools/metricas.py) y página; todo lo que distingue a uno de otro vive
aquí, en un solo sitio: dónde está su contenido, qué ficheros genera,
qué escalera sigue, en qué idioma está, cuántas frases lleva una página
(o si su texto va en párrafos, y qué módulo genera entonces sus
actividades), qué tipos de actividad admite, qué instrucción de lectura
y qué tamaño de letra lleva cada trimestre. gen_days.py, metricas.py y
check_pages.py reciben `--libro frases`, `--libro lupa`, `--libro
english` o `--libro zdania`; sin la opción, `frases` -- así `python3
tools/gen_days.py` a secas sigue haciendo exactamente lo mismo que
antes de que existiera "Leo con lupa".
"""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

# Los cuadernos comparten calendario: 260 días laborables, cuatro
# trimestres de 13 semanas que son las cuatro estaciones del año (ver
# notes/02-revision-y-plan.md, punto 1).
RANGO_TRIMESTRE = {1: (1, 65), 2: (66, 130), 3: (131, 195), 4: (196, 260)}

# Las letras del abecedario de cada idioma, las que se trazan ("traza"):
# las 27 del español, las 26 del inglés y las 32 del polaco (sin q, v ni
# x, que en polaco solo salen en palabras de fuera). Las usan los dos
# generadores, tools/gen_days.py y tools/gen_palabras.py.
ALFABETO_ES = "abcdefghijklmnñopqrstuvwxyz"
ALFABETO_EN = "abcdefghijklmnopqrstuvwxyz"
ALFABETO_PL = "aąbcćdeęfghijklłmnńoóprsśtuwyzźż"

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
    # Idioma del cuaderno: qué fichero de cadenas carga (lang/<idioma>.tex,
    # elegido por \booklang antes de \input{preamble}, ver preamble.tex),
    # contra cuál comprueba tools/gen_days.py \totaldias, y cómo mide
    # tools/metricas.py sus textos (palabras funcionales, nexos, dónde
    # acaba una frase).
    idioma: str = "es"
    # Un libro con el texto en párrafos (ver `parrafos`): qué módulo de
    # tools/ valida su texto y genera su página y su clave -- "lupa"
    # (tools/lupa.py) o "english" (tools/english.py). El cuaderno de
    # frases no tiene: lo genera tools/gen_days.py solo.
    motor: str = None
    # Mientras un cuaderno se escribe por partes (un PR por trimestre, cada
    # uno en verde antes de fusionarse), cuántos días tiene ya escritos:
    # tools/gen_days.py exige exactamente esos, del día 1 en adelante y sin
    # huecos, en vez del libro entero. None = el libro está terminado y
    # tiene que tener sus total_dias -- la regla de siempre. Se quita en
    # cuanto se escribe el último trimestre.
    dias_escritos: int = None
    # La página de medalla de fin de trimestre (PLANTILLA_MEDALLA en
    # tools/gen_days.py), en el idioma del cuaderno: el título ({} = la
    # estación, de nombre_medalla) y la frase de ánimo, con su línea para
    # escribir el nombre.
    titulo_medalla: str = "¡Medalla de {}!"
    animo_medalla: str = r"¡Sigue así, \rule{55mm}{0.4pt}!"
    # "Relaciona" (PLANTILLA_RELACIONA en tools/gen_days.py): la
    # instrucción que va encima de las parejas, en el idioma del cuaderno.
    instruccion_relaciona: str = "Une cada nombre con quién es, con una línea."
    # "Traza": la palabra de ejemplo de cada letra ("M de Mamá", "M jak
    # mama"), editada a mano, y el abecedario del cuaderno. Con
    # abecedario, tools/gen_days.py comprueba además que cada letra que
    # se traza es suya y que, con el libro entero, se trazan todas; sin
    # él (None), solo que la letra tiene contorno y palabra, como siempre.
    palabras_trazo: Path = CONTENT_DIR / "palabras-trazo.json"
    alfabeto: str = None

    def __post_init__(self):
        if self.rango_trimestre is None:
            object.__setattr__(self, "rango_trimestre", dict(RANGO_TRIMESTRE))
        if self.nombre_medalla is None:
            object.__setattr__(self, "nombre_medalla", dict(NOMBRE_MEDALLA_TRIMESTRE))

    @property
    def parrafos(self):
        """True si el texto del día va en párrafos y la página y las
        actividades las genera el módulo de `motor` ("Leo con lupa" y
        "Read and Draw"), no tools/gen_days.py."""
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
        # compañeros de clase y gente del colegio (invierno y primavera)
        "nora", "leo", "irene", "álex", "pilar", "luis", "elena", "jorge",
        "nacho",
        # la granja escuela
        "julián", "lola",
    }),
    motor="lupa",
)

ENGLISH = Libro(
    nombre="english",
    # Un nivel por debajo de "Leo con lupa" (ver notes/05-english.md): en
    # inglés, la lectora está donde en español estaba con el cuaderno de
    # frases.
    nivel=2,
    dir_contenido=CONTENT_DIR / "english",
    salida_dias=CONTENT_DIR / "english" / "generated-days.tex",
    salida_clave=CONTENT_DIR / "english" / "generated-clave.tex",
    progresion=CONTENT_DIR / "english" / "progresion.json",
    instruccion_lectura={
        1: r"\lblIngInstruccionUno",
        2: r"\lblIngInstruccionDos",
        3: r"\lblIngInstruccionTres",
        4: r"\lblIngInstruccionCuatro",
    },
    # \fuenteIngles (preamble-english.tex): más grande que la de "Leo con
    # lupa" -- textos más cortos, y en un idioma que todavía se está
    # aprendiendo.
    fuente_trimestre={1: 1, 2: 2, 3: 3, 4: 4},
    tipos_validos=frozenset({
        # ver tools/english.py: casi todas acaban dibujando, marcando o
        # uniendo, casi nunca escribiendo más de una palabra
        "dibuja", "colorea", "donde", "si_no", "rodea", "relaciona",
        "mitades", "ordena", "huecos", "busca", "adivina", "vinetas",
        "repasa", "crea",
    }),
    idioma="en",
    motor="english",
    nombre_medalla={1: "Autumn", 2: "Winter", 3: "Spring"},
    titulo_medalla="{} medal!",
    animo_medalla=r"Well done, \rule{55mm}{0.4pt}!",
    nombres_propios=frozenset({
        "lucía", "dani", "toby", "rosa", "marta", "sofía", "pedro", "luna",
        "mum", "dad", "grandma",
        # los vecinos nuevos, de Londres
        "amy", "sam", "pip", "brown", "browns", "mr", "mrs", "london",
        # el bibliotecario del barrio y el conserje del colegio (los mismos
        # de «Leo con lupa»)
        "tomás", "paco",
        # la granja escuela de la primavera: el granjero y su cabra (los
        # mismos de «Leo con lupa»)
        "julián", "lola",
        # el pueblo, en verano
        "andrés", "bigotes", "martín",
    }),
)

ZDANIA = Libro(
    nombre="zdania",
    # El cuaderno de frases, en polaco (ver notes/09-zdania.md): los mismos
    # días, frase a frase, las mismas actividades y las mismas reglas --
    # de una frase al día en otoño a cuatro en verano, y sin "responde" en
    # otoño --; lo que cambia es el idioma, la escalera (las frases
    # polacas tienen menos palabras: no hay artículos, y el sujeto a
    # menudo no se dice) y las letras de "Pisz po śladzie", que en polaco
    # son 32.
    nivel=2,
    dir_contenido=CONTENT_DIR / "zdania",
    salida_dias=CONTENT_DIR / "zdania" / "generated-days.tex",
    salida_clave=CONTENT_DIR / "zdania" / "generated-clave.tex",
    progresion=CONTENT_DIR / "zdania" / "progresion.json",
    # Las mismas macros que el cuaderno de frases: lang/pl.tex las tiene
    # en polaco.
    instruccion_lectura=FRASES.instruccion_lectura,
    fuente_trimestre=FRASES.fuente_trimestre,
    tipos_validos=FRASES.tipos_validos,
    frases_por_trimestre=FRASES.frases_por_trimestre,
    trimestres_sin_responde=FRASES.trimestres_sin_responde,
    # En polaco, los nombres se declinan: cada forma que sale en el
    # cuaderno cuenta como el nombre, no como una palabra nueva (ver
    # lematizar_pl en tools/metricas.py). Lucía y Sofía conservan la í
    # en todas sus formas; Toby, el apóstrofo (Toby'ego, Toby'emu).
    nombres_propios=frozenset({
        "lucía", "lucíi", "lucíę", "lucíą", "lucío",
        "dani", "daniego", "daniemu", "danim",
        "toby",
        "rosa", "rosy", "rosie", "rosę", "rosą", "roso",
        "marta", "marty", "marcie", "martę", "martą", "marto",
        "sofía", "sofíi", "sofíę", "sofíą", "sofío",
        "pedro", "pedra", "pedrowi", "pedrem", "pedrze",
        "luna", "luny", "lunie", "lunę", "luną",
        "mama", "mamy", "mamie", "mamę", "mamą", "mamo",
        "tata", "taty", "tacie", "tatę", "tatą", "tato",
        "babcia", "babci", "babcię", "babcią", "babciu",
    }),
    idioma="pl",
    dias_escritos=65,
    nombre_medalla={1: "jesień", 2: "zimę", 3: "wiosnę"},
    titulo_medalla="Medal za {}!",
    animo_medalla=r"Tak trzymaj, \rule{55mm}{0.4pt}!",
    instruccion_relaciona=r"\lblInstruccionRelaciona",
    palabras_trazo=CONTENT_DIR / "zdania" / "palabras-trazo.json",
    alfabeto=ALFABETO_PL,
)

LIBROS = {libro.nombre: libro for libro in (FRASES, LUPA, ENGLISH, ZDANIA)}


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
