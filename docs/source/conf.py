# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys
from pathlib import Path

# For sphinx-multiversion, we need to build API docs of the corresponding package version, related issue:
# https://github.com/Holzhaus/sphinx-multiversion/issues/42
pkg_src_dir = (
    Path(os.environ.get("SPHINX_MULTIVERSION_SOURCEDIR", default="."))
    .joinpath("../../src")
    .resolve()
)
sys.path.insert(0, str(pkg_src_dir))

from pydolphinscheduler import __version__  # noqa

# Debug to uncomment this to see the source path
# print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
# print(pkg_src_dir)
# [print(p) for p in sys.path]
# print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")


# -- Project information -----------------------------------------------------

project = "apache-dolphinscheduler"
copyright = "2022, apache"
author = "Apache Software Foundation"

# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # Measures durations of Sphinx processing
    "sphinx.ext.duration",
    # Semi-automatic make docstrings to document
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx_rtd_theme",
    # Documenting command line interface
    "sphinx_click.ext",
    # Add inline tabbed content
    "sphinx_inline_tabs",
    "sphinx_copybutton",
    "sphinx_multiversion",
    "sphinx_github_changelog",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# sphinx_multiversion configuration
html_sidebars = {
    "**": [
        "versioning.html",
    ],
}
# Match all exists tag for pydolphinscheduler expect version 2.0.4(not release apache dolphinscheduler)
smv_tag_whitelist = r"^(?!2.0.4)\d+\.\d+\.\d+$"
smv_branch_whitelist = "main"
smv_remote_whitelist = r"^(origin|upstream)$"
smv_released_pattern = "^refs/tags/.*$"
smv_outputdir_format = "versions/{ref.name}"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
    "private-members": True,
    "undoc-members": True,
    "member-order": "groupwise",
}

autosectionlabel_prefix_document = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
