LATEX  = latexmk -lualatex -interaction=nonstopmode -file-line-error
MAIN   = main
BW     = main-bw
N2     = main-nivel2
N2BW   = main-nivel2-bw

.PHONY: all all-formats generate build build-bw check check-bw clean watch \
        nivel2 generate-nivel2 build-nivel2 build-nivel2-bw check-nivel2 check-nivel2-bw

# Dos libros, un solo motor (ver tools/libros.py):
#   nivel 1, "Aprendo a leer" -- main.tex / main-bw.tex, content/q*.json
#   nivel 2, "Leo con lupa"   -- main-nivel2.tex / main-nivel2-bw.tex,
#                                content/nivel2/q*.json (notes/03-nivel2.md)
# El color y el blanco-y-negro de cada libro comparten el mismo body y el
# mismo .tex generado -- lo único que cambia es \bookcolor, fijado por su
# main antes de \input{preamble} (ver preamble.tex).
# `all` sigue siendo solo el nivel 1 en color, por compatibilidad; `nivel2`
# es lo mismo para el nivel 2; `all-formats` construye y comprueba los dos
# libros en los dos formatos -- es lo que corre el CI.
all: generate build check

nivel2: generate-nivel2 build-nivel2 check-nivel2

all-formats: generate build check build-bw check-bw \
             generate-nivel2 build-nivel2 check-nivel2 build-nivel2-bw check-nivel2-bw

generate:
	python3 tools/gen_days.py

generate-nivel2:
	python3 tools/gen_days.py --libro nivel2

build:
	$(LATEX) $(MAIN).tex

build-bw:
	$(LATEX) $(BW).tex

build-nivel2:
	$(LATEX) $(N2).tex

build-nivel2-bw:
	$(LATEX) $(N2BW).tex

check:
	python3 tools/checklog.py $(MAIN).log
	python3 tools/check_pages.py $(MAIN).aux
	python3 tools/gen_days.py --check
	python3 tools/metricas.py

check-bw:
	python3 tools/checklog.py $(BW).log
	python3 tools/check_pages.py $(BW).aux

check-nivel2:
	python3 tools/checklog.py $(N2).log
	python3 tools/check_pages.py $(N2).aux
	python3 tools/gen_days.py --libro nivel2 --check
	python3 tools/metricas.py --libro nivel2

check-nivel2-bw:
	python3 tools/checklog.py $(N2BW).log
	python3 tools/check_pages.py $(N2BW).aux

clean:
	latexmk -C $(MAIN).tex
	latexmk -C $(BW).tex
	latexmk -C $(N2).tex
	latexmk -C $(N2BW).tex
	rm -f content/generated-days.tex content/generated-clave.tex
	rm -f content/nivel2/generated-days.tex content/nivel2/generated-clave.tex

watch:
	$(LATEX) -pvc $(MAIN).tex
