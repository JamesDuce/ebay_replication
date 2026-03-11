.PHONY: all clean

all: paper/paper.pdf

# Preprocessing: data wrangling and figures
output/figures/figure_5_2.png output/figures/figure_5_3.png: input/PaidSearch.csv code/preprocess.py
	python code/preprocess.py

# DID estimation
output/tables/did_table.tex: input/PaidSearch.csv code/did_analysis.py
	python code/did_analysis.py

# Paper compilation
paper/paper.pdf: paper/paper.tex output/figures/figure_5_2.png output/figures/figure_5_3.png output/tables/did_table.tex
	cd paper && pdflatex paper.tex && pdflatex paper.tex

clean:
	rm -f output/figures/*.png output/tables/*.tex paper/paper.pdf paper/paper.aux paper/paper.log


# Task 2 answers:
# 1) If code/preprocess.py changes: rebuild figures and then paper.pdf; skip did_table.tex.
# 2) If code/did_analysis.py changes: rebuild did_table.tex and then paper.pdf; skip figures.
# 3) If paper/paper.tex changes: rebuild only paper.pdf; skip both python scripts.
