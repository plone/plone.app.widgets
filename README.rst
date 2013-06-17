``plone.app.widgets`` is a revamp of plone widgets. It does this by overriding
the widgets of some of the fields in plone.

.. image:: https://travis-ci.org/plone/plone.app.widgets.png?branch=master
   :target: https://travis-ci.org/plone/plone.app.widgets

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
    extends = http://dist.plone.org/release/4.3/versions.cfg
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


Fields and widgets demo gallery
================================

``plone.app.widgets`` provides view ``@@widgets-demo`` which will render
examples of ``zope.schema`` fields and ``plone.app.z3cform`` widgets (Dexterity).

To see the examples go on your Plone site::

    http://localhost:8080/Plone/@@widgets-demo

Contributing to fields and widgets gallery
---------------------------------------------

External packages can add widgets to the demo by inheriting
and registering a demo form snippet. For examples,
see ``plone.app.widgets.demos`` source code.



.. _`Plone Mockup`: http://plone.github.io/mockup
.. _`issue tracker`: https://github.com/plone/plone.app.widgets/issues
