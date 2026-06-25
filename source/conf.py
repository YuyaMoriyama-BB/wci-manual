# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'WCI設定事例集'
copyright = '2025, Bit-Brain Corporation.'
author = 'BitBrain'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_design",
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

#html_theme_options = {
#    "style_nav_header_background": "#FFFFFF",
#}

html_show_sourcelink = False

html_static_path = ['_static']

def setup(app):
    app.add_css_file('custom.css')  # Sphinx >= 1.8


# html_logo = '_static/logo.bmp'


html_favicon = "_static/fav.ico"

html_baseurl = "https://YuyaMoriyama-BB.github.io/wci-manual/"