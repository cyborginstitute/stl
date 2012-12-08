MAKEFLAGS += --include-dir docs/ --no-print-directory
PYTHONBIN := $(shell which python)
bin-output = build/bin

.PHONY: install build sdist docs simple

install:
	$(PYTHONBIN) setup.py install
build:
	$(PYTHONBIN) setup.py build
sdist:
	$(PYTHONBIN) setup.py sdist
docs: 
	@$(MAKE) -C docs/ publish

simple:
	mkdir -p $(bin-output)/
	cp stl/{stl,wc_track,sauron,lnote}.py $(bin-output)/
	ln -s stl.py stl-link
	mv stl-link $(bin-output)/stl
	ln -s wc_track.py wc-track
	mv wc-track $(bin-output)/
	ln -s sauron.py sauron
	mv sauron $(bin-output)/
	ln -s lnote.py lnote
	mv lnote $(bin-output)/
