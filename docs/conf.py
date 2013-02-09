# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set to its containing dir.

import sys, os

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.todo', 'sphinx.ext.intersphinx']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['.templates']

# The suffix of source filenames.
source_suffix = '.txt'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Personal Status Logger (stl)'
copyright = u'2011, Sam Kleinman'

version = '0.2'
release = ''

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------

git_name = 'stl'
html_theme_options = { 'project': git_name }

html_theme = 'cyborg'
html_theme_path = ['themes']

html_use_smartypants = True
html_theme_options = { 
    'project': git_name, 
    'ga_code': 'UA-2505694-4'
}

html_sidebars = {
    '**': ['localtoc.html', 'relations.html', 'sourcelink.html'],
}

#html_title = None
#html_short_title = None
#html_logo = None
#html_favicon = None

html_use_index = True
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True


html_static_path = ['source/.static']
html_use_smartypants = True
htmlhelp_basename = 'cyborg-institute'

# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'stl.tex', u'Personal Status Logger',
   u'Sam Kleinman', 'howto'),
]

# The name of an image file (relative to this directory) to place at the top of the title page.
#latex_logo = None

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'Personal Status Logger', u'Personal Status Logger',
     [u'Sam Kleinman'], 1)
]

# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = u'The Cyborg Institute'
epub_author = u'Sam Kleinman'
epub_publisher = u'Sam Kleinman'
epub_copyright = u'2011, Sam Kleinman'

# The depth of the table of contents in toc.ncx.
#epub_tocdepth = 3
# Allow duplicate toc entries.
#epub_tocdup = True

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'python': ('http://docs.python.org/', None) }
