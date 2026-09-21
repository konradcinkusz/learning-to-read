LATEX = latexmk -pdf -interaction=nonstopmode -file-line-error
MAIN  = main
BW    = main-bw

.PHONY: all all-formats generate build build-bw check check-bw clean watch

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

check-bw:
	python3 tools/checklog.py $(BW).log
	python3 tools/check_pages.py $(BW).aux

clean:
	latexmk -C $(MAIN).tex
	latexmk -C $(BW).tex
	rm -f content/generated-days.tex

watch:
	$(LATEX) -pvc $(MAIN).tex
