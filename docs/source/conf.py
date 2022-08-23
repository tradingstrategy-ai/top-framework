# Configuration file for the Sphinx documentation builder.

project = 'Top Framework'
copyright = '2022 Market Software Ltd'
author = 'Mikko Ohtamaa'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx_sitemap",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
#    "sphinx_toolbox.more_autodoc",
#    "sphinx_autodoc_typehints"
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "rich": ("https://rich.readthedocs.io/en/stable/", None),
    "redis-py": ("https://redis-py.readthedocs.io/en/stable/", None)
}

# https://help.farbox.com/pygments.html
pygments_style = 'perldoc'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Fix "en" in sitemap URL
# https://pypi.org/project/sphinx-sitemap/
sitemap_url_scheme = "{link}"

# Bump to force Google reindex
sitemap_filename = "sitemap.xml"

# Logos
# https://pradyunsg.me/furo/customisation/logo/
html_theme_options = {
    # https://pradyunsg.me/furo/customisation/edit-button/
    "source_repository": "https://github.com/tradingstrategy-ai/top-framework/",
    "source_branch": "master",
    "source_directory": "source/",
}

# https://stackoverflow.com/a/62613202/315168
autodoc_class_signature = "separated"

autodoc_typehints = "description"

autosummary_generate = True

add_module_names = False

autodoc_member_order = "bysource"

# autosummary_imported_members = True

# Monkey-patch autosummary template context
from sphinx.ext.autosummary.generate import AutosummaryRenderer


def partial_name(fullname):
    parts = fullname.split(".")
    return parts[-1]


def fixed_init(self, app):
    AutosummaryRenderer.__old_init__(self, app)
    self.env.filters["partial_name"] = partial_name


AutosummaryRenderer.__old_init__ = AutosummaryRenderer.__init__
AutosummaryRenderer.__init__ = fixed_init

