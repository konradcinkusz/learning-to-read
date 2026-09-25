LATEX  = latexmk -lualatex -interaction=nonstopmode -file-line-error
MAIN   = main
BW     = main-bw
PAL    = palabras
PALBW  = palabras-bw
LUPA   = lupa
LUPABW = lupa-bw
EN     = english
ENBW   = english-bw
FW     = firstwords
FWBW   = firstwords-bw
SL     = slowa
SLBW   = slowa-bw
ZD     = zdania
ZDBW   = zdania-bw
CZ     = czytam
CZBW   = czytam-bw

.PHONY: all all-formats palabras lupa english firstwords slowa zdania czytam verano muestra generate \
        build build-bw build-palabras build-palabras-bw build-lupa build-lupa-bw \
        build-english build-english-bw build-firstwords build-firstwords-bw \
        build-slowa build-slowa-bw build-zdania build-zdania-bw build-czytam build-czytam-bw \
        check check-bw check-palabras check-palabras-bw check-lupa check-lupa-bw \
        check-english check-english-bw check-firstwords check-firstwords-bw \
        check-slowa check-slowa-bw check-zdania check-zdania-bw check-czytam check-czytam-bw \
        clean watch

# Ocho cuadernos -- tres niveles en español, dos en inglés y tres en
# polaco --, el mismo motor:
#   - palabras.tex / palabras-bw.tex -- nivel 1, primeras palabras
#     (content/palabras/q*.json, tools/gen_palabras.py);
#   - main.tex / main-bw.tex         -- nivel 2, el cuaderno de frases
#     (content/q*.json, tools/gen_days.py);
#   - lupa.tex / lupa-bw.tex         -- nivel 3, "Leo con lupa"
#     (content/lupa/q*.json, tools/gen_days.py --libro lupa);
#   - english.tex / english-bw.tex   -- "Read and Draw", en inglés, un
#     nivel por debajo de "Leo con lupa"
#     (content/english/q*.json, tools/gen_days.py --libro english);
#   - firstwords.tex / firstwords-bw.tex -- «First Words», las primeras
#     palabras en inglés, muy por debajo de "Read and Draw"
#     (content/firstwords/q*.json, tools/gen_palabras.py --libro firstwords);
#   - slowa.tex / slowa-bw.tex       -- «Pierwsze słowa», las primeras
#     palabras en polaco, por sílabas, como el nivel 1 en español
#     (content/slowa/q*.json, tools/gen_palabras.py --libro slowa);
#   - zdania.tex / zdania-bw.tex     -- «Zdania», el cuaderno de frases
#     en polaco, día a día el de main.tex
#     (content/zdania/q*.json, tools/gen_days.py --libro zdania);
#   - czytam.tex / czytam-bw.tex     -- «Czytam z lupą», "Leo con lupa"
#     en polaco, día a día el de lupa.tex
#     (content/czytam/q*.json, tools/gen_days.py --libro czytam).
# El color y el blanco-y-negro de cada uno comparten body y contenido
# generado -- lo único que cambia es \bookcolor, fijado antes de
# \input{preamble} (ver preamble.tex).
# `all` sigue siendo solo el cuaderno de frases en color, por
# compatibilidad; `palabras`, `lupa`, `english`, `firstwords`, `slowa`,
# `zdania` y `czytam` son lo mismo para los otros siete, `verano` y
# `muestra` compilan y comprueban los catorce cuadernos de verano y las
# catorce muestras (ver más abajo), y `all-formats` compila y comprueba
# los cuarenta y cuatro PDF -- es lo que corre el CI.
all: generate build check

palabras: generate build-palabras check-palabras

lupa: generate build-lupa check-lupa

english: generate build-english check-english

firstwords: generate build-firstwords check-firstwords

slowa: generate build-slowa check-slowa

zdania: generate build-zdania check-zdania

czytam: generate build-czytam check-czytam

all-formats: generate build check build-bw check-bw \
             build-palabras check-palabras build-palabras-bw check-palabras-bw \
             build-lupa check-lupa build-lupa-bw check-lupa-bw \
             build-english check-english build-english-bw check-english-bw \
             build-firstwords check-firstwords build-firstwords-bw check-firstwords-bw \
             build-slowa check-slowa build-slowa-bw check-slowa-bw \
             build-zdania check-zdania build-zdania-bw check-zdania-bw \
             build-czytam check-czytam build-czytam-bw check-czytam-bw \
             verano muestra

generate:
	python3 tools/gen_days.py
	python3 tools/gen_palabras.py
	python3 tools/gen_days.py --libro lupa
	python3 tools/gen_days.py --libro english
	python3 tools/gen_palabras.py --libro firstwords
	python3 tools/gen_palabras.py --libro slowa
	python3 tools/gen_days.py --libro zdania
	python3 tools/gen_days.py --libro czytam

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

build-firstwords:
	$(LATEX) $(FW).tex

build-firstwords-bw:
	$(LATEX) $(FWBW).tex

build-slowa:
	$(LATEX) $(SL).tex

build-slowa-bw:
	$(LATEX) $(SLBW).tex

