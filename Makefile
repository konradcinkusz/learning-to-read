LATEX  = latexmk -lualatex -interaction=nonstopmode -file-line-error
MAIN   = main
BW     = main-bw
PAL    = palabras
PALBW  = palabras-bw
LUPA   = lupa
LUPABW = lupa-bw
EN     = english
ENBW   = english-bw

.PHONY: all all-formats palabras lupa english generate \
        build build-bw build-palabras build-palabras-bw build-lupa build-lupa-bw \
        build-english build-english-bw \
        check check-bw check-palabras check-palabras-bw check-lupa check-lupa-bw \
        check-english check-english-bw \
        clean watch

# Cuatro cuadernos -- tres niveles en español y uno en inglés --, el
# mismo motor:
#   - palabras.tex / palabras-bw.tex -- nivel 1, primeras palabras
#     (content/palabras/q*.json, tools/gen_palabras.py);
#   - main.tex / main-bw.tex         -- nivel 2, el cuaderno de frases
#     (content/q*.json, tools/gen_days.py);
#   - lupa.tex / lupa-bw.tex         -- nivel 3, "Leo con lupa"
#     (content/lupa/q*.json, tools/gen_days.py --libro lupa);
#   - english.tex / english-bw.tex   -- "Read and Draw", en inglés, un
#     nivel por debajo de "Leo con lupa"
#     (content/english/q*.json, tools/gen_days.py --libro english).
# El color y el blanco-y-negro de cada uno comparten body y contenido
# generado -- lo único que cambia es \bookcolor, fijado antes de
# \input{preamble} (ver preamble.tex).
# `all` sigue siendo solo el cuaderno de frases en color, por
# compatibilidad; `palabras`, `lupa` y `english` son lo mismo para los
# otros tres, y `all-formats` compila y comprueba los ocho PDF -- es lo
# que corre el CI.
all: generate build check

palabras: generate build-palabras check-palabras

lupa: generate build-lupa check-lupa

english: generate build-english check-english

all-formats: generate build check build-bw check-bw \
             build-palabras check-palabras build-palabras-bw check-palabras-bw \
             build-lupa check-lupa build-lupa-bw check-lupa-bw \
             build-english check-english build-english-bw check-english-bw

generate:
	python3 tools/gen_days.py
	python3 tools/gen_palabras.py
	python3 tools/gen_days.py --libro lupa
	python3 tools/gen_days.py --libro english

build:
	$(LATEX) $(MAIN).tex

build-bw:
	$(LATEX) $(BW).tex

build-palabras:
	$(LATEX) $(PAL).tex

build-palabras-bw:
	$(LATEX) $(PALBW).tex

build-lupa:
	$(LATEX) $(LUPA).tex

build-lupa-bw:
	$(LATEX) $(LUPABW).tex

build-english:
	$(LATEX) $(EN).tex

build-english-bw:
	$(LATEX) $(ENBW).tex

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

check-lupa:
	python3 tools/checklog.py $(LUPA).log
	python3 tools/check_pages.py $(LUPA).aux
	python3 tools/gen_days.py --libro lupa --check
	python3 tools/metricas.py --libro lupa

check-lupa-bw:
	python3 tools/checklog.py $(LUPABW).log
	python3 tools/check_pages.py $(LUPABW).aux

check-english:
	python3 tools/checklog.py $(EN).log
	python3 tools/check_pages.py $(EN).aux
	python3 tools/gen_days.py --libro english --check
	python3 tools/metricas.py --libro english

check-english-bw:
	python3 tools/checklog.py $(ENBW).log
	python3 tools/check_pages.py $(ENBW).aux

clean:
	latexmk -C $(MAIN).tex
	latexmk -C $(BW).tex
	latexmk -C $(PAL).tex
	latexmk -C $(PALBW).tex
	latexmk -C $(LUPA).tex
	latexmk -C $(LUPABW).tex
	latexmk -C $(EN).tex
	latexmk -C $(ENBW).tex
	rm -f content/generated-days.tex content/generated-clave.tex
	rm -f content/palabras/generated-days.tex content/palabras/generated-clave.tex
	rm -f content/lupa/generated-days.tex content/lupa/generated-clave.tex
	rm -f content/english/generated-days.tex content/english/generated-clave.tex

watch:
	$(LATEX) -pvc $(MAIN).tex
