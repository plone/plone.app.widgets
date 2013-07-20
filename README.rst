The goal of ``plone.app.widgets`` is to provide an implementation for a new
set of javascript widgets being developed in the `Plone Mockup`_ project. It
overrides existing widgets used in dexterity and archetypes to provide tested
and modularized widgets based on the concept of *patterns*.

.. image:: https://travis-ci.org/plone/plone.app.widgets.png?branch=master
   :target: https://travis-ci.org/plone/plone.app.widgets

.. contents::

Introduction
============

The widgets that are provided currently are:

- Adjust Text Size -- *Easily change text size on a page.*
- Cookie Directive -- *A pattern that checks cookies enabled and asks
  permission for the user to allow cookies or not.*
- Expose -- *Exposes the focused element by darkening everything else on the
  page. Useful to focus the user attention on a particular area.*
- Form Unload Alert -- *A pattern to warn user when changes are unsaved and
  they try to navigate away from page.*
- Live Search -- *Dynamically query the server and display results.*
- Modal -- *Creates a modal dialog (also called overlay).*
- Pick A Date -- *Allows the user to select a date (with or without time)
  through a calendar.*
- Picture -- *A responsive image widget.*
- Prevent Double Submit -- *A pattern to prevent submitting a form twice.*
- Query String for Collections -- *A widget for creating query's for
  collections*
- Related Items -- *An advanced widget for selecting related items.*
- Select2 -- *Autocompletes, multiple or single selections from any kind of
  data source (with search!).*
- Table Sorter -- *A pattern you can apply to a table so it can have its items
  rearranged when clicking the header.*
- TinyMCE (v4!!!) -- *Rich text editor.*
- Table of Contents -- *Automatically generate a table of contents.*
- Tooltip -- *A pattern to show a tooltip on hover.*
- DropZone -- *Drag 'n drop file upload*

Widgets that are overridden in ``Edit`` forms are:

- ``subject``
- ``language``
- ``effectiveDate``
- ``expirationDate``
- ``contributrors``
- ``creators``
- ``relatedItems``
- ``query``

All client side code (javascript/css/images) is done and tested as part of
`Plone Mockup`_ project.

Any feature / bug / compliment please insert in the `issue tracker`_.


Installation
============

For now only tested with Plone 4.3::

    [buildout]
    extends = http://dist.plone.org/release/4.3.1/versions.cfg
    versions = versions
    parts = instance

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    http-address = 8080
    eggs =
        Pillow
        Plone
        plone.app.widgets[archetypes,dexterity]
    zcml =
        plone.app.widgets

    [versions]
    plone.app.jquery = 1.8.3
    plone.app.vocabularies = 2.1.11


..
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
.. _`issue tracker`: https://github.com/plone/mockup/issues?labels=widgets
