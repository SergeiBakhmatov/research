# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GraphQL_fastAPI'
copyright = '2023, Sergei Bakhmatov'
author = 'Sergei Bakhmatov'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration



import sphinx_rtd_theme
import os
import sys
sys.path.insert(0, os.path.abspath('/Users/sergeibakhmatov/research-1/'))
   
     

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc"
    ]
pygments_style = "sphinx"
version = '0.1.0'
templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#sphinx_rtd_theme classic sphinx-build -b html . _build_cloud
html_theme = 'cloud'
html_static_path = ['_static']
