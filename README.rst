``plone.app.widgets`` is a revamp of plone widgets. It does this by overriding
the widgets of some of the fields in plone.

.. contents::

Introduction
============

Widgets that are overridden in ``Edit`` forms are:

- ``subject``
- ``language``
- ``effectiveDate``
- ``expirationDate``
- ``contributrors``
- ``creators``

Currently ``plone.app.widgets`` only works with Archetypes, but Dexterity
support is planned in next release.

All client side code (javascript/css/images) is done and tested as part of
`Plone Mockup`_ project.

Any feature / bug / compliment please insert in `issue tracker`_.

Installation
============

For now only tested with Plone 4.3.::

    [buildout]
    extends = http://dist.plone.org/release/4.3b2/versions.cfg
    versions = versions
    parts = instance

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    http-address = 8080
    eggs =
        Pillow
        Plone
        plone.app.widgets[archetypes]
    zcml =
        plone.app.widgets

    [versions]
    plone.app.jquery = 1.8.3
    plone.app.search = 1.1.2
    plone.app.vocabularies = 2.1.10


.. _`Plone Mockup`: https://plone.github.com/mockup
.. _`issue tracker`: https://github.com/plone.app.widgets/issues
