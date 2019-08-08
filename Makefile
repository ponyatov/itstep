DOC = README.md wiki/*.md
docs/index.html: $(DOC) Makefile
	pandoc --metadata pagetitle=" " -f gfm -t html -s --toc -o $@ $(DOC)

update:
	cd wiki ; git pull -v

wiki:
	git clone -o gh git@github.com:ponyatov/itstep.wiki.git wiki
