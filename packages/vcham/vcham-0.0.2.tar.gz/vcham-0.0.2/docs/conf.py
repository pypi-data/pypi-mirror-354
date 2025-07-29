# Configuration file for the Sphinx documentation builder.
# For the full list of options, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pathlib
import sys
import sphinx_rtd_theme

# -- Path setup --------------------------------------------------------------

# Path to the root of the project (one level up from the docs directory)
# Using pathlib for better path manipulations
project_root = pathlib.Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root / 'pyvcham'))

# -- Project information -----------------------------------------------------

project = 'pyVCHAM'
author = 'Emilio Rodríguez Cuenca'
# It is recommended to import your package and get the version dynamically
# Example:
# import pyvcham
# release = pyvcham.__version__
release = '0.1'

# -- General configuration ---------------------------------------------------

# Sphinx extension module names
extensions = [
    'sphinx.ext.autodoc',        # Automatically document modules
    'sphinx.ext.napoleon',       # Support for NumPy and Google style docstrings
    'sphinx.ext.viewcode',        # Add links to highlighted source code
    'sphinx.ext.intersphinx',     # Link to other project's documentation
    'sphinx_rtd_theme',           # Read the Docs theme
    # 'sphinx.ext.todo',          # Uncomment to enable todo notes
    # 'sphinx.ext.coverage',      # Uncomment to enable coverage reports
    # 'sphinx.ext.mathjax',       # Uncomment to enable MathJax for LaTeX support
]

# Napoleon settings for Google style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Intersphinx mapping to link to Python's documentation and others
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
}

# Paths that contain templates, relative to this directory
templates_path = ['_templates']

# Patterns to exclude from the documentation build
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    # Add any other patterns you want to exclude
]

# -- Options for HTML output -------------------------------------------------

# Theme to use for HTML and HTML Help pages
html_theme = 'sphinx_rtd_theme'

# Theme path for sphinx_rtd_theme
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options to customize appearance
html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    'display_version': True,
    'style_external_links': False,
    'logo_only': False,
    # 'canonical_url': 'https://yourproject.org/',  # Uncomment and set your canonical URL
}

# Paths that contain custom static files, relative to this directory
html_static_path = ['_static']

# Custom CSS files to override default styles
html_css_files = [
    'custom.css',  # Ensure this file exists in the _static directory
]

# Logo and favicon (optional)
# html_logo = 'path/to/logo.png'  # Place your logo in the _static directory
# html_favicon = 'path/to/favicon.ico'  # Place your favicon in the _static directory

# Additional HTML options
html_show_sourcelink = True  # Show link to source files
html_show_sphinx = True       # Show "Created with Sphinx" footer
html_show_copyright = True

# -- Autodoc Configuration ---------------------------------------------------

# Automatically add members from modules
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'private-members': False,
    'special-members': False,
    'inherited-members': True,
    'show-inheritance': True,
    'autosummary': True,  # Generate summary tables
}

# Autodoc type hints configuration
autodoc_typehints = 'description'  # Options: 'signature', 'description', 'none'

# -- Miscellaneous ------------------------------------------------------------

# Source file suffix
source_suffix = ['.rst', '.md']  # Support reStructuredText and Markdown

# The master toctree document
master_doc = 'index'

# Enable extension for Markdown files if needed
# extensions.append('recommonmark')
# from recommonmark.transform import AutoStructify
#
# def setup(app):
#     app.add_config_value('recommonmark_config', {
#         'auto_toc_tree_section': 'Contents',
#     }, True)
#     app.add_transform(AutoStructify)

