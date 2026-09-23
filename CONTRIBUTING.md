# Contribuir a este repositorio

Antes de nada, una aclaración honesta: esto es el cuaderno de lectura de
una niña real, de 6 años. Los personajes (Lucía, Dani, Toby, Mamá, Papá,
Abuela Rosa), las frases y la trama semanal son una decisión editorial de
su autor, no un contenido abierto a propuestas -- así que **no es un
proyecto que busque contribuciones de historia** (nuevas frases, nuevos
personajes, cambios de trama). Ver `notes/01-curriculum.md` para el
razonamiento completo detrás del programa del curso.

Lo que sí tiene sentido, y es bienvenido:

## Lo que encaja aquí

- **Errores del motor**: algo que no compila, un caracter que se renderiza
  mal (el propio repositorio tuvo uno real -- babel-spanish convierte `"`
  en un carácter activo, y una comilla suelta en un diálogo se corrompía
  en silencio; el arreglo está documentado en `preamble.tex` junto al
  código, como ejemplo del tipo de problema que merece un *issue* o un PR).
- **Los generadores** (`tools/gen_days.py`, `tools/gen_palabras.py`,
  `tools/lupa.py`, `tools/english.py`) y sus validaciones -- por ejemplo, si detectas un
  caso que debería fallar la validación y no lo hace, o al revés (una
  tabla lógica con dos soluciones que el generador no detecta, una ruta
  de mapa que llega a otra casilla...).
- **El silabeo** (`tools/silabas.py`) -- una palabra real que las reglas
  parten mal es exactamente el tipo de error que merece un *issue* (con
  la palabra y el silabeo correcto; si es un caso legítimo que las
  reglas no cubren, se añade a `EXCEPCIONES` y a `CASOS_PRUEBA`).
- **`tools/check_pages.py`** y el invariante "1 día = 1 página" -- si
  encuentras un caso donde se rompe sin que el *build* lo detecte.
- **CI** (`.github/workflows/`), el `Makefile`, o cualquier parte de la
  infraestructura de construcción.

## Lo que no

- Frases nuevas, personajes nuevos, cambios de trama -- eso es una
  decisión editorial del autor sobre la historia de su propia hija.

## La vía principal: haz un fork

El repositorio está deliberadamente construido para esto: el motor LaTeX
(`preamble*.tex`, `lang/es.tex`, `lang/en.tex`, `tools/`) es independiente
del contenido (`content/*.json`, `content/palabras/*.json`,
`content/lupa/*.json`, `content/english/*.json`). Si
quieres un cuaderno parecido para otro niño o niña, haz un fork,
sustituye `content/q1.json` a `q4.json` (frases), `content/palabras/q1.json`
a `q4.json` (primeras palabras), `content/lupa/q1.json` a `q4.json`
(Leo con lupa) y/o `content/english/q1.json` a `q4.json` (Read and
Draw, en inglés) por tus propios personajes, frases y palabras, y
conserva el resto tal cual -- es exactamente el reparto MIT/CC BY-NC-SA de `LICENSE`: el motor
es tuyo para reutilizar, la historia concreta de esta familia no.

## Flujo de trabajo

```sh
make generate       # content/q*.json, content/{palabras,lupa,english}/q*.json -> .tex generados
make build           # compila el cuaderno de frases en color (main.tex)
make palabras        # genera, compila y comprueba el de primeras palabras (palabras.tex)
make lupa            # genera, compila y comprueba Leo con lupa (lupa.tex)
make english         # genera, compila y comprueba Read and Draw (english.tex)
make check            # tools/checklog.py + tools/check_pages.py + tools/gen_days.py --check + tools/metricas.py
make all-formats      # los cuatro cuadernos, color Y blanco-y-negro -- ejecútalo
                       # antes de abrir un PR, es lo mismo que corre el CI
```

Las barreras duras que tienen que quedar en verde:

- **1 día = exactamente 1 página** (`tools/check_pages.py`, lee el `.aux`
  después de compilar -- es la única forma de saber si un día se ha
  desbordado a una segunda página sin mirar las 260 páginas una a una).
- **El log sin errores ni `Overfull`** (`tools/checklog.py` -- nunca
  `grep '^!'`: con `-file-line-error` la línea de error empieza por una
  ruta, no por `!`, y `-interaction=nonstopmode` escribe igualmente un PDF
  encima del error, así que el código de salida y el propio PDF dicen
  "todo bien" aunque no lo esté).
- **El JSON y el `.tex` generado coinciden** (`tools/gen_days.py --check`
  -- si alguien toca `content/generated-days.tex` a mano y luego cambia el
  JSON, el desajuste se detecta).
- **La escalera de sílabas** del cuaderno de primeras palabras
  (`tools/gen_palabras.py --check`): cada palabra escrita a mano con sus
  sílabas (`"pe-lo-ta"`) tiene que coincidir con el silabeo automático
  de `tools/silabas.py`, y no puede usar estructuras de sílaba que su
  semana todavía no admite (una `rr` en otoño, por ejemplo).
- **La escalera de progresión** (`tools/metricas.py`, contra
  `content/progresion.json` -- ver `notes/02-revision-y-plan.md`, Parte
  C): palabras por página y frase más larga no pueden superar el
  objetivo de esa semana. El vocabulario nuevo por día solo avisa, no
  bloquea. En Leo con lupa (`--libro lupa`, contra
  `content/lupa/progresion.json`) y en Read and Draw (`--libro english`,
  contra `content/english/progresion.json`) hay además un mínimo de
  oraciones subordinadas por texto.
- **Las actividades de Leo con lupa** (`tools/gen_days.py --libro lupa
  --check`, ver `tools/lupa.py`): cada tabla lógica con una sola
  solución, cada ruta de mapa llegando a donde dice la clave, cada
  corrección de «Caza los errores» presente de verdad en el texto de la
  semana, y el libro entero, con sus 260 días.
- **Las actividades de Read and Draw** (`tools/gen_days.py --libro
  english --check`, ver `tools/english.py`): cada frase de «The missing
  words» y de «Match the halves» presente tal cual en el texto de la
  semana, cada palabra de «Word hunt» en el del día, cada dibujo de
  `diagrams/english/` que se pide existiendo, y el texto en inglés
  británico, sin rastros del español; y el libro entero, con sus 260
  días.

`.github/workflows/build.yml` corre exactamente estas mismas comprobaciones
en cada *push* y *pull request*, así que un PR con `make all-formats` en
verde localmente debería pasar el CI sin sorpresas.

## Cómo reportar un problema

Abre un [*issue*](https://github.com/konradcinkusz/learning-to-read/issues)
describiendo qué esperabas y qué ha pasado -- si es un problema de
compilación, adjunta la línea exacta del log (`tools/checklog.py` te la da
ya localizada, con el fichero y el número de línea).