build-zdania:
	$(LATEX) $(ZD).tex

build-zdania-bw:
	$(LATEX) $(ZDBW).tex

build-czytam:
	$(LATEX) $(CZ).tex

build-czytam-bw:
	$(LATEX) $(CZBW).tex

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

check-firstwords:
	python3 tools/checklog.py $(FW).log
	python3 tools/check_pages.py $(FW).aux
	python3 tools/fonetica.py --prueba
	python3 tools/gen_palabras.py --libro firstwords --check

check-firstwords-bw:
	python3 tools/checklog.py $(FWBW).log
	python3 tools/check_pages.py $(FWBW).aux

check-slowa:
	python3 tools/checklog.py $(SL).log
	python3 tools/check_pages.py $(SL).aux
	python3 tools/sylaby.py --prueba
	python3 tools/gen_palabras.py --libro slowa --check

check-slowa-bw:
	python3 tools/checklog.py $(SLBW).log
	python3 tools/check_pages.py $(SLBW).aux

check-zdania:
	python3 tools/checklog.py $(ZD).log
	python3 tools/check_pages.py $(ZD).aux
	python3 tools/gen_days.py --libro zdania --check
	python3 tools/metricas.py --libro zdania

check-zdania-bw:
	python3 tools/checklog.py $(ZDBW).log
	python3 tools/check_pages.py $(ZDBW).aux

check-czytam:
	python3 tools/checklog.py $(CZ).log
	python3 tools/check_pages.py $(CZ).aux
	python3 tools/gen_days.py --libro czytam --check
	python3 tools/metricas.py --libro czytam

check-czytam-bw:
	python3 tools/checklog.py $(CZBW).log
	python3 tools/check_pages.py $(CZBW).aux

# Las ediciones (ver notes/07-ediciones.md), en color y en blanco y negro:
# el cuaderno de verano de cada cuaderno y su muestra gratuita (las cuatro
# primeras semanas). ediciones/<raíz>-<edición>.tex es el .tex raíz de
# siempre con \edicion fijado antes, y sus .tex generados los escribe
# `make generate` a la vez que los del libro entero. `make
# build-lupa-verano` compila uno, `make check-lupa-verano` lo compila y
# lo comprueba, y `make verano` / `make muestra`, los catorce de cada una.
RAICES        = $(MAIN) $(BW) $(PAL) $(PALBW) $(LUPA) $(LUPABW) $(EN) $(ENBW) $(FW) $(FWBW) \
                $(SL) $(SLBW) $(ZD) $(ZDBW)
BUILD_VERANO  = $(RAICES:%=build-%-verano)
CHECK_VERANO  = $(RAICES:%=check-%-verano)
BUILD_MUESTRA = $(RAICES:%=build-%-muestra)
CHECK_MUESTRA = $(RAICES:%=check-%-muestra)
.PHONY: $(BUILD_VERANO) $(CHECK_VERANO) $(BUILD_MUESTRA) $(CHECK_MUESTRA)

verano: generate $(CHECK_VERANO)

muestra: generate $(CHECK_MUESTRA)

$(BUILD_VERANO) $(BUILD_MUESTRA): build-%:
	$(LATEX) ediciones/$*.tex

$(CHECK_VERANO) $(CHECK_MUESTRA): check-%: build-%
	python3 tools/checklog.py $*.log
	python3 tools/check_pages.py $*.aux

clean:
	latexmk -C $(MAIN).tex
	latexmk -C $(BW).tex
	latexmk -C $(PAL).tex
	latexmk -C $(PALBW).tex
	latexmk -C $(LUPA).tex
	latexmk -C $(LUPABW).tex
	latexmk -C $(EN).tex
	latexmk -C $(ENBW).tex
	latexmk -C $(FW).tex
	latexmk -C $(FWBW).tex
	latexmk -C $(SL).tex
	latexmk -C $(SLBW).tex
	latexmk -C $(ZD).tex
	latexmk -C $(ZDBW).tex
	latexmk -C $(CZ).tex
	latexmk -C $(CZBW).tex
	for r in $(RAICES); do latexmk -C ediciones/$$r-verano.tex; latexmk -C ediciones/$$r-muestra.tex; done
	rm -f content/generated-*-verano.tex content/*/generated-*-verano.tex
	rm -f content/generated-*-muestra.tex content/*/generated-*-muestra.tex
	rm -f content/generated-days.tex content/generated-clave.tex
	rm -f content/palabras/generated-days.tex content/palabras/generated-clave.tex
	rm -f content/lupa/generated-days.tex content/lupa/generated-clave.tex
	rm -f content/english/generated-days.tex content/english/generated-clave.tex
	rm -f content/firstwords/generated-days.tex content/firstwords/generated-clave.tex \
	      content/firstwords/generated-sonidos.tex
	rm -f content/slowa/generated-days.tex content/slowa/generated-clave.tex
	rm -f content/zdania/generated-days.tex content/zdania/generated-clave.tex
	rm -f content/czytam/generated-days.tex content/czytam/generated-clave.tex

watch:
	$(LATEX) -pvc $(MAIN).tex
