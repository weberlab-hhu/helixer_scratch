pdflatex --shell-escape $1.tex
bibtex $1
pdflatex --shell-escape $1.tex
pdflatex --shell-escape $1.tex
