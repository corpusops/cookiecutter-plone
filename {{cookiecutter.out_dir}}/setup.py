# -*- coding: utf-8 -*-
"""Installer for the mirabell.chanel package."""

from setuptools import find_packages
from setuptools import setup


setup(
    name='{{cookiecutter.egg_ns}}.{{cookiecutter.project_name}}',
    version='1.0a1',
    description="{{cookiecutter.egg_ns.capitalize()}} {{cookiecutter.project_name.capitalize()}}",
    long_description="",
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='{{cookiecutter.author}}',
    author_email='{{cookiecutter.author_email}}',
    url='https://pypi.python.org/pypi/{{cookiecutter.egg_ns}}.{{cookiecutter.project_name}}',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['{{cookiecutter.egg_ns}}'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'plone.api>=1.8.4',
        'Products.GenericSetup>=1.8.2',
        'setuptools',
        'z3c.jbot',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = {{cookiecutter.egg_ns}}.{{cookiecutter.project_name}}.locales.update:update_locale
    """,
)
