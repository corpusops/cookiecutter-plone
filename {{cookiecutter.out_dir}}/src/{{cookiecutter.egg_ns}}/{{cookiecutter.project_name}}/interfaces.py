# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class I{{cookiecutter.egg_ns.capitalize()}}{{cookiecutter.project_name.capitalize()}}Layer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
