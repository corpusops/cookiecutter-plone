# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import {{cookiecutter.egg_ns}}.{{cookiecutter.project_name}}


class {{cookiecutter.egg_ns.capitalize()}}{{cookiecutter.project_name.capitalize()}}Layer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package={{cookiecutter.egg_ns}}.{{cookiecutter.project_name}})

    def setUpPloneSite(self, portal):
        applyProfile(portal, '{{cookiecutter.egg_ns}}.{{cookiecutter.project_name}}:default')


{{cookiecutter.egg_ns.upper()}}_{{cookiecutter.project_name.upper()}}_FIXTURE = {{cookiecutter.egg_ns.capitalize()}}{{cookiecutter.project_name.capitalize()}}Layer()


{{cookiecutter.egg_ns.upper()}}_{{cookiecutter.project_name.upper()}}_INTEGRATION_TESTING = IntegrationTesting(
    bases=({{cookiecutter.egg_ns.upper()}}_{{cookiecutter.project_name.upper()}}_FIXTURE,),
    name='{{cookiecutter.egg_ns.capitalize()}}{{cookiecutter.project_name.capitalize()}}Layer:IntegrationTesting',
)


{{cookiecutter.egg_ns.upper()}}_{{cookiecutter.project_name.upper()}}_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=({{cookiecutter.egg_ns.upper()}}_{{cookiecutter.project_name.upper()}}_FIXTURE,),
    name='{{cookiecutter.egg_ns.capitalize()}}{{cookiecutter.project_name.capitalize()}}Layer:FunctionalTesting',
)


{{cookiecutter.egg_ns.upper()}}_{{cookiecutter.project_name.upper()}}_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        {{cookiecutter.egg_ns.upper()}}_{{cookiecutter.project_name.upper()}}_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='{{cookiecutter.egg_ns.capitalize()}}{{cookiecutter.project_name.capitalize()}}Layer:AcceptanceTesting',
)
