# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sys,os
sys.path.insert(0, os.path.abspath('exts'))
sys.path.append('/Users/todd/GitHub/mwarp1d/')
import mwarp1d


# -- Project information -----------------------------------------------------

project = 'mwarp1d'
copyright = '2019, Todd Pataky'
author = 'Todd Pataky'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'video',
	'sphinx.ext.autosectionlabel',
	'sphinx.ext.autodoc',
	'matplotlib.sphinxext.plot_directive',
	'nbsphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['**/.ipynb_checkpoints']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'bootstrap-astropy'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    'logotext1': 'mwarp',  # white,  semi-bold
    'logotext2': '1d',  # orange, light
    'logotext3': '',   # white,  light
    'astropy_project_menubar': False
    }
