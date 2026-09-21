LATEX = latexmk -pdf -interaction=nonstopmode -file-line-error
MAIN  = main

.PHONY: all generate build check clean watch

all: generate build check

generate:
	python3 tools/gen_days.py

build:
	$(LATEX) $(MAIN).tex

check:
	python3 tools/checklog.py $(MAIN).log
	python3 tools/check_pages.py $(MAIN).aux
	python3 tools/gen_days.py --check

clean:
	latexmk -C $(MAIN).tex
	rm -f content/generated-days.tex

watch:
	$(LATEX) -pvc $(MAIN).tex
