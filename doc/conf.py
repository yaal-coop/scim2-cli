import datetime
import os
import sys
from importlib import metadata

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../scim_cli"))

# -- General configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_click",
]

templates_path = ["_templates"]
master_doc = "index"
project = "scim-cli"
year = datetime.datetime.now().strftime("%Y")
copyright = f"{year}, Yaal Coop"
author = "Yaal Coop"

version = metadata.version("scim_cli")
language = "en"
exclude_patterns = []
pygments_style = "sphinx"
todo_include_todos = True
toctree_collapse = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Options for HTML output ----------------------------------------------

html_theme = "shibuya"
# html_static_path = ["_static"]
html_baseurl = "https://scim-cli.readthedocs.io"
html_theme_options = {
    "globaltoc_expand_depth": 3,
    "accent_color": "orange",
    "gitlab_url": "https://codeberg.org/yaal/scim-cli",
    "mastodon_url": "https://toot.aquilenet.fr/@yaal",
    "nav_links": [
        {
            "title": "SCIM",
            "url": "https://simplecloud.info/",
        },
        {"title": "PyPI", "url": "https://pypi.org/project/scim_cli"},
    ],
}

# -- Options for manual page output ---------------------------------------

man_pages = [(master_doc, "scim-cli", "scim-cli Documentation", [author], 1)]

# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (
        master_doc,
        "scim_cli",
        "scim_cli Documentation",
        author,
        "scim_cli",
        "One line description of project.",
        "Miscellaneous",
    )
]

# -- Options for autosectionlabel -----------------------------------------

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2
