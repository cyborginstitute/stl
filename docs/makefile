MAKEFLAGS += -j -r --no-print-directory
# Makefile for Sphinx documentation
#
include makefile.docs

# You can set these variables from the command line.
SPHINXOPTS    = -c ./
SPHINXBUILD   = sphinx-build
PAPER	      =
BUILDDIR      = build

#
# Publication system
#

publish: $(BUILDDIR)/publish
	@echo [build]: html build complete. starting epub/pdf build
	@$(MAKE) -j2 $(BUILDDIR)/publish/stl.pdf $(BUILDDIR)/publish/stl.epub
	@echo [build]: epub/pdf build complete

$(BUILDDIR)/dirhtml:dirhtml links
$(BUILDDIR)/latex/stl.tex:latex
$(BUILDDIR)/epub/PersonalStatusLoggerstl.epub:epub
$(BUILDDIR)/latex/stl.pdf:$(BUILDDIR)/latex/stl.tex
$(BUILDDIR)/publish/stl.epub:$(BUILDDIR)/epub/PersonalStatusLoggerstl.epub
	@cp $< $@
	@echo [build]: migrating $@
$(BUILDDIR)/publish:$(BUILDDIR)/dirhtml
	@mkdir -p $@
	@cp -R $</* $@
	@echo [build]: migrating $@
$(BUILDDIR)/publish/stl.pdf:$(BUILDDIR)/latex/stl.pdf
	@cp $< $@
	@echo [build]: migrating $@

$(BUILDDIR)/dirhtml/usage:dirhtml
$(BUILDIR)/dirhtml/use/index.html:dirhtml
$(BUILDDIR)/dirhtml/man/index.html:$(BUILDDIR)/dirhtml/use/index.html
	@ln -s -f ../use/index.html index.html
	@mv index.html $@
	@echo [symlink]: created a link at: $@
link-targets += $(BUILDDIR)/dirhtml/man/index.html
$(BUILDDIR)/dirhtml/usage:$(BUILDDIR)/dirhtml/use
	@ln -s -f use usage
	@mv usage $@
	@echo [symlink]: created a link at: $@
link-targets += $(BUILDDIR)/dirhtml/usage
$(BUILDDIR)/dirhtml/code:$(BUILDDIR)/dirhtml/internals
	@ln -s -f internals code
	@mv code $@
	@echo [symlink]: created a link at: $@
link-targets += $(BUILDDIR)/dirhtml/usage

links:$(link-targets)

clean:
	rm -rf $(BUILDDIR)/*
