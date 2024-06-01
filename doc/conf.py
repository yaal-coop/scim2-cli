import datetime
import os
import sys
from importlib import metadata

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../scim2_cli"))

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
project = "scim2-cli"
year = datetime.datetime.now().strftime("%Y")
copyright = f"{year}, Yaal Coop"
author = "Yaal Coop"
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

version = metadata.version("scim2_cli")
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
html_baseurl = "https://scim2-cli.readthedocs.io"
html_theme_options = {
    "globaltoc_expand_depth": 3,
    "accent_color": "orange",
    "github_url": "https://github.com/yaal-coop/scim2-cli",
    "mastodon_url": "https://toot.aquilenet.fr/@yaal",
    "nav_links": [
        {
            "title": "SCIM specs",
            "url": "https://simplecloud.info/",
            "children": [
                {
                    "title": "RFC7642 - SCIM: Definitions, Overview, Concepts, and Requirements",
                    "url": "https://tools.ietf.org/html/rfc7642",
                },
                {
                    "title": "RFC7643 - SCIM: Core Schema",
                    "url": "https://tools.ietf.org/html/rfc7643",
                },
                {
                    "title": "RFC7644 - SCIM: Protocol",
                    "url": "https://tools.ietf.org/html/rfc7644",
                },
            ],
        },
        {"title": "pydantic-scim2", "url": "https://pydantic-scim2.readthedocs.io"},
        {
            "title": "httpx-scim2-client",
            "url": "https://httpx-scim2-client.readthedocs.io",
        },
    ],
}

# -- Options for manual page output ---------------------------------------

man_pages = [(master_doc, "scim2-cli", "scim2-cli Documentation", [author], 1)]

# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (
        master_doc,
        "scim2_cli",
        "scim2_cli Documentation",
        author,
        "scim2_cli",
        "One line description of project.",
        "Miscellaneous",
    )
]

# -- Options for autosectionlabel -----------------------------------------

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2
