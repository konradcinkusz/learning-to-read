LATEX  = latexmk -pdf -interaction=nonstopmode -file-line-error
MAIN   = main
BW     = main-bw
MUESTRA = main-muestra

.PHONY: all all-formats generate build build-bw check check-bw clean watch \
        generate-muestra build-muestra check-muestra muestra

# El color y el blanco-y-negro comparten el mismo body.tex y el mismo
# content/generated-days.tex -- lo único que cambia es \bookcolor, fijado
# por main.tex / main-bw.tex antes de \input{preamble} (ver preamble.tex).
# `all` sigue siendo solo la versión en color, por compatibilidad; usar
# `all-formats` para las dos.
all: generate build check

all-formats: generate build check build-bw check-bw

generate:
	python3 tools/gen_days.py

build:
	$(LATEX) $(MAIN).tex

build-bw:
	$(LATEX) $(BW).tex

check:
	python3 tools/checklog.py $(MAIN).log
	python3 tools/check_pages.py $(MAIN).aux
	python3 tools/gen_days.py --check
	python3 tools/metricas.py

check-bw:
	python3 tools/checklog.py $(BW).log
	python3 tools/check_pages.py $(BW).aux

clean:
	latexmk -C $(MAIN).tex
	latexmk -C $(BW).tex
	latexmk -C $(MUESTRA).tex
	rm -f content/generated-days.tex content/generated-muestra.tex

watch:
	$(LATEX) -pvc $(MAIN).tex

# NO es el libro -- 60 páginas (15 días reales de cada trimestre) para
# comparar el nivel de un vistazo. Ver tools/gen_muestra.py. No entra en
# `all` / `all-formats` porque no forma parte del cuaderno que se publica.
generate-muestra:
	python3 tools/gen_muestra.py

build-muestra:
	$(LATEX) $(MUESTRA).tex

check-muestra:
	python3 tools/checklog.py $(MUESTRA).log
	python3 tools/check_pages.py --allow-gaps $(MUESTRA).aux
	python3 tools/gen_muestra.py --check

muestra: generate-muestra build-muestra check-muestra
