LATEX  = latexmk -lualatex -interaction=nonstopmode -file-line-error
MAIN   = main
BW     = main-bw
PAL    = palabras
PALBW  = palabras-bw

.PHONY: all all-formats palabras generate build build-bw build-palabras build-palabras-bw \
        check check-bw check-palabras check-palabras-bw clean watch

# Dos cuadernos, dos niveles, el mismo motor:
#   - main.tex / main-bw.tex         -- el cuaderno de frases (content/q*.json);
#   - palabras.tex / palabras-bw.tex -- el de primeras palabras, el nivel
#     anterior (content/palabras/q*.json, tools/gen_palabras.py).
# El color y el blanco-y-negro de cada uno comparten body y contenido
# generado -- lo único que cambia es \bookcolor, fijado antes de
# \input{preamble} (ver preamble.tex).
# `all` sigue siendo solo el cuaderno de frases en color, por
# compatibilidad; `palabras` es lo mismo para el de primeras palabras, y
# `all-formats` compila y comprueba los cuatro PDF.
all: generate build check

palabras: generate build-palabras check-palabras

all-formats: generate build check build-bw check-bw \
             build-palabras check-palabras build-palabras-bw check-palabras-bw

generate:
	python3 tools/gen_days.py
	python3 tools/gen_palabras.py

build:
	$(LATEX) $(MAIN).tex

build-bw:
	$(LATEX) $(BW).tex

build-palabras:
	$(LATEX) $(PAL).tex

build-palabras-bw:
	$(LATEX) $(PALBW).tex

check:
	python3 tools/checklog.py $(MAIN).log
	python3 tools/check_pages.py $(MAIN).aux
	python3 tools/gen_days.py --check
	python3 tools/metricas.py

check-bw:
	python3 tools/checklog.py $(BW).log
	python3 tools/check_pages.py $(BW).aux

check-palabras:
	python3 tools/checklog.py $(PAL).log
	python3 tools/check_pages.py $(PAL).aux
	python3 tools/silabas.py --prueba
	python3 tools/gen_palabras.py --check

check-palabras-bw:
	python3 tools/checklog.py $(PALBW).log
	python3 tools/check_pages.py $(PALBW).aux

clean:
	latexmk -C $(MAIN).tex
	latexmk -C $(BW).tex
	latexmk -C $(PAL).tex
	latexmk -C $(PALBW).tex
	rm -f content/generated-days.tex content/generated-clave.tex
	rm -f content/palabras/generated-days.tex content/palabras/generated-clave.tex

watch:
	$(LATEX) -pvc $(MAIN).tex
