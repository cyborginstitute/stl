# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -c ./
SPHINXBUILD   = sphinx-build
PAPER	      =
BUILDDIR      = build

#
# Publication system
#

publish: $(BUILDDIR)/publish
	$(MAKE) -j2 $(BUILDDIR)/publish/stl.pdf $(BUILDDIR)/publish/stl.epub

$(BUILDDIR)/dirhtml:dirhtml
$(BUILDDIR)/latex/stl.tex:latex
$(BUILDDIR)/epub/PersonalStatusLoggerstl.epub:epub
$(BUILDDIR)/latex/stl.pdf:$(BUILDDIR)/latex/stl.tex
$(BUILDDIR)/publish/stl.epub:$(BUILDDIR)/epub/PersonalStatusLoggerstl.epub
	cp $< $@
$(BUILDDIR)/publish:$(BUILDDIR)/dirhtml
	mkdir -p $@
	cp -R $</* $@
	touch $@
$(BUILDDIR)/publish/stl.pdf:$(BUILDDIR)/latex/stl.pdf
	cp $< $@

include makefile.docs
